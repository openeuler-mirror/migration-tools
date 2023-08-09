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

#2. 获取rpm包列表,并解压rpm包
get_rpm_list()
{
	#清理历史数据
        if [ -f "$EXP_DIR/$UOS_PKG_RPMS_LIST" ]
        then
		rm -f $EXP_DIR/$UOS_PKG_RPMS_LIST
	fi

        if [ -f "$EXP_DIR/$OTH_PKG_RPMS_LIST" ]
        then
		rm -f $EXP_DIR/$OTH_PKG_RPMS_LIST
	fi

	#获取当前系统包列表
	for line in `rpm -qa | sort`
	do 
		var=${line%-*} 
		echo ${var%-*} >> $EXP_DIR/$OTH_PKG_RPMS_LIST 
	done

	#源仓库批量下载当前系统包列表
	for downpkg in `cat $EXP_DIR/$OTH_PKG_RPMS_LIST`
	do
		string=$downpkg
		downpkg_list="${downpkg_list} ${string}"
	done

	yumdownloader --destdir=$UOS_DIR $downpkg_list --skip-broken

	#获取迁移系统包列表
	cd $UOS_DIR && for line1 in `ls *.rpm`;do var1=${line1%-*} echo ${var1%-*} >> $EXP_DIR/$UOS_PKG_RPMS_LIST ;done 

	#当前系统与迁移系统共有的包列表
	grep -f $EXP_DIR/$UOS_PKG_RPMS_LIST $EXP_DIR/$OTH_PKG_RPMS_LIST > $EXP_DIR/$PKG_COMP_LIST_04

	#当前系统有，迁移系统无的包列表
	grep -wvf $EXP_DIR/$UOS_PKG_RPMS_LIST $EXP_DIR/$OTH_PKG_RPMS_LIST > $EXP_DIR/$PKG_COMP_LIST_02

	#根据包名找到对应的.rpm包,通过判断：(包名长度+1)个字符为数字判断是否为要解压的包
	for data in `cat $EXP_DIR/$PKG_COMP_LIST_04`
	do
		data_len=`expr length "$data"`
		len_char=`expr $data_len + 1`

		cmd_rst=`ls $data*`
		#针对同一包名多个查找结果处理
		for pkg_name in $cmd_rst
		do
			char=${pkg_name:$len_char:1}
			echo "$char" | [ -n "`sed -n '/^[0-9][0-9]*$/p'`" ] && rpm2cpio $pkg_name | cpio -idmv
		        if [ $? == 0 ];then

				#条件不完整,可根据情况添加检测的目录
                		rpm -qpl $pkg_name | grep -v ".build-id\|\/etc\/\|\/share\/" > $EXP_DIR/rpm-pkg-info.txt
                		deal_file $EXP_DIR/rpm-pkg-info.txt $data
				mv $UOS_DIR/$pkg_name  $UOS_DIR/$pkg_name$SUFFIX
        		fi
		done
	done
}