# content of test_sysexit.py
import os, sys, pytest, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'qemu_composer')))

__qemuComposer__ = __import__('qemuComposer')
__composer__ = __import__('composer')
__main__ = __import__('__main__')

class TestClass(object):

    def test_import_qemuComposer(self):
        assert __qemuComposer__ is not None

    def test_import_composer(self):
        assert __composer__ is not None

    def test_import_main(self):
        assert __main__ is not None

    def test_QemuComposer_class(self):
        assert __qemuComposer__.QemuComposer is not None
    def test_composer_main_function(self):
        assert __composer__.main is not None  

    def test_main_own_main_function(self):
        assert __main__.main is not None  
