import os, pytest, subprocess

__prefix__ = os.path.dirname(__file__)
__bin__ = os.path.join(__prefix__, '.bin')
__docker__ = os.path.join(__bin__, 'docker-compose.yml')
__jessie__ = os.path.join(__bin__, 'jessie')

class TestClass(object):

    def test_bin(self):
        p = os.path.abspath(__bin__)
        assert os.path.isdir(p) is True

    
    def test_dockercompose(self):
        p = os.path.abspath(__docker__)
        assert os.path.isfile(p) is True

    
    def test_target(self):
        p = os.path.abspath(__jessie__)
        assert os.path.isdir(p) is True

    
    def test_arch_arm64(self):
        __p__ = os.path.join(__jessie__, 'arm64')
        p = os.path.abspath(__p__)
        assert os.path.isdir(p) is True

    
    def test_arch_armel(self):
        __p__ = os.path.join(__jessie__, 'armel')
        p = os.path.abspath(__p__)
        assert os.path.isdir(p) is True

    
    def test_arch_armhf(self):
        __p__ = os.path.join(__jessie__, 'armhf')
        p = os.path.abspath(__p__)
        assert os.path.isdir(p) is True

    
    def test_Dockerfile_arm64(self):
        __p__ = os.path.join(__jessie__, 'arm64', 'Dockerfile')
        p = os.path.abspath(__p__)
        assert os.path.isfile(p) is True

    
    def test_Dockerfile_armel(self):
        __p__ = os.path.join(__jessie__, 'armel', 'Dockerfile')
        p = os.path.abspath(__p__)
        assert os.path.isfile(p) is True

    
    def test_Dockerfile_armhf(self):
        __p__ = os.path.join(__jessie__, 'armhf', 'Dockerfile')
        p = os.path.abspath(__p__)
        assert os.path.isfile(p) is True
