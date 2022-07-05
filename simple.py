
'''
项目：nnunet_like
项目内编号：3
内容：nnunet_like傻瓜式一键训练
'''

from global_ import *
from dataset_setting import setting
from collections import OrderedDict
from plan_convert_ import convert_
from plan_crop_ import crop_


# -------------------------------------------------------------------------------------------------------

# 1.安装（省略）


# 2.构建文件夹结构（已经在global完成）


# 3.构建标准数据集结构（项目级）    # /home/deepliver2/Disksdd/menjingru/nnUNet_script/nnUNet_dataset_setting.py
to_setting = False

# （修改区）-----------
project_id = 1
project_name = 'spleen'
# （修改区停）----------

# dataset.json配置
dic = OrderedDict()  # 建立有序字典
dic['name'] = str("Task%02d_%s" % (project_id, project_name))

# （修改区）-----------
dic['description'] = 'Segmentation'
dic['tensorImageSize'] = '3D'
dic['reference'] = '可参考数据集/home/deepliver2/Disksdd/spleen_5mm'  # 参考
dic['licence'] = '20220616'
dic['release'] = '0.0'  # 不知道是什么但不重要
dic['modality'] = {'0': 'CT', }
dic['labels'] = {'0': 'background', '1': 'spleen', }  # 脾脏
# （修改区停）-----------

if to_setting:
    save_00 = setting(nnUNet_raw_data,source_path,dic,project_id,project_name)
else:
    # 如果不需要新建项目数据集，可以从已有数据集中手动指定
    save_00 = '/home/deepliver2/Disksdd/menjingru/dataset/nnUNet_raw_data_base/nnUNet_raw_data/Task05_Try'  # （例）


# 4.转换为官方格式（图加_0000，统一为三维）   # nnUNet_convert_decathlon_task -i /home/deepliver2/Disksdd/menjingru/dataset/nnUNet_raw_data_base/nnUNet_raw_data/Task01_Try
to_convert = False
if to_convert:
    id_int = convert_(save_00)
else:
    # 如果不需要转换，可以从已转换数据集中手动指定
    id_int = 1  # （例）


# 5.预处理     # nnUNet_plan_and_preprocess -t NUM
#     crop_(id_int=str(id_int))

# 6.训练      # nnUNet_train 3d_fullres nnUNetTrainerV2 NUM 4


# 7.后处理


# 8.测试   # nnUNet_predict -i /home/deepliver2/Disksdd/menjingru/dataset/nnUNet_raw_data_base/nnUNet_raw_data/Task001_Try/imagesTs -o /home/deepliver2/Disksdd/menjingru/dataset/nnUNet_raw_data_base/nnUNet_raw_data/Task001_Try/infersTs -t 1 -m 3d_fullres -f 4


