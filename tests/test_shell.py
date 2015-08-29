""" run with

python setup.py install; nosetests -v --nocapture  tests/test_shell.py:Test_shell.test_001

nosetests -v --nocapture tests/test_shell.py

or

nosetests -v tests/test_vm.py

"""
from __future__ import print_function
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result

class Test_shell():
    """

    """


    def setup(self):
        pass



    def test_001(self):
        """
        check if we can run help
        :return:
        """
        HEADING()
        r = run("cm help")
        print(r)
        assert "Documented commands" in r

        assert "bar" in r
        assert "help" in r
        assert "EOF" in r
        assert "q" in r
        assert "quit" in r
