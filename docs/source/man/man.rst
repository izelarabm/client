Commands
======================================================================
banner
----------------------------------------------------------------------

Command - banner::

    Usage:
        banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT

    Arguments:
        TEXT   The text message from which to create the banner
        CHAR   The character for the frame.
        WIDTH  Width of the banner
        INDENT indentation of the banner
        COLOR  the color

    Options:
        -c CHAR   The character for the frame. [default: #]
        -n WIDTH  The width of the banner. [default: 70]
        -i INDENT  The width of the banner. [default: 0]
        -r COLOR  The color of the banner. [default: BLACK]

    Prints a banner form a one line text message.


clear
----------------------------------------------------------------------

Command - clear::

    Usage:
        clear

    Clears the screen.

cloud
----------------------------------------------------------------------

Command - cloud::

    Usage:
        cloud list [--format=FORMAT]
        cloud activate CLOUD
        cloud deactivate CLOUD
        cloud info CLOUD

    managing the admins test test test test

    Arguments:
      KEY    the name of the admin
      VALUE  the value to set the key to

    Options:
       --cloud=CLOUD    the name of the cloud [default: general]
       --format=FORMAT  the output format [default: table]

    Description:
       Cloudmesh contains a cloudmesh.yaml file that contains
       templates for multiple clouds that you may or may not have
       access to. Hence it is useful to activate and deacivate clouds
       you like to use in other commands.

       To activate a cloud a user can simply use the activate
       command followed by the name of the cloud to be
       activated. To find out which clouds are available you can
       use the list command that will provide you with some
       basic information. As default it will print a table. Thus
       the commands       cloud activate india
         cloud deactivate aws

       Will result in

          +----------------------+--------+-------------------+
          | Cloud name           | Active | Type              |
          +----------------------+--------+-------------------+
          | india                | True   | Openstack         |
          +----------------------+--------+-------------------+
          | aws                  | False  | AWS               |
          +----------------------+--------+-------------------+

       To get ore information about the cloud you can use the command

          cloud info CLOUD

       It will call internally also the command uses in register

    See also:
       register


context
----------------------------------------------------------------------

Command - context::

    Usage:
        context

    Description:
        Lists the context variables and their values


default
----------------------------------------------------------------------

Command - default::

                      Usage:
                  default list [--format=FORMAT]
                  default delete KEY [--cloud=CLOUD]
                  default KEY [--cloud=CLOUD]
                  default KEY=VALUE [--cloud=CLOUD]


              managing the defaults test test test test

              Arguments:

                KEY    the name of the default
                VALUE  the value to set the key to

              Options:

                 --cloud=CLOUD    the name of the cloud [default: general]
                 --format=FORMAT  the output format [default: table]

            Description:

                Cloudmesh has the ability to manage easily multiple
                clouds. One of the key concepts to make the usage of such
                clouds easier is the introduction of defaults for each
                cloud or globally. Hence it is possible to set default
                images, flavors for each cloud, but also the default
                cloud. The default command is used to set and list the
                default values. These defaults are used in other commands
                if they are not overwritten by a command parameter.

    	    The current default values can by listed with:(if you have
    	    a default cloud specified. You can also add a
    	    --cloud=CLOUD parameter to apply the command to a specific
    	    cloud)

    	    	default list

                A default can be set with

                     default KEY=VALUE

                 To look up a default value you can say

                      default KEY

                   A deafult can be deleted with

                       default delete KEY



EOF
----------------------------------------------------------------------

Command - EOF::

    Usage:
        EOF

    Description:
        Command to the shell to terminate reading a script.


group
----------------------------------------------------------------------

Command - group::

    Usage:
        group info [--cloud=CLOUD] [--format=FORMAT] NAME
        group add [--name=NAME] [--type=TYPE] [--cloud=CLOUD] --id=IDs
        group list [--cloud=CLOUD] [--format=FORMAT]
        group delete [--cloud=CLOUD] [--name=NAME]
        group copy FROM TO
        group merge GROUPA GROUPB MERGEDGROUP

    manage the groups

    Arguments:

        NAME         name of a group
        FROM         name of a group
        TO           name of a group
        GROUPA       name of a group
        GROUPB       name of a group
        MERGEDGROUP  name of a group

    Options:
        --cloud=CLOUD    the name of the cloud
        --format=FORMAT  the output format
        --type=TYPE     the resource type
        --name=NAME      the name of the group


    Description:

        Todo: design parameters that are useful and match
        description
        Todo: discuss and propose command

        cloudmesh can manage groups of resources and cloud related
        objects. As it would be cumbersome to for example delete
        many virtual machines or delete VMs that are in the same
        group, but are running in different clouds.

        Hence it is possible to add a virtual machine to a
        specific group. The group name to be added to can be set
        as a default. This way all subsequent commands use this
        default group. It can also be set via a command parameter.
        Another convenience function is that the group command can
        use the last used virtual machine. If a vm is started it
        will be automatically added to the default group if it is set.

        The delete command has an optional cloud parameter so that
        deletion of vms of a partial group by cloud can be
        achieved.

        If finer grained deletion is needed, it can be achieved
        with the delete command that supports deletion by name

    Example:
        default group mygroup

        group add --type=vm --id=gregor-[001-003]
            adds the vms with teh given name using the Parameter
            see base

        group add --type=vm
         adds the last vm to the group

        group delete --name=mygroup
            deletes all objects in the group


help
----------------------------------------------------------------------

Command - help::

    Usage:
        help
        help COMMAND

    Description:
        List available commands with "help" or detailed help with
        "help COMMAND".

inventory
----------------------------------------------------------------------

Command - inventory::

    Usage:
        inventory add NAMES [--label=LABEL]
                            [--service=SERVICES]
                            [--project=PROJECT]
                            [--owners=OWNERS]
                            [--comment=COMMENT]
                            [--cluster=CLUSTER]
                            [--ip=IP]
        inventory set NAMES for ATTRIBUTE to VALUES
        inventory delete NAMES
        inventory clone NAMES from SOURCE
        inventory list [NAMES] [--format=FORMAT] [--columns=COLUMNS]
        inventory info

    Arguments:

      NAMES     Name of the resources (example i[10-20])

      FORMAT    The format of the output is either txt,
                yaml, dict, table [default: table].

      OWNERS    a comma separated list of owners for this resource

      LABEL     a unique label for this resource

      SERVICE   a string that identifies the service

      PROJECT   a string that identifies the project

      SOURCE    a single host name to clone from

      COMMENT   a comment

    Options:

       -v       verbose mode

    Description:

          add -- adds a resource to the resource inventory

          list -- lists the resources in the given format

          delete -- deletes objects from the table

          clone -- copies the content of an existing object
                   and creates new once with it

          set   -- sets for the specified objects the attribute
                   to the given value or values. If multiple values
                   are used the values are assigned to the and
                   objects in order. See examples

          map   -- allows to set attibutes on a set of objects
                   with a set of values

    Examples:

      cm inventory add x[0-3] --service=openstack

          adds hosts x0, x1, x2, x3 and puts the string
          openstack into the service column

      cm lists

          lists the repository

      cm x[3-4] set temperature to 32

          sets for the resources x3, x4 the value of the
          temperature to 32

      cm x[7-8] set ip 128.0.0.[0-1]

          sets the value of x7 to 128.0.0.0
          sets the value of x8 to 128.0.0.1

      cm clone x[5-6] from x3

          clones the values for x5, x6 from x3



key
----------------------------------------------------------------------

Command - key::

    Usage:
      key  -h | --help
      key list [--source=db] [--format=FORMAT]
      key list --source=cloudmesh [--format=FORMAT]
      key list --source=ssh [--dir=DIR] [--format=FORMAT]
      key list --source=git [--format=FORMAT] [--username=USERNAME]
      key add --git [--name=KEYNAME] FILENAME
      key add --ssh [--name=KEYNAME]
      key add [--name=KEYNAME] FILENAME
      key get NAME
      key default [KEYNAME | --select]
      key delete (KEYNAME | --select | --all) [-f]

    Manages the keys

    Arguments:

      SOURCE         db, ssh, all
      KEYNAME        The name of a key
      FORMAT         The format of the output (table, json, yaml)
      FILENAME       The filename with full path in which the key
                     is located

    Options:

       --dir=DIR            the directory with keys [default: ~/.ssh]
       --format=FORMAT      the format of the output [default: table]
       --source=SOURCE      the source for the keys [default: db]
       --username=USERNAME  the source for the keys [default: none]
       --name=KEYNAME       The name of a key
       --all                delete all keys

    Description:

    key list --source=git  [--username=USERNAME]

       lists all keys in git for the specified user. If the
       name is not specified it is read from cloudmesh.yaml

    key list --source=ssh  [--dir=DIR] [--format=FORMAT]

       lists all keys in the directory. If the directory is not
       specified the default will be ~/.ssh

    key list --source=cloudmesh  [--dir=DIR] [--format=FORMAT]

       lists all keys in cloudmesh.yaml file in the specified directory.
        dir is by default ~/.cloudmesh

    key list [--format=FORMAT]

        list the keys in teh giiven format: json, yaml,
        table. table is default

    key list

         Prints list of keys. NAME of the key can be specified


    key add [--name=keyname] FILENAME

        adds the key specifid by the filename to the key
        database


    key default [NAME]

         Used to set a key from the key-list as the default key
         if NAME is given. Otherwise print the current default
         key

    key delete NAME

         deletes a key. In yaml mode it can delete only key that
         are not saved in the database

    key rename NAME NEW

         renames the key from NAME to NEW.



man
----------------------------------------------------------------------

Command - man::

    Usage:
           man COMMAND
           man [--noheader]

    Options:
           --norule   no rst header

    Arguments:
           COMMAND   the command to be printed

    Description:
        man
            Prints out the help pages

        man COMMAND
            Prints out the help page for a specific command


nova
----------------------------------------------------------------------

Command - nova::

    Usage:
           nova set CLOUD
           nova info [CLOUD] [--password]
           nova help
           nova ARGUMENTS...

    A simple wrapper for the openstack nova command

    Arguments:

      ARGUMENTS      The arguments passed to nova
      help           Prints the nova manual
      set            reads the information from the current cloud
                     and updates the environment variables if
                     the cloud is an openstack cloud
      info           the environment values for OS

    Options:
       --password    Prints the password
       -v            verbose mode



open
----------------------------------------------------------------------

Command - open::

    Usage:
            open FILENAME

    ARGUMENTS:
        FILENAME  the file to open in the cwd if . is
                  specified. If file in in cwd
                  you must specify it with ./FILENAME

    Opens the given URL in a browser window.


pause
----------------------------------------------------------------------

Command - pause::

    Usage:
        pause [MESSAGE]

    Displays the specified text then waits for the user to press RETURN.

    Arguments:
       MESSAGE  message to be displayed


q
----------------------------------------------------------------------

Command - q::

    Usage:
        quit

    Description:
        Action to be performed whne quit is typed


quit
----------------------------------------------------------------------

Command - quit::

    Usage:
        quit

    Description:
        Action to be performed whne quit is typed


register
----------------------------------------------------------------------

Command - register::

    Usage:
        register info
        register list [--yaml=FILENAME]
        register list ssh
        register cat [--yaml=FILENAME]
        register edit [--yaml=FILENAME]
        register rc HOST [OPENRC]
        register merge FILEPATH
        register form [--yaml=FILENAME]
        register check [--yaml=FILENAME]
        register test [--yaml=FILENAME]
        register json HOST
        register india [--force]
        register CLOUD CERT [--force]
        register CLOUD --dir=DIR

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
      OPENRC  the location of the openrc file
      FILEPATH the path of the file
      CLOUD the cloud name
      CERT the path of the certificate


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

        register rc HOST [OPENRC]

              reads the Openstack OPENRC file from a host that
              is described in ./ssh/config and adds it to the
              configuration cloudmesh.yaml file. We assume that
              the file has already a template for this host. If
              not it can be created from other examples before
              you run this command.

              The hostname can be specified as follows in the
              ./ssh/config file.

              Host india
                  Hostname india.futuresystems.org
                  User yourusername

              If the host is india and the OPENRC file is
              ommitted, it will automatically fill out the
              location for the openrc file. To obtain the
              information from india simply type in

                  register rc india

        register merge FILEPATH
            Replaces the TBD in cloudmesh.yaml with the contents
            present in FILEPATH's FILE

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

        register india [--force]
            copies the cloudmesh/clouds/india/juno directory from india
            to the ~/.cloudmesh/clouds/india/juno local directory

        register CLOUD CERT [--force]
            Copies the CERT to the ~/.cloudmesh/clouds/host directory
            and registers that cert in the coudmesh.yaml file.
            For india, CERT will be in india:.cloudmesh/clouds/india/juno/cacert.pem
            and would be copied to ~/.cloudmesh/clouds/india/juno

        register CLOUD --dir
            Copies the entire directory from the cloud and puts it in
            ~/.cloudmesh/clouds/host
            For india, The directory would be copied to ~/.cloudmesh/clouds/india


reservation
----------------------------------------------------------------------

Command - reservation::

    Usage:
        reservation info [--user=USER]
                         [--project=PROJECT]
        reservation list [--name=NAME]
                         [--user=USER]
                         [--project=PROJECT]
                         [--hosts=HOSTS]
                         [--start=TIME_START]
                         [--end=TIME_END]
                         [--hosts=HOSTS]
                         [--format=FORMAT]
        reservation delete [all]
                           [--user=USER]
                           [--project=PROJECT]
                           [--name=NAME]
                           [--hosts=HOSTS]
                           [--start=TIME_START]
                           [--end=TIME_END]
                           [--host=HOST]
        reservation delete --file=FILE
        reservation update [--name=NAME]
                           [--hosts=HOSTS]
                           [--start=TIME_START]
                           [--end=TIME_END]
        reservation add [--user=USER]
                        [--project=PROJECT]
                        [--hosts=HOSTS]
                        [--description=DESCRIPTION]
                        --name=NAMES
                        --start=TIME_START
                        --end=TIME_END
        reservation add --file=FILE

    Options:
        --name=NAMEs          Names of the reservation
        --user=USER           user name
        --project=PROJECT     project id
        --start=TIME_START    Start time of the reservation, in
                              YYYY/MM/DD HH:MM:SS format. [default: 1901-01-01]
        --end=TIME_END        End time of the reservation, in
                              YYYY/MM/DD HH:MM:SS format. In addition a duration
                              can be specified if the + sign is the first sign.
                              The duration will than be added to
                              the start time. [default: 2100-12-31]
        --host=HOST           host name
        --description=DESCRIPTION  description summary of the reservation
        --file=FILE           Adding multiple reservations from one file
        --format=FORMAT       Format is either table, json, yaml or csv
                              [default: table]

    Description:

        reservation info
            lists the resources that support reservation for
            a given user or project.


secgroup
----------------------------------------------------------------------

Command - secgroup::

    Usage:
        secgroup list [--cloud=CLOUD] [--tenant=TENANT]
        secgroup create [--cloud=CLOUD] [--tenant=TENANT] LABEL
        secgroup delete [--cloud=CLOUD] [--tenant=TENANT] LABEL
        secgroup rules-list [--cloud=CLOUD] [--tenant=TENANT] LABEL
        secgroup rules-add [--cloud=CLOUD] [--tenant=TENANT] LABEL FROMPORT TOPORT PROTOCOL CIDR
        secgroup rules-delete [--cloud=CLOUD] [--tenant=TENANT] LABEL FROMPORT TOPORT PROTOCOL CIDR
        secgroup -h | --help
        secgroup --version

    Options:
        -h                  help message
        --cloud=CLOUD       Name of the IaaS cloud e.g. india_openstack_grizzly.
        --tenant=TENANT     Name of the tenant, e.g. fg82.

    Arguments:
        LABEL         The label/name of the security group
        FROMPORT      Staring port of the rule, e.g. 22
        TOPORT        Ending port of the rule, e.g. 22
        PROTOCOL      Protocol applied, e.g. TCP,UDP,ICMP
        CIDR          IP address range in CIDR format, e.g., 129.79.0.0/16

    Description:
        security_group command provides list/add/delete
        security_groups for a tenant of a cloud, as well as
        list/add/delete of rules for a security group from a
        specified cloud and tenant.


    Examples:
        $ secgroup list --cloud india --tenant fg82
        $ secgroup rules-list --cloud india --tenant fg82 default
        $ secgroup create --cloud india --tenant fg82 webservice
        $ secgroup rules-add --cloud india --tenant fg82 webservice 8080 8088 TCP "129.79.0.0/16"



select
----------------------------------------------------------------------

Command - select::

    Usage:
        select image [CLOUD]
        select flavor [CLOUD]
        select cloud [CLOUD]
        select key [CLOUD]

    selects interactively the default values

    Arguments:

      CLOUD    the name of the cloud

    Options:



server
----------------------------------------------------------------------

Command - server::

    Usage:
        server

    Options:
      -h --help
      -v       verbose mode

    Description:
      Starts up a REST service and a WEB GUI so one can browse the data in an
      existing cloudmesh database.

      The location of the database is supposed to be in

        ~/.cloud,esh/cloudmesh.db



ssh
----------------------------------------------------------------------

Command - ssh::

    Usage:
        ssh list [--format=FORMAT]
        ssh register NAME PARAMETERS
        ssh ARGUMENTS


    conducts a ssh login on a machine while using a set of
    registered machines specified in ~/.ssh/config

    Arguments:

      NAME        Name or ip of the machine to log in
      list        Lists the machines that are registered and
                  the commands to login to them
      PARAMETERS  Register te resource and add the given
                  parameters to the ssh config file.  if the
                  resoource exists, it will be overwritten. The
                  information will be written in /.ssh/config

    Options:

       -v       verbose mode
       --format=FORMAT   the format in which this list is given
                         formats incluse table, json, yaml, dict
                         [default: table]

       --user=USER       overwrites the username that is
                         specified in ~/.ssh/config

       --key=KEY         The keyname as defined in the key list
                         or a location that contains a pblic key



version
----------------------------------------------------------------------

Command - version::

    Usage:
       version [--format=FORMAT] [--check=CHECK]

    Options:
        --format=FORMAT  the format to print the versions in [default: table]
        --check=CHECK    boolean tp conduct an additional check [default: True]

    Description:
        Prints out the version number
