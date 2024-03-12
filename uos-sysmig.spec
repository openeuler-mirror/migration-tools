%ifarch aarch64
%if 0%{?rhel} < 8 
%global sa_pyenv 1xxc_aarch64
%else
%global sa_pyenv 1xxa_aarch64
%endif
%endif
%ifarch x86_64
%if 0%{?rhel} < 8 
%global sa_pyenv 1xxc_x86_64
%else
%global sa_pyenv 1xxa_x86_64
%endif
%endif
Name: uos-sysmig		
Version:1.0.0	
Release:2%{?dist}
Summary:uos-sysmig	
BuildArch: aarch64 x86_64
License:GPL
Source0:ut-Migration-tools.tar.gz
%description
UOS Migration Software
############################
%package -n uos-sysmig-agent
Summary: uos-sysmig-agent
License: GPL
Requires:yum-utils
Requires:libabigail
Requires:uos-sysmig-data
Requires:python3
%if 0%{?rhel} < 8
Requires:gcc
Requires:openssl-devel
%endif
%description -n uos-sysmig-agent
Migration software agent side
############################
%package -n uos-sysmig-server
Summary: uos-sysmig-server
License: GPL
%if 0%{?rhel} > 7
Requires:nodejs
Requires:openblas,openblas-threads
Requires:libsodium
%endif
Requires:uos-sysmig-data
Requires:sshpass
Requires:python3
%if 0%{?rhel} < 8
Requires:gtk3
%ifarch aarch64
Requires:atlas
%endif
Requires:gcc
Requires:rpm
Requires:openssl-devel
%endif
%description -n uos-sysmig-server
Migration software server side
############################
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
#tar -zxf ut-Migration-tools/sa_pyenv/%{?sa_pyenv}/agent_env.tar.gz -C  $RPM_BUILD_ROOT/usr/lib/uos-sysmig-agent/
#tar -zxf ut-Migration-tools/sa_pyenv/%{?sa_pyenv}/server_env.tar.gz -C $RPM_BUILD_ROOT/usr/lib/uos-sysmig-server/
#cp -r `find ut-Migration-tools -maxdepth 1 |grep '/'|grep -v sa_pyenv|grep conf|xargs`  $RPM_BUILD_ROOT/usr/lib/uos-sysmig-data/
cp -r ut-Migration-tools/sa_pyenv/%{?sa_pyenv}/agent_env.tar.gz   $RPM_BUILD_ROOT/usr/lib/uos-sysmig-agent/
cp -r ut-Migration-tools/sa_pyenv/%{?sa_pyenv}/server_env.tar.gz  $RPM_BUILD_ROOT/usr/lib/uos-sysmig-server/
cp -r ut-Migration-tools/server/ $RPM_BUILD_ROOT/usr/lib/uos-sysmig-data/
cp -r `find ut-Migration-tools -maxdepth 1 |grep '/'|grep -v sa_pyenv|xargs`  $RPM_BUILD_ROOT/usr/lib/uos-sysmig-server/
cp -r `find ut-Migration-tools -maxdepth 1 |grep '/'|grep -v sa_pyenv|grep -v template|xargs` $RPM_BUILD_ROOT/usr/lib/uos-sysmig-agent/
%post -n uos-sysmig-server
mkdir -p /var/tmp/uos-migration
cp -r /usr/lib/uos-sysmig-server/server/uos-sysmig-server.service /usr/lib/systemd/system/
chmod +x /usr/lib/uos-sysmig-server/server/start_webview.sh
ln -s /usr/lib/uos-sysmig-server/server/start_webview.sh /usr/bin/uos-sysmig
tar -zxf /usr/lib/uos-sysmig-server/server_env.tar.gz -C  /usr/lib/uos-sysmig-server/
systemctl daemon-reload
systemctl restart uos-sysmig-server.service
systemctl enable uos-sysmig-server.service
cd /usr/lib/uos-sysmig-server/template && npm i >>/dev/null
systemctl restart uos-sysmig-data.service
%post -n uos-sysmig-agent
mkdir -p /var/tmp/uos-migration
cp -r /usr/lib/uos-sysmig-agent/server/uos-sysmig-agent.service /usr/lib/systemd/system/
tar -zxf /usr/lib/uos-sysmig-agent/agent_env.tar.gz -C  /usr/lib/uos-sysmig-agent/
systemctl daemon-reload
systemctl restart uos-sysmig-agent.service
#systemctl enable uos-sysmig-agent.service
%post -n uos-sysmig-data
mkdir -p /etc/uos-sysmig
cp -r /usr/lib/uos-sysmig-data/server/uos-sysmig.conf /etc/uos-sysmig
cp -r /usr/lib/uos-sysmig-data/server/uos-sysmig-data.service /usr/lib/systemd/system/
systemctl enable uos-sysmig-data.service
systemctl restart uos-sysmig-data.service
%postun -n uos-sysmig-server
systemctl disable uos-sysmig-server.service
rm -rf /usr/lib/uos-sysmig-server
rm -rf /usr/bin/uos-sysmig
rm -rf /usr/lib/systemd/system/uos-sysmig-server.service
rm -rf /var/uos-migration
rm -rf /etc/uos-sysmig
%postun -n uos-sysmig-agent
systemctl disable uos-sysmig-agent.service
rm -rf /usr/lib/uos-sysmig-agent
rm -rf /usr/lib/systemd/system/uos-sysmig-agent.service
rm -rf /var/tmp/uos-migration
rm -rf /etc/uos-sysmig
%postun -n uos-sysmig-data
rm -rf /etc/uos-sysmig
rm -rf /usr/lib/uos-sysmig-data
rm -rf /usr/lib/systemd/system/uos-sysmig-data.service
%files -n uos-sysmig-agent
/usr/lib/uos-sysmig-agent
%files -n uos-sysmig-server
/usr/lib/uos-sysmig-server
%files -n uos-sysmig-data
/usr/lib/uos-sysmig-data
%changelog
* Wed Jan 05 2022 XueZhixin  <xuezhixin@uniontech.com> - 1.0.0-2
- Update to migration 
* Wed Nov 10 2021 XueZhixin  <xuezhixin@uniontech.com> - 1.0.0-1.1
- Build noarch , add anolis8 migration ,fix progress in check_env station
* Tue Oct 19 2021 MengFanSheng  <mengfansheng@uniontech.com> - 1.0.0-1
- Packed uos-sysmig into rpm
