%define _enable_debug_package 0
%define debug_package %{nil}

Name: 		migration-tools
Version:	1.1.0
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
Requires:migration-tools-data

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

############################
%package -n migration-tools-data
AutoReqProv: no
Summary: migration-tools-data
License: MulanPSL-2.0

%description -n migration-tools-data
Migration software conf side


%prep
%setup -c

%build
pushd migration-tools/ui/report_templates
npm install
make

%install
rm -rf %{buildroot}
%{__mkdir_p} $RPM_BUILD_ROOT/var/tmp/uos-migration
%{__mkdir_p} $RPM_BUILD_ROOT/etc/migration-tools
%{__mkdir_p} $RPM_BUILD_ROOT/usr/lib/migration-tools-agent
%{__mkdir_p} $RPM_BUILD_ROOT/usr/lib/migration-tools-server
%{__mkdir_p} $RPM_BUILD_ROOT/usr/lib/migration-tools-data

%{__cp} -r migration-tools/server/ $RPM_BUILD_ROOT/usr/lib/migration-tools-data/

cp -r migration-tools/* $RPM_BUILD_ROOT/usr/lib/migration-tools-server/

# Install server config
%{__cp} -r $RPM_BUILD_ROOT/usr/lib/migration-tools-server/server/migration-tools.conf $RPM_BUILD_ROOT/etc/migration-tools

# Template
%{__mkdir_p} $RPM_BUILD_ROOT/usr/lib/migration-tools-data/template
%{__cp} -r migration-tools/ui/report_templates/dist/* $RPM_BUILD_ROOT/usr/lib/migration-tools-data/template/


%post -n migration-tools-server
mkdir -p /etc/migration-tools
mkdir -p /var/tmp/uos-migration/UOS_migration_log
cp -r /usr/lib/migration-tools-server/server/migration-tools-server.service /usr/lib/systemd/system/
chmod +x /usr/lib/migration-tools-server/server/start_webview.sh
ln -s /usr/lib/migration-tools-server/server/start_webview.sh /usr/bin/migration-tools
cd /usr/lib/migration-tools-server/migration-tools/views;make
systemctl daemon-reload
systemctl restart migration-tools-server.service
systemctl enable migration-tools-server.service


%postun -n migration-tools-server
systemctl disable migration-tools-server.service
rm -rf /usr/lib/migration-tools-server/
rm -rf /usr/lib/migration-tools
rm -rf /usr/bin/migration-tools

%postun -n migration-tools-agent
systemctl disable migration-tools-agent.service
rm -rf /usr/lib/migration-tools-agent
rm -rf /usr/lib/systemd/system/migration-tools-agent.service
rm -rf /var/tmp/uos-migration
rm -rf /etc/migration-tools

%postun -n migration-tools-data
rm -rf /etc/migration-tools
rm -rf /usr/lib/migration-tools-data
rm -rf /usr/lib/systemd/system/migration-tools-data.service

%files -n migration-tools-server
/etc/migration-tools
/usr/lib/migration-tools-server

%files -n migration-tools-agent
/usr/lib/migration-tools-agent

%files -n migration-tools-data
/usr/lib/migration-tools-data


%changelog
* Mon Nov 11 2024 xuezhixin <xuezhixin@uniontech.com> - 1.1.0-0
- update to 1.1.0

* Wed Aug 16 2023 lixin <lixinb@uniontech.com> - 1.0.0-1
- init
