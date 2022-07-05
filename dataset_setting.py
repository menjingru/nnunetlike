# -*- coding:utf-8 -*-
"""
项目：nnunet_like
项目内编号：0
内容：标准数据集-框架填充
"""

# python -c 'import torch;print(torch.backends.cudnn.version())'
# python -c 'import torch;print(torch.__version__)'

from global_ import *

from pathlib import Path
from shutil import copy
import json




def setting(nnUNet_raw_data,source_path,dic,id=0,name = '',ratio=0.8):
    # 项目位置
    save_dir = Path(nnUNet_raw_data)/str("Task%02d_%s" % (id,name))
    # print('save_dir',save_dir)
    save_dir.mkdir(exist_ok=True,parents=True)

    # 创建文件夹框架
    train_img_dir = save_dir/"imagesTr"
    train_label_dir = save_dir/"labelsTr"
    test_img_dir = save_dir/"imagesTs"
    train_img_dir.mkdir(exist_ok=True,parents=True)
    train_label_dir.mkdir(exist_ok=True,parents=True)
    test_img_dir.mkdir(exist_ok=True,parents=True)

    # 对数据进行分配
    #    ↓
    source_path = Path(source_path)
    img_path = sorted([i for i in source_path.glob('**\*_V.nii.gz')])  # 排序
    label_path = sorted([i for i in source_path.glob('**\*_all_vessel.nii.gz')])
    print(len(img_path) == len(label_path))
    cut_num = int(len(img_path)*ratio)  # 比例
    train_img = img_path[:cut_num]
    train_label = label_path[:cut_num]
    test_img = img_path[cut_num:]
    for i in range(len(train_img)):  # 训练图
        copy(train_img[i],str(train_img_dir/train_img[i].name))
        copy(train_label[i],str(train_label_dir/train_img[i].name))
        # print(train_img_dir/train_img[i].name)
        # print(train_label_dir/train_img[i].name)
    for k in img_path[cut_num:]:  # 测试图
        copy(str(k),str(test_img_dir/k.name))
    #    ↑

    dic['numTraining'] = len(train_img)
    dic['numTest'] = len(test_img)
    dic['training'] = [{'image': str(train_img_dir/idx.name), "label": str(train_label_dir/idx.name)} for idx in train_img]
    dic['test'] = [str(test_img_dir/i.name) for i in test_img]


    j = json.dumps(dic, sort_keys=False, indent=4)

    with open(save_dir/'dataset.json', 'w') as f:
        f.write(j)


    print(' 本次训练信息: \n save_dir（文件框架地址）:   %s \n source_path（图像原地址）:  %s \n ratio（训练样本比例）:      %s' % (save_dir, source_path, ratio))
    print()
    print(' over')
    return str(save_dir)
