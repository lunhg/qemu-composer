# content of test_sysexit.py
import os, sys, pytest, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'qemu-composer')))

__module__ = __import__('qemuComposer')

class TestClass(object):

    def test_import(self):
        assert __module__ is not None

    def test_QemuComposer_class(self):
        assert __module__.QemuComposer is not None    
