
import os, sys, uuid, yaml, subprocess
from qav.questions import Question
from qav.validators import ListValidator

class QemuComposer(object):

    def __init__(self, **kwargs):
        self.group = kwargs.get('group')
        self.gid = kwargs.get('gid')
        self.uid = kwargs.get('uid')
        self.prefix = kwargs.get('prefix')
        self.qemu = self.__qemu__(kwargs.get('file'))
        self.uuid = self.__id__()
        self.build = kwargs.get('build')
        self.up = kwargs.get('up') 
        self.push = kwargs.get('push')
        options = " ".join(str(x) for x in self.qemu['options'])
        commands = " ".join(str(x) for x in self.qemu['commands'])
        
        self.register = self.__own_register__(options, commands)
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


    def __own_register__(self, options, commands):
         self.register = "%s %s %s" % (
             options,
             self.qemu['register'],
             commands
         )

    def __register__(self, cmd):
        self.commands.append(cmd)

    def __qa__(self, q):
        q = Question(q, 'answer', ListValidator(['y', 'n']))
        q.ask()
        return q.answer()

    def __createDir__(self):
        t = (self.prefix, self.qemu['prefix'])
        for e in [
            ["rm", "-rf", "%s/%s" % t],
            ["mkdir", "-p", "%s/%s" % t]
        ]:
            self.__register__(e)

    
    def __build__(self):
        self.__register__([
            "docker",
            "run",
            "%s" % self.register
        ])
        self.__register__([
            "touch",
            "%s/%s/docker-compose.yml" % (self.prefix, self.qemu['prefix'])
        ])
        self.__register__([
            "echo",
            "'version: \"%s\"'" % self.qemu['version'],
            ">>",
            "%s/%s/docker-compose.yml" % (
                self.prefix,
                self.qemu['prefix']
            )
        ])
        self.__register__([
            "echo",
            "'services:'",
            ">>",
            "%s/%s/docker-compose.yml" % (
                self.prefix,
                self.qemu['prefix']
            )
        ])
        for t in self.qemu['targets']:
            for a in self.qemu['arches']:
                self.__register__([
                    "echo",
                    '  %s_%s:' % (t, a),
                    ">>",
                    "%s/%s/docker-compose.yml" % (
                        self.prefix,
                        self.qemu['prefix']
                    )
                ])
                self.__register__([
                    "echo",
                    "'    image: %s:%s-%s'" % (
                        self.qemu['image'],
                        t,
                        a
                    ),
                    ">>",
                    "%s/%s/docker-compose.yml" % (
                        self.prefix,
                        self.qemu['prefix']
                    )
                ])
                self.__register__([
                    "echo",
                    "'    build:'",
                    ">>",
                    "%s/%s/docker-compose.yml" % (
                        self.prefix,
                        self.qemu['prefix']
                    )
                ])
                self.__register__([
                    "echo",
                    "'      context: %s/%s/%s/%s'" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    ),
                    ">>",
                    "%s/%s/docker-compose.yml" % (
                        self.prefix,
                        self.qemu['prefix']
                    )
                ])
                self.__register__([
                    "echo",
                    "'      dockerfile: Dockerfile'",
                    ">>",
                    "%s/%s/docker-compose.yml" % (
                        self.prefix,
                        self.qemu['prefix']
                    )
                ])
                self.__register__([
                    "echo",
                    "'      args:'",
                    ">>",
                    "%s/%s/docker-compose.yml" % (
                        self.prefix,
                        self.qemu['prefix']
                    )
                ])
                self.__register__([
                    "echo",
                    "'        - \"USER=%s\"'" % self.uuid,
                    ">>",
                    "%s/%s/docker-compose.yml" % (
                        self.prefix,
                        self.qemu['prefix']
                    )
                ])

                self.__register__([
                    "mkdir",
                    "-p",
                    "%s/%s/%s" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t
                    )
                ])
                self.__register__([
                    "mkdir",
                    "-p",
                    "%s/%s/%s/%s" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                self.__register__([
                    "touch",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                self.__register__([
                    "echo",
                    "'FROM %s:%s-%s'" % (
                        self.qemu['base'],
                        a,
                        t
                    ),
                    ">>",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                self.__register__([
                    "echo",
                    "'ARG USER'",
                    ">>",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                self.__register__([
                    "echo",
                    "'RUN addgroup --gid %s %s'" %(
                        self.gid,
                        self.group
                    ),
                    ">>",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                self.__register__([
                    "echo",
                    "'RUN adduser --force-badname --ingroup %s --uid %s --disabled-password --home /home/$USER $USER'" % (
                        self.group,
                        self.uid
                    ),
                    ">>",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                self.__register__([
                    "echo",
                    "'RUN echo \"%s ALL=(ALL) NOPASSWD: ALL\" > /etc/sudoers'" % '%'+self.group,
                    ">>",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                for e in self.qemu['env']:
                    self.__register__([
                        "echo",
                        "'        - \"%s\"'" % e,
                        ">>",
                        "%s/%s/docker-compose.yml" % (
                            self.prefix,
                            self.qemu['prefix']
                        )
                    ])
                    self.__register__([
                        "echo",
                        "'ARG %s'" % e.split("=")[0],
                        ">>",
                        "%s/%s/%s/%s/Dockerfile" % (
                            self.prefix,
                            self.qemu['prefix'],
                            t,
                            a
                        )
                    ])
                for __cmd__ in self.qemu['before_install']:
                    self.__register__([
                        "echo",
                        "'RUN %s'" % __cmd__,
                        ">>",
                        "%s/%s/%s/%s/Dockerfile" % (
                            self.prefix,
                            self.qemu['prefix'],
                            t,
                            a
                        )
                    ])
                self.__register__([
                    "echo",
                    "'USER $USER'",
                    ">>",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                self.__register__([
                    "echo",
                    "'WORKDIR /home/$USER'",
                    ">>",
                    "%s/%s/%s/%s/Dockerfile" % (
                        self.prefix,
                        self.qemu['prefix'],
                        t,
                        a
                    )
                ])
                for c in ['install', 'after_install', 'before_script', 'script', 'after_script']:
                    for __cmd__ in self.qemu[c]:
                        self.__register__([
                            "echo",
                            "'RUN %s'" % __cmd__,
                            ">>",
                            "%s/%s/%s/%s/Dockerfile" % (
                                self.prefix,
                                self.qemu['prefix'],
                                t,
                                a
                            )
                        ])

        if (self.build or self.up or self.push):
            self.__register__([
                "docker-compose",
                "--project-path",
                "%s/%s" % (self.prefix, self.qemu['prefix']),
                "up -d --build" if self.up and not self.build else ("build -d" if self.build and not self.up else ("push" if self.push and not self.up and not self.build else "images"))
            ])

    def make(self):
        self.__createDir__()
        self.__build__()
        for cmd in self.commands:
            print("[ exec ] %s" % cmd)
            subprocess.call(cmd)
