#!/bin/bash
set -x
# Script to switch CentOS (or other similar distribution) to the UniontechOS

set -e
unset CDPATH
KERNEL=/var/tmp/uos-migration/kernel

while getopts :d:k: opt
do
    case "$opt" in
    d) pwddir=${OPTARG};echo "Kernle diractory is ${OPTARG} - $pwddir";;
    k) knl=${OPTARG};echo "Kernel opt is ${OPTARG} - $knl";;
    *) echo "Null";;
    esac
done

echo $pwddir


if [ -n "$knl" ]
then
	sed -i 's/^exclude=.*/exclude=/g'  /etc/yum.conf
	rm -rf $KERNEL
	mkdir -p $KERNEL
	cd $KERNEL
	i=`rpm -qa|grep 'kernel\|bpftool\|perf'|xargs -i rpm -q --qf "%{name} " {}`
	v=`rpm -qa|grep 'kernel'|xargs -i rpm -q --qf "%{version}\\n" {} |sort -u `
	yumdownloader --enablerepo UniontechOS-kernel-$knl --disablerepo UniontechOS-AppStream --skip-broken  $i
        if [ $? != 0 ]
	then
		echo 'No downloader'
	fi
	rpms=`ls $KERNEL`
	rpm -Uvh $KERNEL/*.rpm --nodeps --oldpackage
        rpm -ef $i-$u --nodeps
fi

