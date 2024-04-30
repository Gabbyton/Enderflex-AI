import os
import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.strategies import DDPStrategy
from data.data_module import ParametersDataModule
from model.network_module import ParametersClassifier

from train_config import *

SEED = 1234

set_seed(SEED)
logs_dir = "logs/logs-{}/{}/".format(DATE, SEED)
logs_dir_default = os.path.join(logs_dir, "default")
CODE_DIR = "/mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton"
make_dirs(logs_dir)
make_dirs(logs_dir_default)

tb_logger = pl_loggers.TensorBoardLogger(logs_dir)
checkpoint_callback = ModelCheckpoint(
    monitor="val_loss",
    dirpath="checkpoints/{}/{}/".format(DATE, SEED),
    filename="MHResAttNet-{}-{}-".format(DATASET_NAME, DATE)
    + "{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}",
    save_top_k=3,
    mode="min",
)

model = ParametersClassifier(
    num_classes=3,
    lr=INITIAL_LR,
    gpus=NUM_GPUS,
    transfer=False,
)

data = ParametersDataModule(
    batch_size=BATCH_SIZE,
    data_dir=DATA_DIR,
    csv_file=DATA_CSV,
    dataset_name=DATASET_NAME,
    mean=DATASET_MEAN,
    std=DATASET_STD,
)

trainer = pl.Trainer(
    num_nodes=NUM_NODES,
    accelerator=ACCELERATOR,
    max_epochs=MAX_EPOCHS,
    logger=tb_logger,
    precision=16,
    strategy=DDPStrategy(find_unused_parameters=True),
    callbacks=[checkpoint_callback],
)

trainer.fit(model, data)
