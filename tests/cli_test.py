import os, sys, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'qemu_composer')))

class TestClass(object):

    def test_main_build(self):
        p = os.path.join(os.path.dirname(__file__))
        q = __import__('composer').main(
            prefix=p,
            file='.qemu.yml',
            group='wheel',
            gid=1000,
            uid=1000,
            up=False,
            build=True,
            push=False
        )
        assert q.group is not None
        assert q.gid is not None
        assert q.uid is not None
        assert q.uuid is not None
        assert q.qemu is not None
        assert type(q.commands) is list

    def test_main_up(self):
        q = __import__('composer').main(
            prefix= os.path.dirname(__file__),
            file='.qemu.yml',
            group='wheel',
            gid=1000,
            uid=1000,
            up=True,
            build=False,
            push=False
        )
        assert q.group is not None
        assert q.gid is not None
        assert q.uid is not None
        assert q.uuid is not None
        assert q.qemu is not None
        assert type(q.commands) is list
