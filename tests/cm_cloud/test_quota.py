""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_quota.py:Test_quota.test_001

nosetests -v --nocapture tests/test_quota.py

or

nosetests -v tests/test_quota.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict


class Test_quota:
    """
        This class tests the QuotaCommand
    """

    data = dotdict({
        "cloud": "kilo",
        "format": "csv",
        "wrong_cloud": "kilo_wrong"
    })

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c ="-")
        print (command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """
        test quota list
        :return:
        """
        HEADING()
        result = self.run("cm quota list")
        assert "Quota" in result

    def test_002(self):
        """
        test quota list with csv output
        :return:
        """
        HEADING()
        result = self.run("cm quota list --cloud={cloud} --format={format}")
        assert "ram" in result

    def test_003(self):
        """
        test quota class where cloud doesnt exist
        :return:
        """
        HEADING()
        result = self.run("cm quota list --cloud={wrong_cloud}")
        assert "is not defined in the yaml file" in result