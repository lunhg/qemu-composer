
import os, sys, uuid, yaml, subprocess

class QemuComposer(object):

    def __init__(self, **kwargs):
        self.group = kwargs.get('group')
        self.gid = kwargs.get('gid')
        self.uid = kwargs.get('uid')
        self.prefix = kwargs.get('prefix')
        self.qemu = self.__qemu__(kwargs.get('file'))
        self.uuid = self.__id__()
        options = " ".join(str(x) for x in self.qemu['options'])
        commands = " ".join(str(x) for x in self.qemu['commands'])
        self.register = "%s %s %s" % (
            self.qemu['register'],
            options,
            commands
        )
        self.images = self.__images__()
        self.commands = []
        
    def __id__(self):
        return uuid.uuid4().hex

    def __qemu__(self, f):
        __qemu__ = open(os.path.join(self.prefix, f), 'r')
        return yaml.load(__qemu__)
        
    def __images__(self):
        images = []
        for j in self.qemu['arches']:
            for i in self.qemu['targets']:
                images.append("%s:%s-%s" % (
                    self.qemu['image'],
                    i,
                    j
                ))

        return images


    def __register__(self, cmd):
        self.commands.append(cmd)
        
    def make(self):
        for cmd in self.commands:
            print "[ exec ] %s" % cmd
            subprocess.call(cmd)

    def build(self):
        # Show configuration
        print "==> loaded configuration:"
        print "    uuid/user:  %s" % self.uuid
        print "    register: %s" % self.register
        print "    base image: %s" % self.qemu['base']
        print "    generated images:"
        for i in self.images:
            print "      - %s" % i
        self.__register__("docker run %s" % self.register)
        self.__register__("mkdir -p %s/%s" % (self.prefix, self.qemu['prefix']))
        self.__register__("touch %s/%s/docker-compose.yml" % (self.prefix, self.qemu['prefix']))
        self.__register__("echo 'version: \"%s\"' >> %s/%s/docker-compose.yml" % (self.qemu['version'], self.prefix, self.qemu['prefix']))
        self.__register__("echo 'services:' >> %s/%s/docker-compose.yml" % (self.prefix, self.qemu['prefix']))
        for t in self.qemu['targets']:
            for a in self.qemu['arches']:
                self.__register__("echo '  %s_%s:' >> %s/%s/docker-compose.yml" % (t, a, self.prefix, self.qemu['prefix']))
                self.__register__("echo '    image: %s:%s-%s' >> %s/%s/docker-compose.yml" % (self.qemu['image'], t, a, self.prefix, self.qemu['prefix']))
                self.__register__("echo '    build:' >> %s/%s/docker-compose.yml" % (self.prefix, self.qemu['prefix']))
                self.__register__("echo '      context: %s/%s/%s/%s' >> %s/%s/docker-compose.yml" % (self.prefix, self.qemu['prefix'], t, a, self.prefix, self.qemu['prefix']))
                self.__register__("echo '      dockerfile: Dockerfile' >> %s/%s/docker-compose.yml" % (self.prefix, self.qemu['prefix']))
                self.__register__("echo '      args:' >> %s/%s/docker-compose.yml" % (self.prefix, self.qemu['prefix']))
                self.__register__("echo '        - \'USER=%s\'' >> %s/%s/docker-compose.yml" % (self.uuid, self.prefix, self.qemu['prefix']))
                self.__register__("mkdir -p %s/%s/%s" % (self.prefix, self.qemu['prefix'], t))
                self.__register__("mkdir -p %s/%s/%s/%s" % (self.prefix, self.qemu['prefix'], t, a))
                self.__register__("touch %s/%s/%s/%s/Dockerfile" % (self.prefix, self.qemu['prefix'], t, a))
                self.__register__("echo 'FROM %s:%s-%s' >> %s/%s/%s/%s/Dockerfile" % (self.qemu['base'], a, t, self.prefix, self.qemu['prefix'], t, a))
                self.__register__("echo 'ARG USER' >> %s/%s/%s/%s/Dockerfile" % (self.prefix, self.qemu['prefix'], t, a))
                self.__register__("echo 'RUN addgroup --gid %s %s' >>  %s/%s/%s/%s/Dockerfile" % (self.gid, self.group, self.prefix, self.qemu['prefix'], t, a))
                self.__register__("echo 'RUN adduser --force-badname --ingroup %s --uid %s --disabled-password --home /home/$USER $USER' >> %s/%s/%s/%s/Dockerfile" % (self.group, self.uid, self.prefix, self.qemu['prefix'], t, a))
                self.__register__("echo 'RUN echo \'%s ALL=(ALL) NOPASSWD: ALL\' > /etc/sudoers' >> %s/%s/%s/%s/Dockerfile" % ('%'+self.group, self.prefix, self.qemu['prefix'], t, a))
                for e in self.qemu['env']:
                    self.__register__("echo '        - \"%s\"' >> %s/%s/docker-compose.yml" % (e, self.prefix, self.qemu['prefix']))
                    self.__register__("echo 'ARG %s' >> %s/%s/%s/%s/Dockerfile" % (e.split("=")[0], self.prefix, self.qemu['prefix'], t, a))
                for __cmd__ in self.qemu['before_install']:
                    self.__register__("echo 'RUN %s' >> %s/%s/%s/%s/Dockerfile" % (__cmd__, self.prefix, self.qemu['prefix'], t, a))
                self.__register__("echo 'USER $USER' >> %s/%s/%s/%s/Dockerfile" % (self.prefix, self.qemu['prefix'], t, a))
                self.__register__("echo 'WORKDIR /home/$USER' >> %s/%s/%s/%s/Dockerfile" % (self.prefix, self.qemu['prefix'], t, a))
                for c in ['install', 'after_install', 'before_script', 'script', 'after_script']:
                    for __cmd__ in self.qemu[c]:
                        self.__register__("echo 'RUN %s' >> %s/%s/%s/%s/Dockerfile" % (__cmd__, self.prefix, self.qemu['prefix'], t, a))

