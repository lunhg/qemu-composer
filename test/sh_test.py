import os, pytest, subprocess

class TestClass(object):

    def test_bin(self):
        p = os.path.join(os.path.dirname(__file__), '.bin')
        assert os.path.isdir(p) is True

    
    def test_dockercompose(self):
        p = os.path.join(os.path.dirname(__file__), '.bin', 'docker-compose.yml')
        assert os.path.isfile(p) is True

    
    def test_target(self):
        p = os.path.join(os.path.dirname(__file__), '.bin', 'jessie')
        assert os.path.isdir(p) is True

    
    def test_arch(self):
        p = os.path.join(os.path.dirname(__file__), '.bin', 'jessie', 'arm64')
        assert os.path.isdir(p) is True

    
    def test_Dockerfile(self):
        p = os.path.join(os.path.dirname(__file__), '.bin', 'jessie', 'arm64', 'Dockerfile')
        assert os.path.isfile(p) is True
