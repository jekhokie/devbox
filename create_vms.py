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

import os
import re
import shlex
import time
from ConfigParser import SafeConfigParser
from config import Config
from subprocess import Popen, PIPE

# capture the build time
build_time = time.strftime("%Y%m%d-%H%M%S")

# import the desired configurations
config = Config(file('config/settings.ini'))

# construct variables based on the configuration
packer_dir = "packer/{}{}".format(config.os_name, config.os_version)

# run the Packer command to build the VM based on the inputs
packer_string = '''
packer build --force -machine-readable
             -var 'apt_packages="{}"'
             -var 'homedir_files={}'
             -var 'memory={}'
             -var 'num_cpus={}'
             base_template.json
'''.format(config.apt_packages, config.homedir_files, config.vm_memory, config.vm_num_cpus)
proc = Popen(shlex.split(packer_string), stdout=PIPE, stderr=PIPE, cwd=packer_dir)

# output to console
stdout = ""
while proc.poll() is None:
    line = proc.stdout.readline()
    stdout += line
    print line

# check to see if something went wrong
if proc.stderr.readline():
    print "Something went wrong with the build - exception captured: {}".format(proc.stderr.readline())
    raise Exception("Build Error")

# attempt to capture the Virtualbox box from the output
vagrant_box_name = "artifacts/<BOX_NAME>"
match_obj = re.search(r'\'virtualbox\' provider box: \.\./\.\./artifacts/(.*)\.box', stdout)
if match_obj:
    vagrant_box_name = match_obj.group(1)
    artifact = "artifacts/{}.box".format(vagrant_box_name)
else:
    print "Could not determine the VirtualBox artifact - please inspect the following output:\n{}".format(stdout)

# build the output directory for vagrant
vagrant_dir = "vagrant/{}".format(build_time)
if not os.path.isdir(vagrant_dir):
    os.makedirs(vagrant_dir)

# output the Vagrantfile
vagrant_template = '''
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "{}"

  config.vm.define "devbox" do |config|
    config.ssh.username = "vagrant"
    config.ssh.password = "vagrant"
    config.vm.hostname  = "devbox.localhost"
    config.vm.network "private_network", ip: "10.11.13.14", netmask: "255.255.255.0"
  end
end
'''.format(vagrant_box_name)

with open("{}/Vagrantfile".format(vagrant_dir), 'w') as vagrant_file:
    vagrant_file.write(vagrant_template)

# import the Vagrant box
vagrant_string = "vagrant box add --name {} {}".format(vagrant_box_name, artifact)
proc = Popen(shlex.split(vagrant_string), stdout=PIPE, stderr=PIPE)

# output to console
while proc.poll() is None:
    print proc.stdout.readline()

# check to see if something went wrong
if proc.stderr.readline():
    print "Something went wrong importing the Vagrant box - exception captured: {}".format(proc.stderr.readline())
    raise Exception("Vagrant Box Import Error")

print '''
###############################################################################################
# Your artifact(s) have finished building. A Vagrant directory has been constructed and a     #
# corresponding Vagrantfile created in the directory here:                                    #
#                                                                                             #
#    {}/Vagrantfile                                                      #
#                                                                                             #
# To utilize this project, perform the following:                                             #
#                                                                                             #
#    cd {}                                                               #
#    # inspect the Vagrantfile - if <VAGRANT_BOX> is defined as the box name, you need to     #
#    # first replace this with the actual box name from the Vagrant box import                #
#    vagrant up devbox                                                                        #
#    vagrant ssh devbox                                                                       #
#                                                                                             #
###############################################################################################
'''.format(vagrant_dir, vagrant_dir)
