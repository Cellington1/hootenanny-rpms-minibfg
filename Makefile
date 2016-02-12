
# Default branch of hoot to build
GIT_COMMIT?=develop

all: hoot

hoot: | hoot-rpms copy-rpms

hoot-rpms:
	cd src; $(MAKE) hoot

force:

# Clean out all the RPMs
clean:
	rm -rf el6
	cd src; $(MAKE) clean

# Clean out everything
clean-all: vagrant-clean clean

# Cleans out the RPM el6 stash, and all the hoot source/rpms
clean-hoot:
	rm -rf el6
	cd src; $(MAKE) clean-hoot

ValidHootTarball:
	test "$(words $(wildcard src/SOURCES/hootenanny*.tar.gz))" != "1" && (echo "Did not find exactly one hoot tarball in SOURCES. Too many? Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit -1) || true

vagrant-build-up: vagrant-plugins
	vagrant up

copy-words1: vagrant-build-up
	# If we have words1.sqlite locally don't copy it down from github.
	([ -e /tmp/words1.sqlite ] && cat /tmp/words1.sqlite | vagrant ssh -c "cat > /tmp/words1.sqlite") || true

vagrant-plugins:
	# Install the bindfs plugin if it doesn't exist
	(vagrant plugin list | grep -q bindfs) || vagrant plugin install vagrant-bindfs

vagrant-build-deps: copy-words1
	vagrant ssh -c "cd hootenanny-rpms && make deps"

vagrant-build: | vagrant-build-archive vagrant-build-rpms

vagrant-build-rpms: ValidHootTarball vagrant-build-deps
	vagrant up
	vagrant ssh -c "cd hootenanny-rpms && make"

vagrant-build-archive: vagrant-build-deps
	vagrant up
	vagrant ssh -c "export GIT_COMMIT=$(GIT_COMMIT) ; cd hootenanny-rpms && ./BuildArchive.sh"

vagrant-clean:
	vagrant halt
	vagrant destroy -f
	mkdir -p el6
	cd test && vagrant halt && vagrant destroy -f
	rmdir --ignore-fail-on-non-empty el6 || true

vagrant-test:
	cd test; vagrant up
	cd test; vagrant ssh -c "cd /var/lib/hootenanny && sudo HootTest --exclude=.*RubberSheetConflateTest.sh --exclude=.*ConflateCmdHighwayExactMatchInputsTest.sh --slow"

deps: force
	sudo true || true
	sudo cp repos/HootBuild.repo /etc/yum.repos.d
	sudo cp repos/RPM-GPG-KEY-EPEL-6 /etc/pki/rpm-gpg/
	sudo yum clean metadata
	sudo true || true
	# Sometimes the yum update fails getting the metadata. Try several times and ignore
	# the first two if they error
	sudo yum update -y || sleep 30
	sudo yum update -y || sleep 30
	sudo yum update -y
	sudo true || true
	sudo yum install -y \
	  ant \
	  apr-devel \
	  apr-util-devel \
	  armadillo-devel \
	  automake \
	  bison \
	  boost-devel \
	  cairo-devel \
	  cfitsio-devel \
	  CharLS-devel \
	  chrpath \
	  createrepo \
	  ctags \
	  curl-devel \
	  doxygen \
	  emacs \
	  emacs-el \
	  erlang \
	  flex \
	  freexl-devel \
	  g2clib-static \
	  gcc \
	  gd-devel \
	  giflib-devel \
	  git \
	  graphviz \
	  hdf-devel \
	  hdf5-devel \
	  hdf-static \
	  help2man \
	  info \
	  java-1.6.0-openjdk-devel \
	  java-devel \
	  libdap-devel \
	  libgta-devel \
	  libjpeg-turbo-devel \
	  libotf \
	  libpng-devel \
	  librx-devel \
	  libspatialite-devel \
	  libX11-devel \
	  libXt-devel \
	  libxslt \
	  lua-devel \
	  m17n-lib* \
	  m4 \
	  netcdf-devel \
	  pango-devel \
	  pcre-devel \
	  proj-devel \
	  pygtk2 \
	  python-devel \
	  readline-devel \
	  rpm-build \
	  ruby-devel \
	  sqlite-devel \
	  tetex-tex4ht \
	  tex* \
	  transfig \
	  xerces-c-devel \
	  xz-devel \
	  zlib-devel \
	  wget \
	  w3m \
	  words \
	  rpm-build \
	  m4 \
	  emacs \
	  erlang \
	  python-devel \
	  libxslt \
	  ImageMagick \
	  expat-devel \
	  fontconfig-devel \
	  geos-devel \
	  libtool \
	  giflib-devel \
	  mysql-devel \
	  numpy \
	  poppler-devel \
	  postgresql-devel \
	  ruby \
	  swig \
	  unixODBC-devel \
	  gcc-c++ \
	  php-devel \
	  libicu-devel \
	  cppunit-devel \
	  python-argparse \
	  el6-src/* \

el6: el6-src/* custom-rpms

copy-rpms: el6
	rm -rf el6
	mkdir -p el6
	cp -l el6-src/* el6/
	cp src/RPMS/noarch/* el6/
	cp src/RPMS/x86_64/* el6/
	createrepo el6

custom-rpms:
	cd src; $(MAKE)
