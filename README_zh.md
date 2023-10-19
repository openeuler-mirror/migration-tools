# migration-tools

#### 介绍
统信迁移工具是由统信公司自主研发，具有CentOS系列系统迁移至OpenEuler系统或UOS系统功能的迁移工具。

#### 依赖

* python3
* /bin/bash
* rpm, dnf, curl

#### 安装教程

本工具主要由python和shell构成，开箱即用。


#### 环境准备

1.  需要请确保您系统已经完整的备份资料与系统设置。

2.  需要有稳定的网络连接。

3.  所有自动更新，例如通过' yum-cron '应该被禁用。

4.  系统迁移后，无法再次在更新后的系统中使用此工具。

5.  确保在'/var/cache'中至少有5GB的可用空间。

#### 使用说明

1.  新建镜像挂载目录：
    `mkdir /mnt/iso`
2.  将1002a/1020a镜像文件挂载至/mnt/iso目录下
    `mount xxxxx.iso /mnt/iso`
3.  运行shell/python脚本
    centos7:
    `./centos72uos.sh`
    centos8:
    `python3 centos82uos.py`

#### 参与贡献

我们鼓励您报告问题并做出更改

- [代码仓库地址](https://gitee.com/openeuler/migration-tools)

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

## 开源许可证

migration-tools 在 [MulanPubL-2.0-or-later](LICENSE)下发布。
