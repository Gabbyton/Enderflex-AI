import os
from model.network_module import ParametersClassifier
from PIL import Image
from train_config import *
import time
from dotenv import load_dotenv


load_dotenv()

SAMPLE_DATA = os.getenv('SAMPLE_DATA')
CHECKPOINT_PATH = os.getenv('CHECKPOINT_PATH')

model = ParametersClassifier.load_from_checkpoint(
    checkpoint_path=CHECKPOINT_PATH,
    num_classes=3,
    gpus=1,
)
model.eval()

img_paths = [
    os.path.join(SAMPLE_DATA, img)
    for img in os.listdir(SAMPLE_DATA)
    if os.path.splitext(img)[1] == ".jpg"
]

print("********* CAXTON sample predictions *********")
print("Flow rate | Lateral speed | Z offset | Hotend")
print("*********************************************")

t1 = time.time()

for img_path in img_paths:
    pil_img = Image.open(img_path)
    x = preprocess(pil_img).unsqueeze(0).to('cuda')
    y_hats = model(x)
    y_hat0, y_hat1, y_hat2, y_hat3 = y_hats

    _, preds0 = torch.max(y_hat0, 1)
    _, preds1 = torch.max(y_hat1, 1)
    _, preds2 = torch.max(y_hat2, 1)
    _, preds3 = torch.max(y_hat3, 1)
    preds = torch.stack((preds0, preds1, preds2, preds3)).squeeze()

    preds_str = str(preds.to('cpu').numpy())
    img_basename = os.path.basename(img_path)
    print("Input:", img_basename, "->", "Prediction:", preds_str)

t2 = time.time()
print(f"Completed {len(img_paths)} predictions in {t2 - t1:.2f}s")