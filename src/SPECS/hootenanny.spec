Name:		hootenanny
Version:	0.2.20_292_g35218bf
Release:	1%{?dist}
Summary:	Hootenanny - we merge maps.

Group:		Applications/Engineering
License:	GPLv3
URL:		https://github.com/ngageoint/hootenanny

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf automake boost-devel cppunit-devel doxygen gcc-c++
BuildRequires:  gdal-devel >= 1.10.1
BuildRequires:  gdb
BuildRequires:  geos-devel = 3.4.2
BuildRequires:  git glpk-devel libicu-devel
BuildRequires:  log4cxx-devel nodejs-devel opencv-devel
BuildRequires:  postgresql91-devel proj-devel protobuf-devel python-argparse python-devel qt-devel
# Needed to build the documentation
BuildRequires:  texlive
BuildRequires:  unzip v8-devel w3m wget words zip

Source0:        %{name}-%{version}.tar.gz

%description
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

%package core
Summary:	Hootenanny Core
Requires:       %{name}-core-deps
Group:		Applications/Engineering

%description core
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This package contains the core algorithms and command line interface.

%prep
%setup -q -n %{name}-%{version}

%build
source ./SetupEnv.sh
# The dir configurations set the install directory to work with EL's dir structure	
./configure --with-rnd -q \
	--prefix=$RPM_BUILD_ROOT/usr/ \
	--datarootdir=$RPM_BUILD_ROOT/usr/share/hootenanny/ \
        --docdir=$RPM_BUILD_ROOT/usr/share/doc/hootenanny/ \
	--localstatedir=$RPM_BUILD_ROOT/var/lib/hootenanny/ \
	--libdir=$RPM_BUILD_ROOT/usr/lib64 \
	--sysconfdir=$RPM_BUILD_ROOT/etc/

# Use ccache if it is available
cp LocalConfig.pri.orig LocalConfig.pri
command -v ccache >/dev/null 2>&1 && echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

make -s %{?_smp_mflags}

%install

make install
echo "export HOOT_HOME=/var/lib/hootenanny" > $RPM_BUILD_ROOT/etc/profile.d/hootenanny.sh
chmod 755 $RPM_BUILD_ROOT/etc/profile.d/hootenanny.sh
cp -R test-files/ $RPM_BUILD_ROOT/var/lib/hootenanny/
ln -s /usr/lib64 $RPM_BUILD_ROOT/var/lib/hootenanny/lib
rm $RPM_BUILD_ROOT/var/lib/hootenanny/conf/words.sqlite
cd $RPM_BUILD_ROOT/var/lib/hootenanny/conf/; ln -s words1.sqlite words.sqlite
rm $RPM_BUILD_ROOT/usr/bin/HootEnv.sh
# This allows all the tests to run.
mkdir -p $RPM_BUILD_ROOT/var/lib/hootenanny/hoot-core-test/src/test/
ln -s /var/lib/hootenanny/test-files/ $RPM_BUILD_ROOT/var/lib/hootenanny/hoot-core-test/src/test/resources
# This makes it so HootEnv.sh resolves hoot home properly.
ln -s /var/lib/hootenanny/bin/HootEnv.sh $RPM_BUILD_ROOT/usr/bin/HootEnv.sh

%check
source ./SetupEnv.sh
# The excluded tests are failing on CentOS now and waiting on a fix
# https://github.com/ngageoint/hootenanny/issues/279
# https://github.com/ngageoint/hootenanny/issues/281
HootTest --exclude=.*RubberSheetConflateTest.sh \
	--exclude=.*ConflateCmdHighwayExactMatchInputsTest.sh \
	--exclude=.*ConflateCmdStatsGenericRiversTest.sh \
	--exclude=.*Osm2OgrTranslation.sh \
	--quick

%clean
rm -rf %{buildroot}

%files core
%{_includedir}/hoot
%{_libdir}/*
%docdir /usr/share/docs/%{name}
%{_datarootdir}/doc/%{name}
%{_bindir}/*
%config %{_sharedstatedir}/%{name}/conf/hoot.json
%config %{_sharedstatedir}/%{name}/conf/DatabaseConfig.sh
%{_sharedstatedir}/%{name}/conf/hoot.json
%{_sharedstatedir}/%{name}/conf/DatabaseConfig.sh
%{_sharedstatedir}/%{name}
%{_sysconfdir}/profile.d/hootenanny.sh
%{_sysconfdir}/asciidoc/filters/



%package core-devel-deps
Summary:	Development dependencies for Hootenanny Core
Group:		Development/Libraries
Requires:	%{name}-core-deps = %{version}-%{release}
Requires:	autoconf automake boost-devel cppunit-devel gcc-c++
Requires:       gdb
Requires:       geos-devel = 3.4.2
Requires:       git glpk-devel libicu-devel log4cxx-devel nodejs-devel opencv-devel
Requires:       postgresql91-devel proj-devel protobuf-devel python-argparse python-devel qt-devel v8-devel
# Needed to build the documentation
Requires:       texlive

%description core-devel-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to build and develop the Hootenanny
core. Use this if you want to build from github.

%files core-devel-deps

%package core-deps
Summary:	Dependencies for Hootenanny Core
Group:		Development/Libraries
Requires:	asciidoc cppunit dblatex doxygen FileGDB_API
Requires:       gdal-devel >= 1.10.1
Requires: 	gdal-esri-epsg >= 1.10.1
Requires:       geos = 3.4.2, gnuplot, graphviz
# Needed by gnuplot for report generation
Requires:       liberation-fonts-common liberation-sans-fonts
Requires:       libxslt log4cxx nodejs opencv postgresql91-libs protobuf qt
Requires:       texlive
Requires:       unzip w3m wget words
Requires:       zip

%description core-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to run the Hootenanny core.

%files core-deps

%changelog
* Thu Jan 21 2016 Jason R. Surratt <jason.surratt@digitalglobe.com> - 0.2.21+
- Initial attempt
