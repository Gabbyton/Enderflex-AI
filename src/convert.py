import os.path as path
from PIL import Image
from train_config import *
from model.network_module import ParametersClassifier
from train_config import *
from dotenv import load_dotenv

load_dotenv()
CHECKPOINT_PATH = os.getenv('CHECKPOINT_PATH')
IMG_PATH = os.getenv('IMG_PATH')

model = ParametersClassifier.load_from_checkpoint(
    checkpoint_path=CHECKPOINT_PATH,
    num_classes=3,
    gpus=1,
)
model.eval()

img_path = IMG_PATH
pil_img = Image.open(img_path)
example_input = preprocess(pil_img).unsqueeze(0)

script = model.to_torchscript(method='trace', example_inputs=example_input)
torch.jit.save(script, "deploy/model.pt")