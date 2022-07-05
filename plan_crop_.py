
"""
项目：nnunet_like
项目内编号：2
内容：预处理
"""


from global_ import *
from plan_crop_def import *
from my_def import may_i
import argparse


def crop_(id_int='0'):

    # 设置参数
    # （命令）plan_crop_ -t 任务id
    # （可选）                    憋写了

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task_ids", nargs="+", default=id_int, help="任务id")
    parser.add_argument("-pl3d", "--planner3d", type=str, default="ExperimentPlanner3D_v21",help="一般用默认")
    parser.add_argument("-pl2d", "--planner2d", type=str, default="ExperimentPlanner2D_v21",help="一般用默认")
    parser.add_argument("-no_pp", action="store_true", help="不执行预处理")
    parser.add_argument("-tl", type=int, required=False, default=8,help="低分辨扩进程,一般不用")
    parser.add_argument("-tf", type=int, required=False, default=8,help="高分辨缩进程,一般不用")
    # parser.add_argument("--verify_dataset_integrity", required=False, default=False, action="store_true",help="检查数据集完整，一般不用")
    parser.add_argument("--verify_dataset_integrity", required=False, default=True, action="store_true",help="检查数据集完整，一般不用")
    parser.add_argument("-overwrite_plans", type=str, default=None, required=False,help="指定计划文件，一般不用")  # （只能3d用）
    parser.add_argument("-overwrite_plans_identifier", type=str, default=None, required=False,
                        help="制定计划标识，一般不用，如果要用的话"
                             "格式参考'nnUNet_train CONFIG TRAINER TASKID FOLD -p nnUNetPlans_pretrained_IDENTIFIER -pretrained_weights FILENAME'")
    args = parser.parse_args()

    # 取参
    task_ids = args.task_ids
    dont_run_preprocessing = args.no_pp
    tl = args.tl
    tf = args.tf
    planner_name3d = args.planner3d
    planner_name2d = args.planner2d
    # print(planner_name3d)  # ExperimentPlanner3D_v21
    # print(planner_name2d)  # ExperimentPlanner2D_v21

    # raw data，验证项目数据集 / crop处理数据和标签
    tasks = []
    for i in task_ids:  # 是的，可以好几个任务一起
        i = int(i)
        # 检查id对应文件，并返回id唯一文件名
        task_name = may_i(i)
        print(task_name)
        # 需要检查数据集是否完整吗
        if args.verify_dataset_integrity:
            # 是的我对这个也解析了！！！见3.检查数据完整
            verify_dataset_integrity(join(nnUNet_raw_data, task_name))
        # crop(task名字，覆盖吗，高分辨线程）
        crop(task_name, False, tf)
        # crop(task_name, True, tf)

        tasks.append(task_name)

    # 准备搞数据指纹！！！！
    # planner_name3d =  'ExperimentPlanner3D_v21'
    for t in tasks:
        print("\n\n\n", t)
        # 取已crop好的项目，建立项目预处理的输出文件夹
        cropped_out_dir = os.path.join(nnUNet_cropped_data, t)
        preprocessing_output_dir_this_task = os.path.join(nnUNet_preprocessed, t)

        # 加载json（判断是否需要强度属性）
        dataset_json = load_json(join(cropped_out_dir, 'dataset.json'))
        modalities = list(dataset_json["modality"].values())
        # print('modalities',modalities) → ['CT']
        # 收集/不收集强度属性（当有 CT模态 时，需要强度属性）
        collect_intensityproperties = True if (("CT" in modalities) or ("ct" in modalities)) else False

        # 数据指纹！！！！！！！！！！！！！！！！！！！！！！！！！
        # DatasetAnalyzer（切好的文件地址，覆盖，高分辨进程）
        # print('图名列表',get_patient_identifiers_from_cropped_files(cropped_out_dir)) →
        # ['1000_V_5mm', '1001_V_5mm', '1002_V_5mm', '1003_V_5mm', '1004_V_5mm', '1006_V_5mm', '1007_pizang_V_5mm',
        #  '1008_V_5mm', '1009_V_5mm', '1010_V_5mm']
        dataset_analyzer = DatasetAnalyzer(cropped_out_dir, overwrite=False, num_processes=tf)  # 此类创建指纹
        _ = dataset_analyzer.analyze_dataset(collect_intensityproperties)  # 这将写入 ExperimentPlanner 使用的输出文件
        print('-------------------------------------------------------------')

        maybe_mkdir_p(preprocessing_output_dir_this_task)
        shutil.copy(join(cropped_out_dir, "dataset_properties.pkl"), preprocessing_output_dir_this_task)
        shutil.copy(join(nnUNet_raw_data, t, "dataset.json"), preprocessing_output_dir_this_task)

        threads = (tl, tf)

        # 制定计划！！！！！！！！！！！！！！！！！！！！！！！！
        print("number of threads: ", threads, "\n")

        # 只做三维演示
        exp_planner = ExperimentPlanner3D_v21(cropped_out_dir, preprocessing_output_dir_this_task)
        exp_planner.plan_experiment()
        if not dont_run_preprocessing:  # 如果进行预处理（双重否定）
            exp_planner.run_preprocessing(threads)

# 重采样和归一化？
# 标准化？

if __name__ == "__main__":
    crop_()