Name: 		migration-tools
Version:	1.0.1
Release:	1
License:	MulanPSL-2.0
Summary:	A tool to help users migrate the Centos system to the UOS system and openEuler system

Source0:	ut-Migration-tools.tar.gz
BuildArch: 	noarch
%description
UOS Migration Software

%if 0%{?rhel} < 8
%package -n migration-tools-agent
Summary:        migration-tools-agent
License:        MulanPSL-2.0
Requires:       dnf
Requires:       libabigail
Requires:       python3
Requires:       python3-flask
Requires:       python3-paramiko
Requires:       python3-requests
Requires:       python3-xlrd
Requires:       python3-xlwt
Requires:       openssl
Requires:       rsync
Requires:       yum-utils
%endif

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

%description -n migration-tools-server
Migration software server side


%prep
%setup -c

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/lib/migration-tools-server
mkdir -p $RPM_BUILD_ROOT/usr/lib/migration-tools-agent
mkdir -p $RPM_BUILD_ROOT/var/tmp/uos-migration
mkdir -p $RPM_BUILD_ROOT/etc/migration-tools

cp -r migration-tools/* $RPM_BUILD_ROOT/usr/lib/migration-tools-server/
cp -r migration-tools/* $RPM_BUILD_ROOT/usr/lib/migration-tools-agent/

# Install server config
%{__cp} -r $RPM_BUILD_ROOT/usr/lib/migration-tools-server/server/migration-tools.conf $RPM_BUILD_ROOT/etc/migration-tools


%post -n migration-tools-server
mkdir -p /etc/migration-tools
mkdir -p /var/tmp/uos-migration
cp -r /usr/lib/migration-tools-server/server/migration-tools-server.service /usr/lib/systemd/system/
chmod +x /usr/lib/migration-tools-server/server/start_webview.sh
ln -s /usr/lib/migration-tools-server/server/start_webview.sh /usr/bin/migration-tools
systemctl daemon-reload
systemctl restart migration-tools-server.service
systemctl enable migration-tools-server.service

%post -n migration-tools-agent
mkdir -p /etc/migration-tools
mkdir -p /var/tmp/uos-migration
cp -r /usr/lib/migration-tools-agent/server/migration-tools-agent.service /usr/lib/systemd/system/
systemctl daemon-reload

%postun -n migration-tools-server
systemctl disable migration-tools-server.service
rm -rf /usr/lib/migration-tools-server/
rm -rf /usr/lib/migration-tools
rm -rf /usr/bin/migration-tools

%postun -n migration-tools-agent
rm -rf /usr/lib/migration-tools-agent/
rm -rf /usr/lib/migration-tools
rm -rf /usr/bin/migration-tools

%files -n migration-tools-server
/etc/migration-tools
/usr/lib/migration-tools-server

%files -n migration-tools-agent
/usr/lib/migration-tools-agent

%changelog
* Tue Mar 05 2024 lixin <lixinb@uniontech.com> - 1.0.1-1
- Supports migrations to OpenEuler system using the web-based interface.

* Wed Aug 16 2023 lixin <lixinb@uniontech.com> - 1.0.0-1
- init
