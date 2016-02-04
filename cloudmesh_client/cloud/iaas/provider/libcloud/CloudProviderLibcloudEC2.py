#def CloudProviderLibCloudEC2()

#   return CloudProviderLibCloud(,,,, libcloudprovider="ec2", ....)


class CloudProviderLibcloudEC2(CloudProviderLibcloud):

    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderLibcloudEC2, self).__init__(cloud_name,cloud_details, user=user)
        self.flat = flat
        self.kind = "libcloud"
        self.cloudname = cloud_name
        self.initialize(cloud_name)

    def initialize(self, cloudname, user=None):

        pprint("Initializing libcloud-ec2 for "+ cloudname)
        cls = get_driver(Provider.EC2_US_EAST)

        d = ConfigDict("cloudmesh.yaml")
        self.cloud_details = d["cloudmesh"]["clouds"][cloudname]
        credentials = self.cloud_details["credentials"]
        auth_url = credentials["EC2_URL"]
        pprint("Auth url is "+ auth_url)
        searchobj = re.match( r'^http[s]?://(.+):([0-9]+)/([a-zA-Z/]*)', auth_url, re.M|re.I)

        if searchobj:
           print "searchObj.group() : ", searchobj.group()
           print "host : ", searchobj.group(1)
           host=searchobj.group(1)
           print "port : ", searchobj.group(2)
           port=searchobj.group(2)
           print "path : ", searchobj.group(3)
           path=searchobj.group(3)
        else:
           print "Nothing found!!"

        # if libcloudname == "ec2" :
        # url_split=auth_url.split("/:")

        ec2_access_key=credentials['EC2_ACCESS_KEY']
        ec2_secret_key=credentials['EC2_SECRET_KEY']
        # ec2_auth_url=

        extra_args= {'path' : path}

        # AWS needs two values for authentication
        self.provider = cls(credentials['EC2_ACCESS_KEY'],
             credentials['EC2_SECRET_KEY'], host='openstack.tacc.chameleoncloud.org', port=port, **extra_args)

