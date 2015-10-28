from __future__ import print_function

import os
import os.path
import json

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.cloud.register import CloudRegister
from cloudmesh_base.tables import row_table
from cloudmesh_client.common.tables import attribute_printer, dict_printer


class RegisterCommand(object):

    topics = {"register": "cloud"}

    def __init__(self, context):
        # super(self.__class__, self).__init__()
        self.context = context
        if self.context.debug:
            print("init command register")

    @command
    def do_register(self, args, arguments):
        """
        ::

          Usage:
              register info
              register list [--yaml=FILENAME] [--name]
              register list ssh
              register cat [--yaml=FILENAME]
              register edit [--yaml=FILENAME]
              register export HOST [--password] [--format=FORMAT]
              register rc HOST FILENAME [--force] [--format=FORMAT]
              register merge FILEPATH
              register form [--yaml=FILENAME]
              register check [--yaml=FILENAME]
              register test [--yaml=FILENAME]
              register json HOST
              register remote CLOUD [--force]
              register india [--force]
              register CLOUD CERT [--force]
              register CLOUD --dir=DIR
              register env [--provider=PROVIDER]

          managing the registered clouds in the cloudmesh.yaml file.
          It looks for it in the current directory, and than in
          ~/.cloudmesh.  If the file with the cloudmesh.yaml name is
          there it will use it.  If neither location has one a new
          file will be created in ~/.cloudmesh/cloudmesh.yaml. Some
          defaults will be provided.  However you will still need to
          fill it out with valid entries.

          Arguments:

            HOST   the host name
            USER   the user name
            FILEPATH the path of the file
            CLOUD the cloud name
            CERT the path of the certificate
            PROVIDER the provider or type of cloud [Default: openstack]

          Options:

            --provider=PROVIDER     Provider to be used for cloud. Values are:
                                    openstack, azure, ec2.
            --version=VERSION       Version of the openstack cloud.
            --openrc=OPENRC         The location of the openrc file
            --password              Prints the password

          Description:

              register info
                  It looks out for the cloudmesh.yaml file in the current
                  directory, and then in ~/.cloudmesh

              register list [--yaml=FILENAME]
                  lists the clouds specified in the cloudmesh.yaml file

              register list ssh
                  lists hosts from ~/.ssh/config

              register cat [--yaml=FILENAME]
                  outputs the cloudmesh.yaml file

              register edit [--yaml=FILENAME]
                  edits the cloudmesh.yaml file

              register export HOST [--format=FORMAT]

                    prints the contents of an openrc.sh file based on the
                    information found in the cloudmesh.yaml file.

              register rc HOST FILENAME [--force] [--format=FORMAT]

                    reads from an rc file the data and adds to the
                    cloudmesh.yaml file. If --force is used the existing
                    previous entry will be overwritten with default TBD values.

              register remote CLOUD [--force]

                    reads the Openstack OPENRC file from a remote host that
                    is described in cloudmesh.yaml file. We assume that
                    the file has already a template for this host. If
                    not it can be created from other examples before
                    you run this command.

                    It uses the OS_OPENRC variable to locate the file and
                    copy it onto your computer.

              register merge FILENAME
                  Replaces the TBD in cloudmesh.yaml with the contents
                  present in the named file

              register form [--yaml=FILENAME]
                  interactively fills out the form wherever we find TBD.

              register check [--yaml=FILENAME]
                  checks the yaml file for completness

              register test [--yaml=FILENAME]
                  checks the yaml file and executes tests to check if
                  we can use the cloud. TODO: maybe this should be in
                  a test command

              register json host
                  displays the host details in json format

              register remote CLOUD
                  registers a remote cloud and copies the openrc file
                  specified in the credentials of the cloudmesh.yaml

              register india [--force]
                  copies the cloudmesh/clouds/india/juno directory from india
                  to the ~/.cloudmesh/clouds/india/juno local directory

              register CLOUD CERT [--force]
                  Copies the CERT to the ~/.cloudmesh/clouds/host directory
                  and registers that cert in the coudmesh.yaml file.
                  For india, CERT will be in
                  india:.cloudmesh/clouds/india/juno/cacert.pem
                  and would be copied to ~/.cloudmesh/clouds/india/juno

              register CLOUD --dir
                  Copies the entire directory from the cloud and puts it in
                  ~/.cloudmesh/clouds/host
                  For india, The directory would be copied to
                  ~/.cloudmesh/clouds/india

              register env [--provider=PROVIDER] [HOSTNAME]
                  Reads env OS_* variables and registers a new cloud in yaml,
                  interactively. Default PROVIDER is openstack and HOSTNAME
                  is localhost.
         """
        # from pprint import pprint
        # pprint(arguments)

        def _get_file(arguments):
            if arguments["--yaml"]:
                filename = Config.find_file(arguments["--yaml"])
            else:
                filename = Config.find_file("cloudmesh.yaml")
            return filename

        if arguments["info"]:
            try:
                filename = _get_file(arguments)
                if os.path.isfile(filename):
                    Console.ok('File ' + filename + " exists")
            except:
                Console.error("File cloudmesh.yaml does not exist")
            return

        elif arguments["cat"]:
            filename = _get_file(arguments)
            if not filename:
                Console.error("File {} doesn't exist".format(arguments["--yaml"] or 'cloudmesh.yaml'))
            else:
                os.system("cat {:}".format(filename))
            return

        elif arguments["edit"]:
            filename = _get_file(arguments)
            if not filename:
                Console.error("File {} doesn't exist".format(arguments["--yaml"] or 'cloudmesh.yaml'))
            else:
                Console.ok("editing file " + filename)
                os.system("vim {}".format(filename))
            return

        elif arguments['list'] and arguments['ssh']:
            CloudRegister.list_ssh()
            return

        elif arguments['list']:
            filename = _get_file(arguments)
            if not filename:
                Console.error("File {} doesn't exist".format(arguments["--yaml"] or 'cloudmesh.yaml'))
            else:
                if(arguments['--name']):
                   print(CloudRegister.list(filename).get_string(fields=["Name"]))
                else:
                    print(CloudRegister.list(filename))
            return

        elif arguments['check']:
            filename = _get_file(arguments)
            if not filename:
                Console.error("File {} doesn't exist".format(arguments["--yaml"] or 'cloudmesh.yaml'))
            else:
                CloudRegister.check_yaml_for_completeness(filename)
            return

        elif arguments['merge']:
            file_path = arguments['FILENAME']
            CloudRegister.from_file(file_path)
            return

        elif arguments['test']:
            filename = _get_file(arguments)
            CloudRegister.test(filename)
            return

        elif arguments['form']:
            filename = _get_file(arguments)
            if not filename:
                Console.error("File {} doesn't exist".format(arguments["--yaml"] or 'cloudmesh.yaml'))
            else:
                CloudRegister.fill_out_form(filename)
            return

        elif arguments['export']:

            output = arguments['--format']
            host = arguments['HOST']

            config = ConfigDict("cloudmesh.yaml")
            credentials = dict(config["cloudmesh"]["clouds"][host]["credentials"])

            if not arguments["--password"]:
                credentials["OS_PASSWORD"] = "********"

            if output is None:
                for attribute, value in credentials.iteritems():
                    print ("export {}={}".format(attribute, value))
            elif output == "table":
                print(attribute_printer(credentials))
            else:
                print (dict_printer(credentials,output=output))
                # TODO: bug csv does not work
            return

        elif arguments['rc']:
            host = arguments['HOST']
            openrc = arguments['FILENAME']
            force = arguments['--force'] or False

            result = CloudRegister.read_rc_file(host, openrc, force)
            credentials = dict(result)

            # output password as requested by user
            if not arguments["--password"]:
                credentials["OS_PASSWORD"] = "********"
            print(row_table(credentials, order=None, labels=["Variable", "Value"]))
            return

        elif arguments['json']:
            host = arguments['HOST']
            result = CloudRegister.get(host)
            if result:
                print(json.dumps(result, indent=4))
            else:
                print("Cloud {:} is not described in cloudmesh.yaml".format(host))
            return

        elif arguments['remote']:

            force = arguments['--force']
            cloud = arguments['CLOUD']
            CloudRegister.remote(cloud, force)
            return


        elif arguments['CLOUD']:
            if arguments['CERT']:  # path to the cacert.pem
                cloud = arguments['CLOUD']
                path = arguments['CERT']
                force = False
                if arguments['--force']:
                    force = True
                CloudRegister.certificate(cloud, path, force)
            elif arguments['--dir']:
                cloud = arguments['CLOUD']
                dir = arguments['--dir']
                Console.ok(dir)
                CloudRegister.directory(cloud, dir)
        elif arguments['env']:
            try:
                CloudRegister.register_from_env(arguments['--provider'])
            except Exception, e:
                import traceback
                print(traceback.format_exc())
                print (e)
            return

        # if all fails do a simple list

        filename = _get_file(arguments)
        CloudRegister.list(filename)

        pass


if __name__ == '__main__':
    command = cm_shell_register()
    command.do_register("list")
