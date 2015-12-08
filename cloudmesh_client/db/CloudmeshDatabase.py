from __future__ import print_function

import json
import getpass
from pprint import pprint

from sqlalchemy.orm import sessionmaker
from cloudmesh_base.util import banner
from sqlalchemy import inspect
from cloudmesh_base.hostlist import Parameter
from cloudmesh_client.db.model import database, table, tablenames, \
    FLAVOR, DEFAULT, KEY, IMAGE, VM, GROUP, RESERVATION, COUNTER, VMUSERMAP, BATCHJOB
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Username


# noinspection PyBroadException,PyPep8Naming
class CloudmeshDatabase(object):
    def counter_incr(self, name="counter", user=None):

        user = user or Username()
        count = self.counter_get(name=name, user=user)

        count += 1

        self.counter_set(name=name, user=user, value=count)
        self.save()

    def counter_get(self, name="counter", user=None):
        """
        Function that returns the prefix username and count for vm naming.
        If it is not present in db, it creates a new entry.
        :return:
        """
        user = user or Username()

        try:
            count = self.query("COUNTER", name=name, user=user).first().value
        except:
            count = 1
            c = COUNTER(name=name, value=count, user=user)
            self.add(c)

        return count

    def counter_set(self, name=None, value=None, user=None):
        """
        Special function to update vm prefix count.
        :param kwargs:
        :return:
        """
        if type(value) != int:
            raise ValueError("counter must be integer")
        if value is None:
            value = 0

        element = self.find(COUNTER, output="object", name=name, user=user)
        element.first().value = value
        self.save()

    def __init__(self, user=None):
        """
        initializes the CloudmeshDatabase for a specific user.
        The user is used to add entries augmented with it.

        :param user: The username that is used to be added to the
                        objects in teh database
        """

        self.connected = False
        self.db = database()
        self.db.Base.metadata.create_all()
        self.session = self.connect()

        if user is None:
            self.user = getpass.getuser()
        else:
            self.user = user

    def clear(self, kind, cloud):
        """
        This method deletes all 'kind' entries
        from the cloudmesh database
        :param cloud: the cloud name
        """
        try:
            elements = self.find(kind, output='object',
                                 scope="all", cloud=cloud)
            # pprint(elements)
            for element in elements:
                # pprint(element)
                self.delete(element)

        except Exception as ex:
            Console.error(ex.message, ex)

    # noinspection PyUnusedLocal
    def refresh(self, kind, name, **kwargs):
        """
        This method refreshes the local database
        with the live cloud details
        :param kind:
        :param name:
        :param kwargs:
        :return:
        """
        try:
            # print(cloudname)
            # get the user
            # TODO: Confirm user
            user = self.user

            if kind in ["flavor", "image", "vm"]:

                # get provider for specific cloud
                provider = CloudProvider(name).provider

                # clear local db records for kind
                self.clear(kind, name)

                if kind == "flavor":
                    flavors = provider.list_flavor(name)
                    for flavor in flavors.values():
                        flavor["uuid"] = flavor['id']
                        flavor['type'] = 'string'
                        flavor["cloud"] = name
                        flavor["user"] = user

                        db_obj = {0: {kind: flavor}}
                        self.add_obj(db_obj)
                        self.save()
                    return True

                elif kind == "image":
                    images = provider.list_image(name)

                    for image in images.values():
                        image['uuid'] = image['id']
                        image['type'] = 'string'
                        image['cloud'] = name
                        image['user'] = user
                        db_obj = {0: {kind: image}}

                        self.add_obj(db_obj)
                        self.save()
                    return True

                elif kind == "vm":
                    vms = provider.list_vm(name)
                    for vm in vms.values():
                        vm['uuid'] = vm['id']
                        vm['type'] = 'string'
                        vm['cloud'] = name
                        vm['user'] = user
                        db_obj = {0: {kind: vm}}

                        self.add_obj(db_obj)
                        self.save()
                    return True
            elif kind in ["batchjob"]:

                # provider = BatchProvider(name).provider
                # provider = BatchProvider(name)

                from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
                provider = BatchProvider(name)

                vms = provider.list_job(name)
                for vm in vms.values():
                    vm['uuid'] = vm['id']
                    vm['type'] = 'string'
                    vm['cloud'] = name
                    vm['user'] = user
                    db_obj = {0: {kind: vm}}

                    self.add_obj(db_obj)
                    self.save()
                return True

            else:
                Console.error("refresh not supported for this kind: {}".format(kind))

        except Exception as ex:
            Console.error(ex.message)
            return False

    def connect(self):
        """
        before any method is called we need to connect to the database

        :return: the session of the database
        """
        try:
            connected = self.connected
        except:
            connected = False
        if not connected:
            Session = sessionmaker(bind=self.db.engine)
            self.session = Session()
            self.connected = True
        return self.session

    def save(self):
        self.session.commit()
        self.session.flush()

    def close(self):
        self.session.close()

    def db_table(self, kind):
        _type = kind
        if type(kind) == str:
            _type = self.get_table(kind)
        return _type

    def delete(self, item):
        """
        :param item:
        :return:
        """
        self.session.delete(item)
        self.save()

    def delete_all(self, kind):
        """
        :param kind:
        :return:
        """
        self.session.query(kind).delete()
        self.save()

    def get_table(self, kind):
        if type(kind) == str:
            if kind.lower() in ["flavor"]:
                return FLAVOR
            elif kind.lower() in ["default"]:
                return DEFAULT
            elif kind.lower() in ["image"]:
                return IMAGE
            elif kind.lower() in ["vm"]:
                return VM
            elif kind.lower() in ["key"]:
                return KEY
            elif kind.lower() in ["group"]:
                return GROUP
            elif kind.lower() in ["reservation"]:
                return RESERVATION
            elif kind.lower() in ["counter"]:
                return COUNTER
            elif kind.lower() in ["vmusermap"]:
                return VMUSERMAP
            elif kind.lower() in ["batchjob"]:
                return BATCHJOB
            else:
                TODO.implement("wrong table type: `{}`".format(kind))
        else:
            return kind

    def find_by_name(self, kind, **kwargs):
        """
        find an object by name in the given table.
         If multiple objects have the same name, the first one is returned.

        :param name: the name
        :return: the object
        """

        def first(result):
            if len(result) == 0:
                return None
            else:
                return result[result.keys()[0]]

        if 'name' not in kwargs:
            raise ValueError("name not specified in find_by_name")

        table_type = self.get_table(kind)

        result = first(self.find(table_type, **kwargs))
        return result

    def find(self, kind, scope="all", output="dict", **kwargs):
        """
        NOT tested
        :param kind:
        :param kwargs:
        :return:
        """
        # print("KW", kwargs)
        result = self.query(kind, **kwargs)
        # print("LLL", result)
        if output == 'dict' and result is not None:
            result = self.object_to_dict(result)
            if scope == "first":
                if result.keys().__len__() > 0:
                    first = result.keys()[0]
                    result = result[first]
                else:
                    result = None
        # if result == {}:
        #    return None

        return result

    def query(self, kind, **kwargs):
        """
        NOT tested
        :param kind:
        :param kwargs:
        :return:
        """
        # print("AAA")
        table = self.get_table(kind)
        # print(table)

        result = self.session.query(table).filter_by(**kwargs)
        # print("OK")
        # print(result.__dict__)
        return result

    def all(self, table):
        table_type = self.get_table(table)
        elements = self.session.query(table_type).all()
        d = self.parse_objs(elements)
        return d

    def update(self, kind, kwargs):
        """

        :param kind:
        :param kwargs:
        :return:
        """
        self.find(kind, output="object", name=kwargs["name"]).update(kwargs)
        self.save()

    def update_vm_username(self, **kwargs):
        """
        Special function to update vm prefix count.
        :param kwargs:
        :return:
        """
        self.find(VMUSERMAP, output="object", vm_uuid=kwargs["vm_uuid"]).update(kwargs)
        self.save()

    def delete_by_name(self, kind, name):
        """
        NOT TESTED
        :param kind:
        :param name:
        :return:
        """
        item = self.find(kind, name=name, output="item").first()
        self.delete(item)

    def object_to_dict(self, obj):
        """
        convert the object to dict

        :param obj:
        :return:
        """
        result = dict()
        for u in obj:
            _id = u.id
            values = {}
            for key in u.__dict__.keys():
                if not key.startswith("_sa"):
                    values[key] = u.__dict__[key]
            result[_id] = values
        return result

    def parse_objs(self, elements):
        d = {}
        for element in elements:
            d[element.id] = {}
            for key in element.__dict__.keys():
                if not key.startswith("_sa"):
                    d[element.id][key] = str(element.__dict__[key])
        return d

    def dict(self, table):
        """
        returns a dict from all elements in the table

        :param table:
        :return:
        """
        return self.object_to_dict(self.session.query(table).all())

    def json(self, table):
        """
        returns a json representation from all elements in the table

        :param table:
        :return:
        """
        d = self.dict(table)
        return json.dumps(d)

    def info(self, what=None, kind=None):
        """
        prints information about the database
        """
        count_result = {}
        if kind is None:
            kinds = tablenames()
        else:
            kinds = Parameter.expand(kind)
        if what is None:
            infos = "table,count"
        else:
            infos = Parameter.expand(what)

        banner("Databse table information", c="-")
        inspector = inspect(self.db.engine)

        if "table" in infos:
            for table_name in inspector.get_table_names():
                if table_name in kinds:
                    print(table_name + ":")
                    for column in inspector.get_columns(table_name):
                        print("  ", column['name'], column['type'])

        counter = 0
        if "count" in infos:
            for table_name in inspector.get_table_names():
                if table_name in kinds:
                    t = table(table_name)
                    rows = self.session.query(t).count()
                    count_result[table_name] = rows
                    print("Count {:}: {:}".format(table_name, rows))
                    counter = counter + rows
            count_result['sum'] = counter

        return count_result

    def db_obj_dict(self, kind, obj_dict=None, **kwargs):
        """
        This method is a generic method to populate an object dict.
        The object dict can then be passed to database layer to add/ modify
        objects.
        :param dict: Dict to add object to
        :param kind: The table name in the db.
        :param kwargs: object parameters
        :return: Dict with object added
        """
        if obj_dict is None:
            obj_dict = dict()

        dict_length = len(obj_dict)

        obj_dict[dict_length] = dict()
        obj_dict[dict_length][kind] = kwargs

        # print(obj_dict)
        return obj_dict

    def add(self, o):
        self.session.add(o)
        self.session.commit()
        self.session.flush()

    def add_obj(self, obj_dict):
        # print("Inside add_obj")
        # print("Object Dict to add: {}".format(obj_dict))

        for obj in obj_dict.values():
            # print(obj)
            for key in obj.keys():
                table_name = self.get_table(key)
                obj_to_persist = table_name(**obj[key])
                self.add(obj_to_persist)

    def get(self, table, **kwargs):
        return self.session.query(table).filter_by(**kwargs).first()


def main():
    cm = CloudmeshDatabase(user="gregor")

    #    m = DEFAULT("hallo", "world")
    #    m.newfield__hhh = 13.9
    #    cm.add(m)

    #    n = cm.query(DEFAULT).filter_by(name='hallo').first()

    #    print("\n\n")

    #    pprint(n.__dict__)

    #    o = cm.get(DEFAULT, 'hallo')

    #    print("\n\n")

    #    pprint(o.__dict__)

    #    m = DEFAULT("other", "world")
    #    m.other = "ooo"
    #    cm.add(m)

    #    print("\n\n")
    #    pprint(cm.get(DEFAULT, 'other').__dict__)

    cm.info()

    m = COUNTER("counter", 2, user="gregor")
    cm.add(m)

    o = cm.get(COUNTER, name='counter', user="gregor")

    print("\n\n")

    pprint(o.__dict__)

    cm.counter_set(name="counter", user="gregor", value=0)

    for i in range(0, 10):
        cm.counter_incr(name="counter", user="gregor")

    print(cm.counter_get(name="counter", user="gregor"))
    """



    cm.info()
    # print(cm.list(VM))
    """


if __name__ == "__main__":
    main()
