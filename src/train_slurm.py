import os
import os.path as path
import sys
from datetime import datetime
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.strategies import DDPStrategy
from data.data_module import ParametersDataModule
from model.network_module import ParametersClassifier

from train_config import *

SEED = 1234

# Do not edit the print statements!!!!

try:
    #line contains one line of your input CSV file
    parquet_path = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    print(f'[SLURMSTART] {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")} Job started with args:-{parquet_path} {start} {end}') 
    input_df = pd.read_parquet(parquet_path, engine='pyarrow').iloc[start:end]
    try:
        output = input_df[["output"]].iloc[0]

        set_seed(SEED)
        logs_dir = path.join(CODE_DIR, "logs/logs-{}/{}/".format(DATE, SEED))
        logs_dir_default = path.join(logs_dir, "default")

        make_dirs(logs_dir)
        make_dirs(logs_dir_default)

        tb_logger = pl_loggers.TensorBoardLogger(logs_dir)
        checkpoint_callback = ModelCheckpoint(
            monitor="val_loss",
            dirpath=path.join(CODE_DIR, "checkpoints/{}/{}/".format(DATE, SEED)),
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
            accelerator="auto",
            max_epochs=MAX_EPOCHS,
            logger=tb_logger,
            precision=16,
            strategy=DDPStrategy(find_unused_parameters=True),
            callbacks=[checkpoint_callback],
        )

        trainer.fit(model, data)
    except Exception as exc:
        print("[CODE_ERROR]")
        print(f"Exception found:\n\n{exc}")
    
    # print sample contents
    print(output)
    #Your code ends here

    print(f'[SLURMEND] {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")} Job finished successfully')
except Exception as e:
    print(f'[SLURMFAIL] {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")} Job failed, see error below')
    raise