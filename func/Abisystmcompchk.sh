#!/bin/bash
# 项目名称: abi结果自动化分析实现
# 所属系统: UOS
# 文件名称: Abisystemcompcheck
# 功    能: 基于系统兼容性检查报告的自动化分析
#         : 输出系统兼容百分比，非兼容包原因列表，兼容包列表等。
# 作    者: lihaipeng

########################变量定义#################################

LOCAL_DIR=/var/tmp/uos-migration/data

#原始数据目录
UOS_DIR=$LOCAL_DIR/uos/rpms
DIFF_DIR=$LOCAL_DIR/all-diff

#输出结果目录
EXP_DIR=$LOCAL_DIR/exp-rst

#系统基本信息文件
SYSTEM_INFO=systeminfo.txt

#1. 创建目录
create_file_path()
{
	#接收yum仓库下载的rpm目录
        if [ ! -d "$UOS_DIR" ]
        then
                mkdir -p $UOS_DIR
                echo "mkdir -p $UOS_DIR success ... "
        fi

	#数据导出目录
        if [ ! -d "$EXP_DIR" ]
        then
                mkdir -p $EXP_DIR
                echo "mkdir -p $EXP_DIR success ... "
        fi

	#abidiff工具检测结果目录
        if [ ! -d "$DIFF_DIR" ]
        then
                mkdir -p $DIFF_DIR
                echo "mkdir -p $DIFF_DIR success ... "
        fi
}

