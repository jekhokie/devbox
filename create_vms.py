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
from config import Config
from subprocess import call, check_call
import shlex

# import the desired configurations
config = Config(file('config/settings.ini'))

# construct variables based on the configuration
packer_dir = "packer/{}{}".format(config.os_name, config.os_version)

# run the Packer command to build the VM based on the inputs
packer_string = '''
packer build -var 'apt_packages="{}"'
             -var 'homedir_files={}'
             -var 'memory={}'
             -var 'num_cpus={}'
             base_template.json
'''.format(config.apt_packages, config.homedir_files, config.vm_memory, config.vm_num_cpus)
call(shlex.split(packer_string), cwd=packer_dir)

# next steps if the build succeeded
print '''
###############################################################################################
# Your artifact(s) have finished building. You can find them in the                           #
# artifacts/ directory with the names shown in the output above. To                           #
# use the artifact (i.e. in Vagrant), run the command below:                                  #
#                                                                                             #
#    vagrant box add --name "packer-ubuntu16" artifacts/<artifact_name>.box                   #
#                                                                                             #
# Where '<artifact_name>' is the name of the Vagrant box file. You                            #
# can then insert the name of your box (i.e. 'packer-ubuntu16') into                          #
# your Vagrantfile to use it. Here is a sample Vagrantfile for use once the                   #
# box has been imported for use using the name "packer-ubuntu16", for example:                #
#                                                                                             #
#   -*- mode: ruby -*-                                                                        #
#   vi: set ft=ruby :                                                                         #
#   Vagrant.configure(2) do |config|                                                          #
#       config.vm.box = "packer-ubuntu16"                                                     #
#                                                                                             #
#       config.vm.define "test" do |config|                                                   #
#           config.ssh.username = "vagrant"                                                   #
#           config.ssh.password = "vagrant"                                                   #
#           config.vm.network "private_network", ip: "10.11.13.14", netmask: "255.255.255.0"  #
#       end                                                                                   #
#   end                                                                                       #
#                                                                                             #
###############################################################################################
'''
