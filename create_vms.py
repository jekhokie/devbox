#!/usr/bin/env python
#
# This script is the entry point to creating the developer virtual machine
# instances using Packer. It utilizes the settings defined in the config
# directory to dynamically generate the desired setup and configuration of
# the virtual machine being provisioned.
#
# Note: This script is very loose - there are very few error handlers built
#       into the script, so errors are possible and user experience may be
#       degraded as a result.

from ConfigParser import SafeConfigParser
from subprocess import call, check_call
import shlex

# import the desired configurations
config = SafeConfigParser()
config.read('config/settings.ini')

# construct variables based on the configuration
os_name = config.get('operating_system', 'name')
os_version = config.get('operating_system', 'version')
memory = config.get('hardware', 'memory')
num_cpus = config.get('hardware', 'num_cpus')
packer_dir = "packer/{}{}".format(os_name, os_version)

# run the Packer command to build the VM based on the inputs
packer_command = shlex.split("packer build -var 'memory={}' -var 'num_cpus={}' base_template.json".format(memory, num_cpus))
call(packer_command, cwd=packer_dir)

# next steps if the build succeeded
print '''
##############################################################################
# Your artifact(s) have finished building. You can find them in the          #
# artifacts/ directory with the names shown in the output above. To          #
# use the artifact (i.e. in Vagrant), run the command below:                 #
#                                                                            #
#    vagrant box add --name "packer-ubuntu16" artifacts/<artifact_name>.box  #
#                                                                            #
# Where '<artifact_name>' is the name of the Vagrant box file. You           #
# can then insert the name of your box (i.e. 'packer-ubuntu16') into         #
# your Vagrantfile to use it.                                                #
##############################################################################
'''
