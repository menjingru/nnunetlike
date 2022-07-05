

# 环境配置
import os
from pathlib import Path
import platform

# 动
os.environ["CUDA_VISIBLE_DEVICES"] = "4,5,6,7"
folder_ = "E:\dataset"

source_path = 'E:\NRRD'


# 不动
nnUNet_raw_data_base = Path(folder_)/"nnUNet_raw_data_base"
nnUNet_preprocessed = Path(folder_)/"nnUNet_preprocessed"
nnUNet_trained_models = Path(folder_)/"nnUNet_trained_models"
nnUNet_trained_models_out = Path(nnUNet_trained_models)/"nnUNet"
nnUNet_raw_data_base.mkdir(exist_ok=True,parents=True)
nnUNet_preprocessed.mkdir(exist_ok=True,parents=True)
nnUNet_trained_models.mkdir(exist_ok=True,parents=True)
nnUNet_trained_models_out.mkdir(exist_ok=True,parents=True)

nnUNet_raw_data = Path(nnUNet_raw_data_base)/"nnUNet_raw_data"
nnUNet_cropped_data = Path(nnUNet_raw_data_base)/"nnUNet_cropped_data"
nnUNet_raw_data.mkdir(exist_ok=True,parents=True)
nnUNet_cropped_data.mkdir(exist_ok=True,parents=True)

# 默认线程8
if (platform.system() == 'Windows'):
    default_num_threads = 1
else:
    default_num_threads = 8

