""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_group.py:Test_group.test_001

nosetests -v --nocapture tests/test_group.py

or

nosetests -v tests/test_group.py

"""
from __future__ import print_function
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
from cloudmesh_client.util import banner

from cloudmesh_client.cloud.group import Group
from pprint import pprint
from cloudmesh_client.default import Default
from cloudmesh_client.common.dotdict import dotdict

class Test_group:
    data = dotdict({
        "cloud": Default.get_cloud(),
        "user": "test",
        "group": "groupA"
    })

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        HEADING("testing cm group add ")

        c = "cm group add {user}-001 --group={group}  --type=vm"
        self.run(c)

        id = str(Group.get(name="groupA"))
        print(id)
        assert "test-001" in id
        return

    def test_002(self):
        HEADING("testing cm group add")

        command = "cm group add {user}-002 --group={group}   --type=vm"
        self.run(command)

        group = Group.get(name="groupA")

        names = ["{user}-001".format(**self.data),
                 "{user}-002".format(**self.data)]
        for id in group:
            element = group[id]
            assert element["name"] == "groupA"
            assert element["type"] == "vm"
            assert element["member"] in names
        return

    def test_003(self):
        HEADING("testing cm group copy groupA groupB")

        command = "cm group copy {group} groupB"

        result = self.run(command)
        assert "groupB" in result

        return

    def test_004(self):
        HEADING("testing cm group merge groupA groupB groupC")
        command = "cm group merge {group} groupB groupC"

        result = self.run(command)
        assert "ok." in result
        return

    def test_005(self):
        HEADING("testing cm group list  groupA")
        command = "cm group list  {group}"

        result = self.run(command)
        assert "groupA" in result
        return

    def test_006(self):
        HEADING("testing cm group list  --format json groupA")
        command = "cm group list  --format=json {group}"

        result = self.run(command)
        assert "groupA" in result
        return

    def test_007(self):
        HEADING("testing cm group list  --format table")
        command = "cm group list  --format=table"

        result = self.run(command)
        assert "groupA" in result
        return

    def test_008(self):
        HEADING("testing cm group add with default cloud")
        banner("cm group add --name=groupX --id=albert-00x", c='-')


        result = self.run("cm default cloud")
        pprint(self.data)
        assert self.data.cloud in result

        result = self.run("cm default type=vm")
        assert "ok." in result

        result = self.run("cm group add albert-00x --group=groupX ")
        assert "albert-00x" in result

        result = self.run("cm group list  groupX")
        assert self.data.cloud in result
        assert "vm" in result

        return

    def test_009(self):
        HEADING("testing cm group remove ")
        banner("cm group remove {user}-002  --group={group}")

        result = self.run("cm group remove {user}-002  --group={group} ")
        print(result)
        assert "ok" in result

        result = self.run("cm group list {group}")
        assert "test-002" not in result

        return

    def test_010(self):
        HEADING("testing cm group delete ")

        command = "cm group delete {group} "
        result = self.run(command)
        print(result)


        for group in ["groupA", "groupB", "groupC", "groupX"]:
            self.data.group = group
        command = "cm group delete {group} "

        result = self.run(command)

        assert "ok." in result

        return

    def test_011(self):

        HEADING("list vms in group")

        setup = [
            "cm group add vm_1 --group=group_x",
            "cm group add vm_2 --group=group_x",
            "cm group add vm_3 --group=group_y",
            "cm group add vm_3 --group=group_x",
            "cm group list"]

        for command in setup:
            self.run(command)

        result = Group.get_vms_in_group("group_x")
        pprint(result)
        assert 'vm_1' in result
        assert 'vm_2' in result
        assert 'vm_3' in result

        result = Group.get_vms_in_group("group_y")
        pprint(result)
        assert 'vm_3' in result
        assert 'vm_1' not in result
        assert 'vm_2' not in result

        result = Group.names()
        pprint(result)
        assert 'group_x' in result
        assert 'group_y' in result

        result = Group.vm_groups("vm_1")
        pprint(result)
        assert 'group_x' in result
        assert 'group_y' not in result

        result = Group.vm_groups("vm_3")
        pprint(result)
        assert 'group_x' in result
        assert 'group_y' in result

        result = Group.delete("group_x")
        print(result)
        result = self.run("cm group list")

        assert 'vm_1' not in result
        assert 'vm_2' not in result

        self.run("cm group list")

        for command in setup:
            self.run(command)

        result = Group.delete("group_y")

        print(result)
        result = self.run("cm group list")

        assert 'group_y' not in result
        assert 'vm_3' in result

        return

    def test_012(self):
        HEADING("list non existing group")
        command = "cm group list DOESNOTEXIST"
        result = self.run(command)

        assert "ERROR" in result
