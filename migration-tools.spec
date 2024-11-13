%define _enable_debug_package 0
%define debug_package %{nil}

Name: 		migration-tools
Version:	1.2.0
Release:	0
License:	MulanPSL-2.0
Summary:	A tool to help users migrate the Centos system to the UOS system and openEuler system

Source0:	migration-tools.tar.gz
BuildRequires: make

ExcludeArch:loongarch64 i686
%description
UOS Migration Software


%package -n migration-tools-agent
Summary: migration-tools-agent
License: GPL
Requires:dnf
Requires:libabigail
Requires:python3
Requires:python3-xlrd
Requires:python3-xlwt
Requires:python3-paramiko
Requires:python3-flask
Requires:rsync
Requires:yum-utils

%description -n migration-tools-agent
Migration software agent side


%package -n migration-tools-server
Summary: 	migration-tools-server
License:	MulanPSL-2.0
Requires:	python3
Requires:	python3-pip
Requires:	sshpass
Requires:	python3-paramiko
Requires:	python3-flask
Requires:	python3-requests
Requires:	mysql-server
Requires:	mysql-devel

%description -n migration-tools-server
Migration software server side


%prep
%setup -c

%build
#pushd template
#make build
#popd
pushd ui/report_templates
#pushd ui/uyi-reports
make
popd
pushd ui/mainApp
make
popd

%install
rm -rf %{buildroot}
%{__mkdir_p}  $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/uos-sysmig
%{__mkdir_p}  $RPM_BUILD_ROOT/usr/lib/migration-tools-server/migration-tools
%{__mkdir_p}  /var/tmp/uos-migration
#%{__cp} -r sa_pyenv/%{?sa_pyenv}/agent_env.tar.gz   $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/
#%{__cp} -r sa_pyenv/%{?sa_pyenv}/server_env.tar.gz  $RPM_BUILD_ROOT/usr/lib/migration-tools-server/
%{__cp} -r uos-sysmig/*  $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/uos-sysmig/
%{__cp} -r uos-sysmig/*  $RPM_BUILD_ROOT/usr/lib/migration-tools-server/
%{__cp} -r ui/report_templates/dist $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/
#%{__cp} -r ui/uyi-reports/dist $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/
# install the ui folder `static` and `templates`
%{__cp} -r ui/mainApp/dist/* $RPM_BUILD_ROOT/usr/lib/migration-tools-server/
%{__cp} -r server  $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/
%{__cp} -r server  $RPM_BUILD_ROOT/usr/lib/migration-tools-server/
%{__cp} -r migration-tools.sql  $RPM_BUILD_ROOT/usr/lib/migration-tools-server/

%post -n migration-tools-server
%{__mkdir_p} /var/tmp/uos-migration
%{__mkdir_p} /etc/migration-tools
%{__mkdir_p} /var/tmp/uos-migration/UOS_migration_log
%{__cp} -r /usr/lib/migration-tools-server/server/migration-tools.conf /etc/migration-tools
%{__cp} -r /usr/lib/migration-tools-server/server/migration-tools-server.service /usr/lib/systemd/system/
chmod +x /usr/lib/migration-tools-server/migration-tools/start_webview.py
%{__ln_s} /usr/lib/migration-tools-server/migration-tools/start_webview.py /usr/local/bin/migration-tools
%{__tar} -zxf /usr/lib/migration-tools-server/server_env.tar.gz -C  /usr/lib/migration-tools-server/
%{__cp} -r  /usr/lib/migration-tools-server/migration-tools.sql /etc/migration-tools
cd /usr/lib/migration-tools-server/migration-tools/views;make
systemctl daemon-reload
systemctl restart migration-tools-server.service
systemctl enable migration-tools-server.service

%post -n migration-tools-agent
%{__mkdir_p} /var/tmp/uos-migration
%{__mkdir_p}  /var/tmp/uos-migration/UOS_migration_log
%{__mkdir_p} /etc/migration-tools
%{__cp} -r /usr/lib/migration-tools-agent/server/migration-tools.conf /etc/migration-tools
%{__cp} -r /usr/lib/migration-tools-agent/server/migration-tools-agent.service /usr/lib/systemd/system/
%{__cp} -r /usr/lib/migration-tools-agent/sysmig_agent/destroy.py /var/tmp
%{__tar}  -zxf /usr/lib/migration-tools-agent/agent_env.tar.gz -C  /usr/lib/migration-tools-agent/
systemctl daemon-reload
#systemctl restart migration-tools-agent.service
#systemctl enable migration-tools-agent.service

%postun -n migration-tools-server
systemctl disable migration-tools-server.service
%{__mkdir_p}  /var/tmp/uos-migration/UOS_migration_log
%{__mkdir_p} /etc/migration-tools
%{__cp} -r /usr/lib/migration-tools-agent/server/migration-tools.conf /etc/migration-tools
rm -rf /usr/lib/migration-tools-server
rm -rf /usr/bin/migration-tools
rm -rf /usr/lib/systemd/system/migration-tools-server.service
rm -rf /var/uos-migration
rm -rf /etc/migration-tools

%postun -n migration-tools-agent
systemctl disable migration-tools-agent.service
%{__mkdir_p} /var/tmp/uos-migration/UOS_analysis_report
rm -rf /usr/lib/migration-tools-agent
rm -rf /usr/lib/systemd/system/migration-tools-agent.service
rm -rf /var/tmp/uos-migration
rm -rf /etc/migration-tools
rm -rf /var/uos-migration

%files -n migration-tools-agent
/usr/lib/migration-tools-agent

%files -n migration-tools-server
/usr/lib/migration-tools-server


%changelog
* Wed Nov 13 2024 xuezhixin <xuezhixin@uniontech.com> - 1.2.0-0
- update to 1.2.0

* Mon Nov 11 2024 xuezhixin <xuezhixin@uniontech.com> - 1.1.0-0
- update to 1.1.0

* Wed Aug 16 2023 lixin <lixinb@uniontech.com> - 1.0.0-1
- init
