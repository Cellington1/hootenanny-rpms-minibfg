# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# rpmbuild -bb ./SPECS/tomcat8.spec
%define __jar_repack %{nil}
%global major_version 8
%global minor_version 5
%global micro_version 24
%global tomcat_group tomcat
%global tomcat_user tomcat
%global tomcat_uid 91
%global tomcat_home %{_datadir}/%{name}
%global tomcat_basedir %{_sharedstatedir}/%{name}
%global tomcat_cache %{_var}/cache/%{name}
%global tomcat_config %{_sysconfdir}/%{name}
%global tomcat_logs %{_var}/log/%{name}


Summary:    Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
Name:       tomcat8
Version:    %{major_version}.%{minor_version}.%{micro_version}
Release:    1%{?dist}
License:    ASL 2.0
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    http://www.apache.org/dist/tomcat/tomcat-%{major_version}/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1:    %{name}.conf
Source2:    %{name}.functions
Source3:    %{name}.logrotate
Source4:    %{name}.named-service
Source5:    %{name}.preamble
Source6:    %{name}.server
Source7:    %{name}.service
Source8:    %{name}.sysconfig
Source9:    %{name}.wrapper
BuildArch:  noarch
Requires:   jpackage-utils
Requires:   java-1.8.0-openjdk

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.

This package contains the base tomcat installation that depends on OpenJDK
and not on JPP packages.

%prep
%setup -q -n apache-tomcat-%{version}

%build
# Don't need any Windows batch files.
find . -type f \( -name "*.bat" -o -name "*.tmp" \) -delete

%install
%{__install} -d -m 0755 %{buildroot}%{tomcat_home}
# Set allowLinking to true in Tomcat context.
%{__sed} -i '/<Context>/a\    \<Resources allowLinking="true"/>' conf/context.xml

# Copy all, but omit documentation.
%{__cp} -R * %{buildroot}%{tomcat_home}/
%{__rm} -rf %{buildroot}%{tomcat_home}/{LICENSE,NOTICE,RELEASE-NOTES,RUNNING.txt,temp,work}

# Remove all webapps. Put webapps and degree workspace in /var/lib
# and link back.
%{__rm} -rf %{buildroot}%{tomcat_home}/webapps
%{__install} -d -m 0775 %{buildroot}%{tomcat_basedir}/webapps
pushd %{buildroot}%{tomcat_home}
%{__ln_s} %{tomcat_basedir}/webapps webapps
%{__chmod} 0755 %{buildroot}%{tomcat_basedir}
popd

# Put logging in /var/log and link back.
%{__rm} -rf %{buildroot}%{tomcat_home}/logs
%{__install} -d -m 0775 %{buildroot}%{tomcat_logs}
pushd %{buildroot}%{tomcat_home}
%{__ln_s} %{tomcat_logs} logs
popd

# Put conf in /etc/ and link back.
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}
%{__mv} %{buildroot}%{tomcat_home}/conf %{buildroot}%{tomcat_config}
%{__install} -d -m 0755 %{buildroot}%{tomcat_config}/conf.d
%{__install} -d -m 0775 %{buildroot}%{tomcat_config}/Catalina
pushd %{buildroot}%{tomcat_home}
%{__ln_s} %{tomcat_config} conf
popd

# Put temp and work to /var/cache and link back.
%{__install} -d -m 0775 %{buildroot}%{tomcat_cache}
%{__install} -d -m 0775 %{buildroot}%{tomcat_cache}/temp
%{__install} -d -m 0775 %{buildroot}%{tomcat_cache}/work
pushd %{buildroot}%{tomcat_home}
%{__ln_s} %{tomcat_cache}/temp
%{__ln_s} %{tomcat_cache}/work
popd

# Drop conf script
%{__install} -m 0644 %{SOURCE1} %{buildroot}%{tomcat_config}/%{name}.conf

# Drop functions.
%{__install} -d -m 0755 %{buildroot}%{_libexecdir}/%{name}
%{__install} -m 0755 %{SOURCE2} %{buildroot}%{_libexecdir}/%{name}/functions
%{__install} -m 0755 %{SOURCE5} %{buildroot}%{_libexecdir}/%{name}/preamble
%{__install} -m 0755 %{SOURCE6} %{buildroot}%{_libexecdir}/%{name}/server

# Drop sbin script
%{__install} -m 0755 -d %{buildroot}%{_sbindir}
%{__install} -m 0755 %{SOURCE9} %{buildroot}%{_sbindir}/%{name}

# Drop systemd service units.
%{__install} -m 0755 -d %{buildroot}%{_unitdir}
%{__install} -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}@.service

# Drop sysconfig script
%{__install} -m 0755 -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Drop logrotate script
%{__install} -m 0755 -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
%{__rm} -rf %{buildroot}

%pre
getent group %{tomcat_group} 2>/dev/null || \
    %{_sbindir}/groupadd \
     --system \
     --gid %{tomcat_uid} \
     %{tomcat_group}
getent passwd %{tomcat_user} 2>/dev/null || \
    %{_sbindir}/useradd \
     --system \
     --comment "Apache Tomcat 8 Daemon User" \
     --uid %{tomcat_uid} \
     --gid %{tomcat_group} \
     --home %{tomcat_home} \
     --shell /sbin/nologin \
     %{tomcat_user}

%files
%doc LICENSE NOTICE RELEASE-NOTES RUNNING.txt
%defattr(-,root,root)
%{_libexecdir}/%{name}/functions
%{_libexecdir}/%{name}/preamble
%{_libexecdir}/%{name}/server
%{_sbindir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%{tomcat_home}/bin
%{tomcat_home}/conf
%{tomcat_home}/lib
%{tomcat_home}/logs
%{tomcat_home}/temp
%{tomcat_home}/webapps
%{tomcat_home}/work
%dir %{tomcat_config}
%dir %{tomcat_config}/conf.d
%config(noreplace) %{tomcat_config}/*.conf
%config(noreplace) %{tomcat_config}/*.xml
%config(noreplace) %{tomcat_config}/*.xsd
%config(noreplace) %{tomcat_config}/*.policy
%config(noreplace) %{tomcat_config}/*.properties
# files owned by tomcat user
%defattr(-,%{tomcat_user},%{tomcat_group})
%dir %{tomcat_basedir}
%dir %{tomcat_cache}
%dir %{tomcat_cache}/temp
%dir %{tomcat_cache}/work
%dir %{tomcat_config}/Catalina
%{tomcat_basedir}/webapps
%{tomcat_logs}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%changelog
* Fri Jan 12 2018 Justin Bronn <justin.bronn@digitalglobe.com> - 8.5.24-1
- Upgrade to 8.5.24.
- Replaced init script with systemd units.
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 8.5.23-1
- Initial release.
