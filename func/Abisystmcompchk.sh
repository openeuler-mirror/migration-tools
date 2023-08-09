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

#3. abi检查结果，包括兼容、非兼容的二进制包
#   逐个处理 .diff 结果文件
get_abi_comp_rest()
{
	echo ""
	echo "-------------------------  获取abi兼容、非兼容包列表开始  -------------------------"
	TOTAL_NUM=0
	TOTAL_COMP_NUM=0
	FILE_SO=".so"
	FILE_EXEC=".exec"
	FILE_MOD=".mod"
	DATA_LINE_1="================ changes"
	DATA_LINE_2="Functions changes summary: "
	DATA_LINE_3="Variables changes summary: "
	DATA_LINE_4="Function symbols changes summary: "
	DATA_LINE_5="Variable symbols changes summary: "
	ABI_DIFF_PKG_ABNO=abi-diff-pkg-abno.txt
	ABI_INCOMPAT_PKG_ERR=abi-incompat-pkg-err.txt

	ABI_COMPAT_PKG_LINE="包名"
	ABI_INCOMPAT_PKG_LINE1="abi不兼容的包有INCOMP_PKG_NUM|"
	ABI_INCOMPAT_PKG_LINE2="包名|不兼容类型|不兼容来源|说明"

	cd $DIFF_DIR

	#初始化文件头信息
	echo $ABI_COMPAT_PKG_LINE >> $EXP_DIR/$ABI_COMPAT_PKG
	echo $ABI_INCOMPAT_PKG_LINE1 >> $EXP_DIR/$ABI_INCOMPAT_PKG
	echo $ABI_INCOMPAT_PKG_LINE2 >> $EXP_DIR/$ABI_INCOMPAT_PKG

	for abi_diff_file in `ls *.diff`
	do
		TOTAL_NUM=`expr $TOTAL_NUM + 1`
		NAME=${abi_diff_file%.*}
		FILE_SIZE=`ls -l $abi_diff_file | awk '{print $5}'`
		if [ $FILE_SIZE -eq 0 ];then
			#abi兼容性对比结果文件大小为 0 ，该软件包兼容
			echo $NAME >> $EXP_DIR/$ABI_COMPAT_PKG
			TOTAL_COMP_NUM=`expr $TOTAL_COMP_NUM + 1`
		else
			#将差错报告按以下条件重定向到文件，并分析
			grep "^================ changes" --after-context=4 $abi_diff_file > $abi_diff_file.tmp
        		if [ $? -ne 0 ];then
				grep_rest_tmp="$abi_diff_file|================ changes|grep non-existent!"
				echo $grep_rest_tmp >> $EXP_DIR/$ABI_DIFF_PKG_ABNO 
        		else
				sed -i '/^--$/d' $abi_diff_file.tmp
        		fi
			NUM1=0
			#兼容性开关,0-兼容；1-不兼容
			COMP_FLAG=0
			#cat ./$abi_diff_file.tmp | while read line
			while read line	
			do
				if [[ $line == *$DATA_LINE_1* ]];then 
                			NUM2=$(( $NUM1 % 5 ))
                			if [ $NUM2 = 0 ];then
						str1=${line%\'*}
						data_line="${str1#*\'}"
						if [[ $data_line =~ $FILE_SO ]]
						then
							COMP_TYPE="库差异"
						elif [[ $data_line =~ $FILE_EXEC ]]
						then
							COMP_TYPE="可执行文件"
						elif [[ $data_line =~ $FILE_MOD ]]
						then
							COMP_TYPE="视频文件"
						else
							COMP_TYPE="二进制差异"
						fi
                			else
						#该情况不规范，需要查看
						echo "$NAME|$COMP_TYPE|$data_line|$line" >> $EXP_DIR/$ABI_DIFF_PKG_ERR
					fi
				elif [[ $line == *$DATA_LINE_2* ]];then 
					str2="${line#*: }"
					removed_num=${str2% Removed*}
					change_line=${str2% Changed*}
					change_num=${tmp#*, }
					added_line=${str2% Added*}
					added_num=${tmp1##*,}
					if [[ $removed_num -eq 0 ]] && [[ $change_num -eq 0 ]] && [[ $added_num -eq 0 ]]
					then
						abi_var_comp_2="${abi_diff_file%.*}|$line|兼容"
					else
                        			#echo "$abi_diff_file|$line|不规范，清确认！" >> $EXP_DIR/$ABI_DIFF_PKG_ERR
						abi_var_incomp_2="$NAME|$COMP_TYPE|$data_line|$line"
						echo $abi_var_incomp_2  >> $EXP_DIR/$ABI_INCOMPAT_PKG
						#此时abi编译以来库文件或者二进制包不兼容，那么该rpm包不兼容
						COMP_FLAG=1
					fi
				elif [[ $line == *$DATA_LINE_3* ]];then 
                                        str3="${line#*: }"
                                        removed_num=${str3% Removed*}
                                        change_line=${str3% Changed*}
                                        change_num=${tmp#*, }
                                        added_line=${str3% Added*}
                                        added_num=${tmp1##*,}
                                        if [[ $removed_num -eq 0 ]] && [[ $change_num -eq 0 ]] && [[ $added_num -eq 0 ]]
                                        then
						#abi检查结果中，rpm包以来的库文件或者二进制文件兼容
						abi_var_comp_3="${abi_diff_file%.*}|$line|兼容"
                                        else
                        			#echo "$abi_diff_file|$line|不规范，清确认！" >> $EXP_DIR/$ABI_DIFF_PKG_ERR
						abi_var_incomp_3="$NAME|$COMP_TYPE|$data_line|$line|"
						echo $abi_var_incomp_3  >> $EXP_DIR/$ABI_INCOMPAT_PKG
						#此时abi编译以来库文件或者二进制包不兼容，那么该rpm包不兼容
						COMP_FLAG=1
                                        fi
				elif [[ $line == *$DATA_LINE_4* ]];then 
					str4=${line#*: }
					removed_num=${str4% Removed*}
					if [ $removed_num -ne 0 ]
					then
						#abi检查结果中，rpm包依赖的库文件或者二进制文件不兼容
						abi_var_incomp_4="$NAME|$COMP_TYPE|$data_line|$str4"
						echo $abi_var_incomp_4 >> $EXP_DIR/$ABI_INCOMPAT_PKG
						COMP_FLAG=1
					else
						#此时abi编译依赖库文件或者二进制包兼容
						abi_var_comp_4="${abi_diff_file%.*}|$line|兼容"
					fi
				elif [[ $line == *$DATA_LINE_5* ]];then 
                                	str5=${line#*: }
                                	removed_num=${str5% Removed*}
                                	if [ $removed_num -ne 0 ]
					then
                                                #abi检查结果中，rpm包依赖的库文件或者二进制文件不兼容
                                                abi_var_incomp_5="$NAME|$COMP_TYPE|$data_line|$str5"
                                                echo $abi_var_incomp_5 >> $EXP_DIR/$ABI_INCOMPAT_PKG
                                                COMP_FLAG=1
                                	else
                                                #此时abi编译依赖库文件或者二进制包兼容
                                                abi_var_comp_5="${abi_diff_file%.*}|$line|兼容"
                                	fi
				else 
					ohter_err_info="$NAME|$COMP_TYPE|$data_line|$line|"
					echo $other_err_info >> $EXP_DIR/$ABI_INCOMPAT_PKG_ERR
				fi
				NUM1=`expr $NUM1 + 1`
			done < ./$abi_diff_file.tmp
			#根据兼容性开发COMP_FLAG判断该rpm包是否兼容
			if [ $COMP_FLAG -eq 0 ]
			then
				echo $NAME >> $EXP_DIR/$ABI_COMPAT_PKG
			else
				NUM10=`expr $NUM1 + 1`
			fi
				 
		fi
	done
	rm -f *.diff.tmp

	ABI_INCOMP_NUM_TMP=`cat $EXP_DIR/$ABI_INCOMPAT_PKG | awk -F "|" '{print $1}' | sort | uniq | wc -l`
	ABI_INCOMP_NUM=`expr $ABI_INCOMP_NUM_TMP - 2`
	sed -i 's/INCOMP_PKG_NUM/'$ABI_INCOMP_NUM'/g' $EXP_DIR/$ABI_INCOMPAT_PKG

	#cp -f $EXP_DIR/$ABI_COMPAT_PKG $EXP_DIR/$PKG_COMP_LIST_03 
	#sed -i '/包名/d' $EXP_DIR/$PKG_COMP_LIST_03


	echo "兼容包列表：$EXP_DIR/$ABI_COMPAT_PKG"
	echo "非兼容包列表：$EXP_DIR/$ABI_INCOMPAT_PKG"
	echo "-------------------------  获取abi兼容、非兼容包列表结束  -------------------------"
}

#4. 获取系统基本信息
get_system_info()
{
	#echo "====================Start enter get_system_info=============="
        #数据清理
        rm -f $EXP_DIR/$SYSTEM_INFO

	#SYSTEM_INFO_1_LINE1="|当前系统|迁移系统"
	SYSTEM_INFO_1_LINE1="|当前系统"
	#SYSTEM_INFO_2_LINE2="系统版本|CUR_VERSION|TRA_VERSION"
	SYSTEM_INFO_2_LINE2="系统版本|CUR_VERSION"
	#SYSTEM_INFO_3_LINE3="内核版本|CUR_KERNEL_VERSION|TRA_KERNEL_VERSION"
	SYSTEM_INFO_3_LINE3="内核版本|CUR_KERNEL_VERSION"

	SYSTEM_INFO_5_LINE5="/var/cache可用空间|CUR_USE_SPACE"
	SYSTEM_INFO_6_LINE6="架构|CUR_ARCH"

	#SYSTEM_INFO_8_LINE8="软件包|被替换的软件包|安装的软件包"
	SYSTEM_INFO_8_LINE8="软件包|被替换的软件包"
	#SYSTEM_INFO_9_LINE9="软件包数量|REPLACE_PKG_NUM|INSTALL_PKG_NUM"
	SYSTEM_INFO_9_LINE9="软件包数量|REPLACE_PKG_NUM"

	SYSTEM_INFO_11_LINE11="ABI"
	SYSTEM_INFO_12_LINE12="兼容数量|COMP_NUM"
	SYSTEM_INFO_13_LINE13="不兼容数量|INCOMP_NUM"
	SYSTEM_INFO_14_LINE14="总数|SUM_NUM"

        echo $SYSTEM_INFO_1_LINE1 >> $EXP_DIR/$SYSTEM_INFO

        #获取系统版本
	cur_sysinfo_1=`cat /etc/os-release | grep PRETTY_NAME`
	cur_sysinfo_2=${cur_sysinfo_1#*=}
	cur_sysinfo_len_1=`echo ${cur_sysinfo_1#*=} | wc -L`
	cur_sysinfo_len=`expr $cur_sysinfo_len_1 - 2`

	cur_sysinfo=${cur_sysinfo_2:1:$cur_sysinfo_len}

	system_info_2_line2=${SYSTEM_INFO_2_LINE2//CUR_VERSION/$cur_sysinfo}
	#system_info_2_line2=${system_info_2_line2_tmp//TRA_VERSION/$trans_sysinfo}
        echo $system_info_2_line2 >> $EXP_DIR/$SYSTEM_INFO

	#获取内核版本
        cur_kernel_info=`uname -r`
        #trans_kernel_info="******"

	system_info_3_line3=${SYSTEM_INFO_3_LINE3//CUR_KERNEL_VERSION/$cur_kernel_info}
	#system_info_3_line3=${system_info_3_line3_tmp//TRA_KERNEL_VERSION/$trans_kernel_info}
        echo $system_info_3_line3 >> $EXP_DIR/$SYSTEM_INFO
	echo " " >> $EXP_DIR/$SYSTEM_INFO

	#cache空间及架构
	cur_cache_space_tmp=`head -1 $CACHE_SPACE`
        cur_cache_space=${cur_cache_space_tmp#*为}
        cur_system_arch=`uname -m`

	system_info_5_line5=${SYSTEM_INFO_5_LINE5//CUR_USE_SPACE/$cur_cache_space}
        echo $system_info_5_line5 >> $EXP_DIR/$SYSTEM_INFO

	system_info_6_line6=${SYSTEM_INFO_6_LINE6//CUR_ARCH/$cur_system_arch}
        echo $system_info_6_line6 >> $EXP_DIR/$SYSTEM_INFO
	echo " " >> $EXP_DIR/$SYSTEM_INFO

        echo $SYSTEM_INFO_8_LINE8 >> $EXP_DIR/$SYSTEM_INFO

        abi_comp_pkg_num_tmp=`cat $EXP_DIR/$ABI_COMPAT_PKG | wc -l`
        cur_pkg_num=`expr $abi_comp_pkg_num_tmp - 1`
        #cur_pkg_sum=`rpm -qa | wc -l`
        #trans_pkg_sum=`rpm -qa | wc -l`

	system_info_9_line9=${SYSTEM_INFO_9_LINE9//REPLACE_PKG_NUM/$cur_pkg_num}
	#system_info_9_line9=${system_info_9_line9_tmp//INSTALL_PKG_NUM/$trans_pkg_sum}
        echo $system_info_9_line9 >> $EXP_DIR/$SYSTEM_INFO
	echo " " >> $EXP_DIR/$SYSTEM_INFO

        echo $SYSTEM_INFO_11_LINE11 >> $EXP_DIR/$SYSTEM_INFO

        #abi_comp_pkg_num_tmp=`cat $EXP_DIR/$ABI_COMPAT_PKG | wc -l`
        #abi_comp_pkg_num=`expr $abi_comp_pkg_num_tmp - 1`
	#system_info_12_line12=${SYSTEM_INFO_12_LINE12//COMP_NUM/$abi_comp_pkg_num}
	system_info_12_line12=${SYSTEM_INFO_12_LINE12//COMP_NUM/$cur_pkg_num}
        echo $system_info_12_line12 >> $EXP_DIR/$SYSTEM_INFO

        abi_incomp_pkg_num_tmp=`cat $EXP_DIR/$ABI_INCOMPAT_PKG | awk -F "|" '{print $1}'| sort | uniq |wc -l`
        abi_incomp_pkg_num=`expr $abi_incomp_pkg_num_tmp - 2`
	system_info_13_line13=${SYSTEM_INFO_13_LINE13//INCOMP_NUM/$abi_incomp_pkg_num}
        echo $system_info_13_line13 >> $EXP_DIR/$SYSTEM_INFO

        abi_pkg_num=`expr $abi_comp_pkg_num + $abi_incomp_pkg_num`
	system_info_14_line14=${SYSTEM_INFO_14_LINE14//SUM_NUM/$abi_pkg_num}
        echo $system_info_14_line14 >> $EXP_DIR/$SYSTEM_INFO

	#echo "====================End enter get_system_info=============="
}

#5. 软件包对比
pkg_comp_rst()
{
	#软件包对比文件头定义
	PKGINFO_1_LINE1="待替换/安装的软件包共SUM1个，新安装的软件包共SUM2个"
	PKGINFO_2_LINE2="当前系统持有（不替换）|迁移系统软件包总表"
	PKGINFO_3_LINE3="OTH_VERSION|UOS_VERSION"

	#echo "==============Start enter pkg_comp_rst========="
        #清理数据
        rm -f $EXP_DIR/$PKG_COMP_LIST_01

        pkg_sum_num=`cat $EXP_DIR/$UOS_PKG_RPMS_LIST | wc -l`
        #pkg_num_inst=`cat $EXP_DIR/$UOS_PKG_RPMS_LIST | grep uelc20 | wc -l`
        pkg_num_inst_tmp=`cat $EXP_DIR/$ABI_COMPAT_PKG | wc -l`
	pkg_num_inst=`expr $pkg_num_inst_tmp - 1`


	pkginfo_1_line1_tmp=${PKGINFO_1_LINE1//SUM1/$pkg_sum_num}
	pkginfo_1_line1=${pkginfo_1_line1_tmp//SUM2/$pkg_num_inst}

        echo $pkginfo_1_line1 >> $EXP_DIR/$PKG_COMP_LIST_01

        echo $PKGINFO_2_LINE2 >> $EXP_DIR/$PKG_COMP_LIST_01

        #获取系统版本
        cur_sysinfo_1=`cat /etc/os-release | grep PRETTY_NAME`
        cur_sysinfo_2=${cur_sysinfo_1#*=}
        cur_sysinfo_len_1=`echo ${cur_sysinfo_1#*=} | wc -L`
        cur_sysinfo_len=`expr $cur_sysinfo_len_1 - 2`

        cur_sysinfo=${cur_sysinfo_2:1:$cur_sysinfo_len}

        trans_sysinfo_1="UOS Server Enterprise "

	pkginfo_3_line3_tmp=${PKGINFO_3_LINE3//OTH_VERSION/$cur_sysinfo}
	pkginfo_3_line3=${pkginfo_3_line3_tmp//UOS_VERSION/$trans_sysinfo_1}
        echo $pkginfo_3_line3 >> $EXP_DIR/$PKG_COMP_LIST_01

	#cat $EXP_DIR/$UOS_PKG_RPMS_LIST | grep uelc20 > $EXP_DIR/$PKG_COMP_LIST_04	
	#echo "==============End enter pkg_comp_rst========="
}

create_file_path
get_rpm_list
get_abi_comp_rest
get_system_info
pkg_comp_rst