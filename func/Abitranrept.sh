#!/bin/bash

#系统迁移后调用该脚本获取迁移后系统信息，为迁移后生成报告准备

LOCAL_DIR=/var/tmp/uos-migration/data
#LOCAL_DIR=/var/data

#输出结果目录
EXP_DIR=$LOCAL_DIR/exp-rst

#系统基本信息文件
SYSTEM_INFO=systeminfo.txt
TRAND_END_SYSINFO=trans-end-sysinfo.txt

#软件包对比文件
PKG_COMP_LIST_01=pkginfo_1.txt
PKG_COMP_LIST_01_TRANS=pkginfo_1_trans.txt
PKG_COMP_LIST_03=pkginfo_3.txt

#1. 获取迁移后系统基本信息
get_system_info()
{
        #数据清理
        rm -f $EXP_DIR/$TRAND_END_SYSINFO

	line_num=1
	while read line
	do
		if [ $line_num -eq 1 ];then
			SYSTEM_INFO_1_LINE1="$line|迁移系统"
			echo $SYSTEM_INFO_1_LINE1 >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 2 ];then
        		#获取系统版本
        		cur_sysinfo_1=`cat /etc/os-release | grep PRETTY_NAME`
			cur_sysinfo_2=${cur_sysinfo_1#*=}
			cur_sysinfo_len_1=`echo ${cur_sysinfo_1#*=} | wc -L`
			cur_sysinfo_len=`expr $cur_sysinfo_len_1 - 2`

			cur_sysinfo=${cur_sysinfo_2:1:$cur_sysinfo_len}

			SYSTEM_INFO_2_LINE2="$line|$cur_sysinfo"
			echo $SYSTEM_INFO_2_LINE2 >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 3 ];then
			#当前系统版本
        		cur_kernel_info=`uname -r`
			SYSTEM_INFO_3_LINE3="$line|$cur_kernel_info"
			echo $SYSTEM_INFO_3_LINE3 >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 4 ];then
			echo "" >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 5 ];then
			echo $line >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 6 ];then
			echo $line >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 7 ];then
			echo "" >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 8 ];then
			SYSTEM_INFO_8_LINE8="$line|安装的软件包"
			echo $SYSTEM_INFO_8_LINE8 >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 9 ];then
			install_num=`rpm -qa | grep uelc20 | wc -l`
			SYSTEM_INFO_9_LINE9="$line|$install_num"
			echo $SYSTEM_INFO_9_LINE9 >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 10 ];then
			echo "" >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 11 ];then
			echo $line >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 12 ];then
			echo $line >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 13 ];then
			echo $line >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		if [ $line_num -eq 14 ];then
			echo $line >> $EXP_DIR/$TRAND_END_SYSINFO
		fi

		line_num=`expr $line_num + 1`

	done < $EXP_DIR/$SYSTEM_INFO
}

#5. 软件包对比
pkg_comp_rst()
{
	VAR_LINE="迁移系统特有（新安装）"

        #清理数据
        rm -f $EXP_DIR/$PKG_COMP_LIST_01_TRANS

	line_num=1

	while read line 
	do

		if [ $line_num -eq 1 ];then
        		echo $line >> $EXP_DIR/$PKG_COMP_LIST_01_TRANS
		fi

		if [ $line_num -eq 2 ];then
			var_1=${line%|*}
			var_2=${line#*|}
			PKGINFO_2_LINE2="$var_1|$VAR_LINE|$var_2"
        		echo $PKGINFO_2_LINE2 >> $EXP_DIR/$PKG_COMP_LIST_01_TRANS
		fi

		if [ $line_num -eq 3 ];then
        		echo $line >> $EXP_DIR/$PKG_COMP_LIST_01_TRANS
		fi

		line_num=`expr $line_num + 1`
	done < $EXP_DIR/$PKG_COMP_LIST_01

	#获取已安装包列表
	for line1 in `rpm -qa | grep uelc20`
	#for line1 in `rpm -qa | grep el8`
	do 
		var1=${line1%-*} 
		echo ${var1%-*} >> $EXP_DIR/$PKG_COMP_LIST_03 
	done

	#迁移完成后uelc20包列表不为空，如果为空创建空文件以便统计汇总xls
	if [ ! -f $EXP_DIR/$PKG_COMP_LIST_03 ];then
		touch $EXP_DIR/$PKG_COMP_LIST_03
	fi
}

get_system_info
pkg_comp_rst

