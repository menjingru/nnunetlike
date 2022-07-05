

from global_ import *

from batchgenerators.utilities.file_and_folder_operations import *
from pathlib import Path
import shutil
from multiprocessing import Pool
import SimpleITK as sitk
import numpy as np



# 整理文件夹
def crawl_(folder):  # folder 输入文件夹

    # 验证文件名格式、子文件存在
    assert folder.split('/')[-1].startswith("Task"), "以TaskXX开头，并包含子文件夹imagesTr、labelsTr、imagesTs的文件夹"
    subf = subfolders(folder, join=False)
    assert 'imagesTr' in subf, "没imagesTr"
    assert 'imagesTs' in subf, "没imagesTs"
    assert 'labelsTr' in subf, "没labelsTr"

    # 去掉无用文件
    _ = [os.remove(i) for i in subfiles(folder, prefix=".")]
    _ = [os.remove(i) for i in subfiles(join(folder, 'imagesTr'), prefix=".")]
    _ = [os.remove(i) for i in subfiles(join(folder, 'labelsTr'), prefix=".")]
    _ = [os.remove(i) for i in subfiles(join(folder, 'imagesTs'), prefix=".")]



# 拆分4D数据
def split_4d_nifti(filename, output_folder, add_zeros=False):
    output_folder = Path(output_folder)
    # 读图，维度，名字
    img_itk = sitk.ReadImage(filename)
    dim = img_itk.GetDimension()
    file_base = Path(filename).name

    # 如果三维，末尾加_0000输出
    # 如果四维，不干了
    # 如果二维，删除第四个维度
    if dim == 3:
        shutil.copy(filename, output_folder/(file_base[:-7]+"_0000.nii.gz"))

        return
    elif dim != 4:
        raise RuntimeError("Unexpected dimensionality: %d of file %s, cannot split" % (dim, filename))
    else:
        # 取像素间距、原点、方向
        spacing = img_itk.GetSpacing()
        origin = img_itk.GetOrigin()
        img_npy = sitk.GetArrayFromImage(img_itk)
        direction = np.array(img_itk.GetDirection()).reshape(4,4)
        # 修改像素间距、原点、方向
        spacing = tuple(list(spacing[:-1]))
        origin = tuple(list(origin[:-1]))
        direction = tuple(direction[:-1, :-1].reshape(-1))
        # 咔咔给他cat成三维，删除第四个维度
        for i, t in enumerate(range(img_npy.shape[0])):  # i是序列，t是图
            img = img_npy[t]
            img_itk_new = sitk.GetImageFromArray(img)
            img_itk_new.SetSpacing(spacing)
            img_itk_new.SetOrigin(origin)
            img_itk_new.SetDirection(direction)
            sitk.WriteImage(img_itk_new, str(output_folder/(file_base[:-7]+"_%04.0d.nii.gz" % i)))



# 拆分文件夹
def split_(input_folder, num_processes=default_num_threads):
    input_folder = Path(input_folder)
    # 验证训练用数据和标签文件及json文件都在
    assert Path(input_folder/"imagesTr").is_dir() and Path(input_folder/"labelsTr").is_dir() and \
           Path(input_folder/"dataset.json").is_file(), \
           "输入文件夹必须包含： 子文件夹imagesTr / 子文件夹labelsTr / 文件dataset.json "

    # 验证并提取文件信息（文件名中的信息）----------------------------------------------------------------------------------
    # 验证文件夹以Task开头 —— 符合MSD格式
    full_task_name = Path(input_folder).name
    assert full_task_name.startswith("Task"), "以Task开头"
    # 验证文件夹以01命名 —— 符合MSD格式
    first_underscore = full_task_name.find("_")
    assert first_underscore == 6, "Task后边只能为两位数字"
    # 取id
    input_task_id = int(full_task_name[4:6])
    # 输出、输入文件id同名
    overwrite_task_output_id = input_task_id
    # 项目名
    task_name = full_task_name[7:]

    # 清空、建立、填充输出文件夹----------------------------------------------------------------------------------
    # 输出文件夹命名
    output_folder = Path(nnUNet_raw_data) / str("Task%03d_%s" % (overwrite_task_output_id,task_name))  # %03d 3占位0填充十进制
    output_folder.mkdir(exist_ok=True, parents=True)

    # 输出文件夹清空
    shutil.rmtree(output_folder)


    files = []  # 输入图绝对地址（文件）
    output_dirs = []  # 输出绝对地址（文件夹）

    # 将train和test的图片统一处理至输出文件夹
    for subdir in ["imagesTr", "imagesTs"]:
        curr_out_dir = output_folder/subdir
        curr_out_dir.mkdir(exist_ok=True, parents=True)
        curr_in_dir = input_folder/subdir
        nii_files = [i for i in curr_in_dir.glob('*.nii.gz')]
        nii_files.sort()

        for n in nii_files:  # 先放训练的再放测试的
            files.append(str(n))  # 输入图绝对地址（文件）
            output_dirs.append(str(curr_out_dir))  # 输出绝对地址（文件夹）
            # print(str(n))
            # print(str(curr_out_dir))

    # 标签、json直接复制
    shutil.copytree(input_folder/"labelsTr", output_folder/"labelsTr")
    shutil.copy(join(input_folder, "dataset.json"), output_folder)

    # 多线程执行*1（同一为三维数据）
    p = Pool(num_processes)
    p.starmap(split_4d_nifti, zip(files, output_dirs))  # zip为变量，split_4_nifti为函数
    p.close()
    p.join()



