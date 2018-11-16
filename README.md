# qemu-composer

`qemu-composer` is a little python script that composes a `docker-compose.yml` file with multiple references of `Dockerfile`s, with appropriate variables, assign multiple one-time cross-compilation images. 

## Whats is intented

This script are apropriated if you want your software developed in worksation running in, let's say, a Raspberry Pi or another uncommon architeture.

Let's call `A` a software developed in your `i386`or `x86_64`.  This can be called `A-i386`or `A-x86_64`.

If you want your `A` software ( `A-i386/A-x86_64`)  to be cross-compiled to another architetures, saying `A-armel`, `A-arm64` (`A-aarch64`) , or many others, you can be at the gates of a hell of `Dockerfile`s an multiple services at a `docker-compose` file.

## Using

This script is intented to be used with travis-ci.

### Instalation 

`pip install qemu-composer`

### Configuration

Build a `.qemu.yml` file and follow a hybrid structure of `docker-compose.yml` files and `.travis.yml` files, i.e, this file run under a `docker-compose.yml` version field, qemu specific fields and `before_install`, `install`, ..., fields:

```
# Same as docker-compose `version`field
# will be copied to `<prefix>/docker-compose.yml`
version: '2'

# The registering qemu binaries to be used
register: multiarch/qemu-user-static:register

# The prefix name of images to be used
# in the one-time cross-compilation
base: multiarch/debian-debootstrap

# The generated images if you want to share
image: redelivre/qemu-alpine-builder

# Register runtime options 
options:
  - --rm
  - --privileged

# Register runtime commands
commands:
  - --reset

# base image arches
arches:
  - arm64

# base image targets
targets:
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

## Running

`$ qemu-composer`

This command is alias for:

`$ qemu-composer --prefix $HOME/bin --file $HOME/.qemu.yml`

## Options

| command | long form | short form | description                                                                                                                             |
|---------|-----------|------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| prefix  | --prefix  | -p         | prefix a folder inside your project to populate the generated `docker-compose.yml` and `Dockerfile`s. Defaults to `<your project>/bin.  |
| file    | --file    | -f         | use this file as the qemu-composer generator. Defaults to `<your project>/.qemu.yml`.                                                   |
