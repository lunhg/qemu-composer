import os, sys, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'qemu-composer')))

class TestClass(object):

    def test_main(self):
        self.q = __import__('composer').main(
            prefix= os.path.dirname(__file__),
            file='.qemu.yml',
            group='wheel',
            gid=1000,
            uid=1000
        )
        assert self.q.group is not None
        assert self.q.gid is not None
        assert self.q.uid is not None
        assert self.q.uuid is not None
        assert self.q.qemu is not None
        assert type(self.q.commands) is list
