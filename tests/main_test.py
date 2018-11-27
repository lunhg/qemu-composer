import os, sys, pytest, subprocess

class TestClass(object):

    def test_main_version(self):
        p = os.path.dirname(__file__)
        __p__ = os.path.join(p, '..', 'qemu_composer', '__main__.py')
        cmd = " ".join([
            "python",
            os.path.abspath(__p__),
            "--version"
        ])
        assert subprocess.call(cmd, shell=True) is 0

    
    def test_main_help(self):
        p = os.path.dirname(__file__)
        __p__ = os.path.join(p, '..', 'qemu_composer', '__main__.py')
        cmd = " ".join([
            "python",
            os.path.abspath(__p__),
            "--help"
        ])
        assert subprocess.call(cmd, shell=True) is 0

    def test_main_build(self):
        p = os.path.dirname(__file__)
        __p__ = os.path.join(p, '..', 'qemu_composer', '__main__.py')
        cmd = " ".join([
            "python",
            os.path.abspath(__p__),
            "--prefix=%s" % p,
            "--file=.qemu.yml",
            "--group=wheel",
            "--gid 1000",
            "--uid 1000",
            "build"
        ])
        assert subprocess.call(cmd, shell=True) is 0

    def test_main_up(self):
        p = os.path.dirname(__file__)
        __p__ = os.path.join(p, '..', 'qemu_composer', '__main__.py') 
        cmd = " ".join([
            "python",
            os.path.abspath(__p__),
            "--prefix %s" % p,
            "--file .qemu.yml",
            "--group wheel",
            "--gid 1000",
            "--uid 1000",
            "up"
        ])
        assert subprocess.call(cmd, shell=True) is 0
