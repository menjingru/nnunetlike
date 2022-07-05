
'''
项目：nnunet_like
项目内编号：1
内容：标准数据集-转换数据
'''


from global_ import *
from plan_convert_def import *

import argparse



def convert_(save00=None):

    # 设置参数
    # （命令）plan_convert_ -i 输入文件夹
    # （可选）                    -p 线程

    parser = argparse.ArgumentParser(description="转换格式")

    parser.add_argument("-i", required=False, default=save00, help="输入文件夹 TaskXX_TASKNAME ")


    parser.add_argument("-p", required=False, default=default_num_threads, type=int,
                        help="线程数 is %d" % default_num_threads)
    args = parser.parse_args()

    # 整理文件夹（验证文件夹格式、子文件存在、去除无用文件）——源码中称为MSD格式
    crawl_(args.i)

    # 拆分文件夹
    split_(args.i, args.p)
    id_int = int(Path(save00).name[4:6])
    return id_int



if __name__ == "__main__":
    convert_()
