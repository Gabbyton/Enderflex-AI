import requests
from urllib.parse import urlparse
import time

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

GOOD_EXIT_CODE = 200

def extract_data(prefix, url, body_tag='div', section_class='file-section', data_tag='dd', download_tag='ds-file-download-link', rsrc_tag='href'):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == GOOD_EXIT_CODE:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser') # default for parsing HTML docs
        # Find all elements with the specified tag
        page_data = []
        for element in soup.find_all(body_tag, class_=section_class):
            data_name, data_size, data_format, data_license = [content.text for content in element.find_all(data_tag)]
            download_url = f"{prefix}{element.find(download_tag).a.get(rsrc_tag)}"
            page_data.append([data_name, data_size, data_format, data_license, download_url])
        return page_data
    else:
        raise Exception(response.status_code)

def initial_pop(base_url, end_idx, start_idx=1):
    # URL must come in form http://www.repository.com/.../...?...page=
    url_queue = [(f'{base_url}{i}', 0) for i in range(start_idx, end_idx + 1)]
    return url_queue

if __name == "__main__":
    
    OUTPUT_PATH = "caxton-data-download.csv"
    STATUS_PATH = "caxton-data-status.csv"
    BASE_URL = "https://www.repository.cam.ac.uk/items/6d77cd6d-8569-4bf4-9d5f-311ad2a49ac8/full?obo.page="
    COUNT = 40 # number of pages on the detailed version of the web page for the repository
    REST_TIME = 1 # in seconds
    RETRIES = 5

    parsed_url = urlparse(BASE_URL)
    prefix = f"{parsed_url.scheme}://{parsed_url.netloc}"

    url_queue = initial_pop(BASE_URL, COUNT)
    url_data = []
    good_urls = []
    bad_urls = []

    while url_queue:
        url, tries = url_queue.popleft()
        print(f'items left in queue: {len(url_queue)}')
        try:
            new_data = extract_data(prefix, url)
            url_data.extend(new_data)
            good_urls.append([url, GOOD_EXIT_CODE, True])
            time.sleep(REST_TIME)
        except Exception as exc:
            if tries < RETRIES:
                url_queue.append((url, tries + 1))
            else:
                bad_urls.append([url, exc.args[0], False])

    print("The queue finish processing with the following results:")
    print(f"Successes: {len(good_urls)}, Failures: {len(bad_urls)}")

    data_df = pd.DataFrame(url_data, columns=['name', 'size', 'format', 'license', 'url'])
    data_df.to_csv(OUTPUT_PATH)
    print("Data saved to {OUTPUT_PATH}")

    all_status = good_urls.extend(bad_urls)
    status_df = pd.DataFrame(
        all_status,
        columns=["url", "status_code", "success"])

    status_df.to_csv(STATUS_PATH)
    print("Status of Results saved to {STATUS_PATH}")