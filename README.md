# Hootenanny RPMs

This repository houses the RPM building specifications for Hootenanny and its
third-party dependencies.

## Requirements

* `rpm`
* Docker

RPMs are built in minimal, ephemeral CentOS 7 Docker containers.  Invoking programs
use `spec` files as the source of truth for version information and require `rpm`
itself in order to parse.  On Ubuntu platforms you can install RPM with:

```
sudo apt-get -y install rpm
```

## Quickstart

Build Hootenanny RPM build container using release dependencies (those that are already
available):

```
./BuildHootImages
```

Once that's complete you can build a Hootenanny archive tarball with:

```
./BuildArchive.sh
```

And the RPMs may be built with:

```
./BuildHoot.sh
```

Note: dependency-only packages will be in `RPMS/noarch`, and Hootenanny packages will be placed in `RPMS/x86_64`.
