Name: uos-sysmig
Version:1.0.0
Release:1%{?dist}
Summary:uos-sysmig

License:GPL
Source0:ut-Migration-tools.tar.gz
BuildArch: noarch
%description
UOS Migration Software


%package -n uos-sysmig-agent
Summary: uos-sysmig-agent
License: GPL
Requires:python3
Requires:yum-utils
Requires:libabigail
Requires:python3-xlrd
Requires:python3-xlwt
Requires:uos-sysmig-data
Requires:python3-paramiko
Requires:python3-flask
Requires:python3-pyasn1

%if 0%{?rhel} < 8
Requires:python3-cffi
Requires:python-devel
Requires:dnf
Requires:gcc
Requires:openssl-devel
%endif


%description -n uos-sysmig-agent
Migration software agent side


%package -n uos-sysmig-server
Summary: uos-sysmig-server
License: GPL
Requires:python3
Requires:python3-pip
Requires:uos-sysmig-data
Requires:sshpass
Requires:python3-paramiko
Requires:python3-flask

%if 0%{?rhel} < 8
Requires:python3-gobject
Requires:python3-cffi
Requires:python3-requests
Requires:dnf
Requires:python3-xlrd
Requires:gcc
Requires:openssl-devel
%endif


%description -n uos-sysmig-server
Migration software server side


%package -n uos-sysmig-data
Summary: uos-sysmig-data
License: GPL

%description -n uos-sysmig-data
Migration software conf side

%prep
%setup -c

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/lib/uos-sysmig-agent
mkdir -p $RPM_BUILD_ROOT/usr/lib/uos-sysmig-server
mkdir -p $RPM_BUILD_ROOT/usr/lib/uos-sysmig-data
mkdir -p /var/tmp/uos-migration
cp -r ut-Migration-tools/* $RPM_BUILD_ROOT/usr/lib/uos-sysmig-data/
cp -r ut-Migration-tools/* $RPM_BUILD_ROOT/usr/lib/uos-sysmig-server/
cp -r ut-Migration-tools/* $RPM_BUILD_ROOT/usr/lib/uos-sysmig-agent/

%post -n uos-sysmig-server
mkdir -p /var/tmp/uos-migration
cp -r /usr/lib/uos-sysmig-server/server/uos-sysmig-server.service /usr/lib/systemd/system/
chmod +x /usr/lib/uos-sysmig-server/server/start_webview.sh
ln -s /usr/lib/uos-sysmig-server/server/start_webview.sh /usr/bin/uos-sysmig
systemctl daemon-reload
systemctl restart uos-sysmig-server.service
systemctl enable uos-sysmig-server.service


%post -n uos-sysmig-agent
mkdir -p /var/tmp/uos-migration
cp -r /usr/lib/uos-sysmig-agent/server/uos-sysmig-agent.service /usr/lib/systemd/system/
systemctl daemon-reload
systemctl restart uos-sysmig-agent.service
systemctl enable uos-sysmig-agent.service

%post -n uos-sysmig-data
mkdir -p /etc/uos-sysmig
cp -r /usr/lib/uos-sysmig-data/server/uos-sysmig.conf /etc/uos-sysmig

%postun -n uos-sysmig-server
systemctl disable uos-sysmig-server.service
rm -rf /usr/lib/uos-sysmig-server/
rm -rf /usr/lib/uos-sysmig

%postun -n uos-sysmig-agent
systemctl disable uos-sysmig-agent.service
rm -rf /usr/lib/uos-sysmig-agent/

%postun -n uos-sysmig-data
rm -rf /etc/uos-sysmig

%files -n uos-sysmig-agent
/usr/lib/uos-sysmig-agent

%files -n uos-sysmig-server
/usr/lib/uos-sysmig-server

%files -n uos-sysmig-data
/usr/lib/uos-sysmig-data


%changelog
* Wed Aug 16 2023 lixin <lixinb@uniontech.com> - 1.0.0-1
- init
