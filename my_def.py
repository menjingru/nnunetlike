
from global_ import *
from pathlib import Path
import numpy as np

def linear_list_use(list1,result):
    for s in list1:
        if type(s) != list:
            result.append(s)

        else:
            linear_list_use(s,result)
def linear_list(list):
    result = []
    linear_list_use(list,result)
    return result



def may_i(id):
    raw_same_id = nnUNet_raw_data
    crop_same_id = nnUNet_cropped_data
    pp_same_id = nnUNet_preprocessed
    model_same_id = nnUNet_trained_models_out


    startswith = "Task%03.0d" % id

    raw_same_id = [i for i in Path(raw_same_id).glob('%s*'%startswith)]
    crop_same_id = [i for i in Path(crop_same_id).glob('%s*'%startswith)]
    pp_same_id = [i for i in Path(pp_same_id).glob('%s*'%startswith)]
    # 取nnUNet_trained_models/nnUNet/四个/这个id的文件夹
    model_same_id = linear_list([[k for k in Path(i).glob('%s*'%startswith)] for i in [str(Path(model_same_id)/j) \
             for j in ['2d', '3d_lowres', '3d_fullres', '3d_cascade_fullres'] if (Path(model_same_id)/j).is_dir()]])


    all_candidates = raw_same_id + crop_same_id + pp_same_id + model_same_id
    all_candidates_id = [i.name for i in all_candidates]
    all_candidates_path = [str(i) for i in all_candidates]
    # print(all_candidates_id)
    # print(all_candidates_path)
    unique_candidates_id = np.unique(all_candidates_id)
    unique_candidates_path = np.unique(all_candidates_path)
    if len(unique_candidates_id) > 1:
        raise RuntimeError("有多个该编号文件，名称为" + str(unique_candidates_id) + '\n' + '\t'*7 +
                           '  位置为\n' + str(unique_candidates_path) + '\n' + '\t'*7 + '  你处理一下，留你需要的那个就行')
    if len(unique_candidates_id) == 0:
        raise RuntimeError("没有该编号文件（三位数）")
    return unique_candidates_id[0]
