# qemu-composer

[![Build Status](https://travis-ci.org/lunhg/qemu-composer.svg?branch=master)](https://travis-ci.org/lunhg/qemu-composer) [![Coverage Status](https://coveralls.io/repos/github/lunhg/qemu-composer/badge.svg?branch=master)](https://coveralls.io/github/lunhg/qemu-composer?branch=master)

`qemu-composer` is a python command line interface that composes a `docker-compose.yml` file  under a prefixed/posfixed path with multiple references to many `Dockerfile`. These files are indexed under appropiated paths and variables, assigning a single cross-compilation images for many processor architetures within a containerized, at the current version, in a debian environment.

## Whats is intented

Supose that you want a software developed in your laptop running in a Raspberry Pi with `arm* ` architeture (like is my case).

Let's call `A` that software developed in your `i386`or `x86_64`.  This wiil be `A-i386`or `A-x86_64`. The `A` software ( `A-i386/A-x86_64`) will be cross-compiled to another architetures, saying `A-armel`, `A-arm64` (`A-aarch64`).

## Using

This script is intented to be used with travis-ci, but you can use locally.

### Instalation from pip

`$ pip install qemu-composer`

### Instalation from source

```
$ git clone https://www.github.com/lunhg/qemu-composer.git
$ cd qemu-composer/
$ pip install -e .
```

### Configuration

Create a `.qemu.yml` file that follow a hybrid structure of `docker-compose.yml` files and `.travis.yml` files.

This file will:

  - create a `docker-compose.yml` with apropriated version field
  - register a special `docker` image that runs `QEMU`
  - base the qemu specific architeture, that generates a `FROM <base>` directive in `Dockerfile`s
  - register a `before_install` command field  running under root privilegies
  - register `install` and subsequent command fields running a user with a randomic name

```
# Same as docker-compose `version`field
# will be copied to `<prefix>/docker-compose.yml`
version: '2'

# The registering qemu binaries to be used
register: multiarch/qemu-user-static:register

# The prefix name of images to be used in the one-time cross-compilation in Dockerfile as FROM * 
base: multiarch/debian-debootstrap

# The generated images if you want to share
image: redelivre/qemu-alpine-builder

# Where alll will builded <--prefix from cli>/.bin
prefix: .bin

# Register runtime options 
options:
  - --rm
  - --privileged

# Register runtime commands
commands:
  - --reset

# base image arches
arches:
  - armel
  - armhf
  - arm64

# base image targets
targets:
  - wheezy
  - jessie

# The environment os builds
env:
  - VAR=<name>
  ...

# RUN commands
# User is root on this point
# Useful in update apt-packages
before_install:
  - echo "`whoami` running `uname -a` at `hostname`"
  - apt-get update
  - apt-get install -y <pkg>
  ...

# User isnt root on this point
install:
  - echo "`whoami` running `uname -a` at `hostname`"
  ...
  
after_install:
  - echo "`whoami` running `uname -a` at `hostname`"
  ...

before_script:
  - echo "`whoami` running `uname -a` at `hostname`"
  ...
  
script:
  - echo "`whoami` running `uname -a` at `hostname`"
  ...
  
after_script:
  - echo "`whoami` running `uname -a` at `hostname`"
  ...
```

### Running tests

  - Simple test: 
  
  ```
  $ pytest
  ```
  
  - Complete test: 
  
  ```
  $ sudo COVERALLS_TOKEN=<token> tox
  ```
  
  If you found a compilation error from `cffi`, module, you will need to add a `CFLAGS` environment variable.
  
  This occurs when you are using a non-debian OS, like a Archlinux:
  
  ```
  $ sudo COVERALLS_TOKEN=<token> CFLAGS=-I/<path-to-libffi> tox
  ```

### LIBFFI paths:

  - Archlinux: 
    - path: /usr/lib/libffi-<version>/include:
    - installing: `pacman -Syu libffi`
  
## Running as CLI

`$ qemu-composer`

This command is alias for:

`$ qemu-composer --prefix $PWD/<define prefix in file> --file .qemu.yml`

## Options

| Option name | long form | short form | description                                                      |
|-------------|-----------|------------|------------------------------------------------------------------|
| prefix      | --prefix  | -p         | Set a prefix where qemu-composer runs (default: $PWD)            |
| file        | --file    | -f         | The file where qemu-composer is configured (default: .qemu.yml)  |
| group       | --group   | -G         | The group of a passwordless user in qemu                         |
| gid         | --gid     | -g         | The gid of the group                                             |
| uid         | --uid     | -u         | The uid of passwordless user of qemu                             |
