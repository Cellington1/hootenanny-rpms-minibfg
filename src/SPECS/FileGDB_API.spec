# ESRI File Geodatabase API Library
Name:		FileGDB_API
Version:	1.5.1
Release:	1%{?dist}
Summary:	ESRI FileGDB API

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		https://github.com/Esri/file-geodatabase-api

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global filegdbtarball FileGDB_API_%(echo %{version} | tr '.' '_')-64.tar.gz
Source0:	%{filegdbtarball}

%description
The FileGDB API provides basic tools that allow the creation of file
geodatbases, feature classes and tables. Simple features can be created
and loaded.

Copyright © 2014 ESRI

All rights reserved under the copyright laws of the United States and
applicable international laws, treaties, and conventions.

You may freely redistribute and use the sample code, with or without
modification, provided you include the original copyright notice and use
restrictions.

Disclaimer:  THE SAMPLE CODE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL ESRI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

For additional information, contact:
Environmental Systems Research Institute, Inc.
Attn: Contracts and Legal Services Department
380 New York Street
Redlands, California, 92373
USA

email: contracts@esri.com


%files
%docdir /doc/html
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/doc/%{name}-%{version}/*
%{_datarootdir}/pkgconfig/%{name}.pc

%prep
mkdir -p %{name}-%{version}
cd %{name}-%{version}
tar xf %{_sourcedir}/%{filegdbtarball} --strip-components 1

%build
true

%install
rm -fr $RPM_BUILD_ROOT
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/%{name}
install -d %{buildroot}%{_datarootdir}/pkgconfig
install -d %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/FileGDB_SQL_files

install -m 0755 -D %{_builddir}/%{name}-%{version}/lib/*.so %{buildroot}%{_libdir}
install -m 0644 -D %{_builddir}/%{name}-%{version}/lib/*.a %{buildroot}%{_libdir}
install -m 0644 -D %{_builddir}/%{name}-%{version}/include/* %{buildroot}%{_includedir}/%{name}
install -m 0644 -D %{_builddir}/%{name}-%{version}/doc/html/*.{css,html,js,pdf,png,txt,xml} %{buildroot}%{_datarootdir}/doc/%{name}-%{version}
install -m 0644 -D %{_builddir}/%{name}-%{version}/doc/html/FileGDB_SQL_files/*.xml %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/FileGDB_SQL_files

cat > %{buildroot}%{_datarootdir}/pkgconfig/%{name}.pc <<EOF
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: ESRI FileGDB API
Version: %{version}
Cflags: -I\${includedir}
EOF
chmod 0644 %{buildroot}%{_datarootdir}/pkgconfig/%{name}.pc

%check

%clean

%changelog
* Tue Mar 07 2017 Benjamin Marchant <benjamin.marchant@digitalglobe.com>
- Upgrade to v1.5
* Thu Jan 19 2017 Benjamin Marchant <benjamin.marchant@digitalglobe.com>
- Upgrade to v1.4
* Tue Jan 26 2016 Jason R. Surratt <jason.surratt@digitalglobe.com>
- Initial attempt
