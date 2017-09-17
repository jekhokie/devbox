# Devbox

Auto-provisioning and configuration of personalized virtual machines to support development.

## CAUTION

**MAKE SURE THAT YOU TURN OFF ALL ANTIVIRUS SCANNING SOFTWARE, SUCH AS KASPERSKY, PRIOR TO RUNNING
THE `create_vm.py` SCRIPT - FAILURE TO DO SO WILL LIKELY RESULT IN AN INVALID BOOT COMMAND BEING
TYPED (YOU WILL LIKELY SEE DUPLICATE CHARACTERS BEING SENT TO THE SCREEN DUE TO KEY-UP DELAYS).**

## Background

This project is slightly theoretical in nature. Although I do actually use it for provisioning
myself new developer VMs, it is very limited in nature and was formed as more of a way to
demonstrate capabilities of the Packer tool and supporting infrastructure.

As a developer, I am constantly developing and testing on various platforms, operating
systems, etc. The primary use case I have is to instantiate a brand new VM using Vagrant
to do development and testing using a clean operating system. Each time I provision a new
VM, however, I am inclined to scp/copy/install/etc. all of the dependencies related to
my preferred development environment, including but not limited to:

* vim
  * Highlighting
  * Syntax Completion
  * Editor controls/status bar
  * Git integration
  * Folder/file explorer
* git
  * Shortcuts
  * Default configuration settings
* Custom Bash Scripts
  * Auto-completion scripts
* bashrc, bash_profile
  * Environment variables
  * Aliases
  * Default settings
* tmux
  * Shortcut settings
  * Default configurations
* screen
  * Shortcut settings
  * Default configurations
* RVM
* etc.

As seen, it is cumbersome to re-initialize all of the above each time I stand up a
new development VM and/or receive a new laptop.

## Purpose

This project aims to abstract away the various tasks I perform to create a new development
environment for myself each and every time I feel like the current environment is getting
to be too cluttered and/or introducing potential dependencies from other projects that
may impact the integrity of testing related to the current project being worked on.

## Technologies

The following technologies are used/assumed in this project - these are the tools I use
most frequently, but the framework abstracts the infrastructure enough such that I could
add the ability to deploy/configure a new devbox in AWS, Azure, etc.

* Packer (https://www.packer.io/docs/)
* Vagrant (https://www.vagrantup.com/)
* VirtualBox (https://www.virtualbox.org/)

## Installation / Usage

To utilize this project to create new development VMs catered to your preferences, perform
the following steps. Note that the code was developed and has been tested on the following
platforms - it may work on other platforms, but there are no guarantees at this time:

Mac OS X - El Capitan

### Prerequisites

Make sure the following software and tools are installed and/or available (other versions may
function as expected, but have not been tested, so your mileage may vary):

* Python 2.7.x+
* Packer 1.1.0+
* VirtualBox 5.1.28+
* Vagrant 2.0.0+

### Code

Obtain the project code from GitHub and initialize your Python environment:

```bash
$ git clone https://github.com/jekhokie/devbox.git
$ cd devbox
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

### Configuration

Customize the configuration for your environment:

```bash
$ cp config/settings.ini.sample config/settings.ini
# edit the configuration in config/settings.ini for your environment
```

### Build Customized VM

**WARNING**: PLEASE REFER TO THE WARNING AT THE BEGINNING OF THIS ARTICLE AND ENSURE ANY/ALL VIRUS
SCANNING SOFTWARE IS DISABLED PRIOR TO RUNNING THE FOLLOWING COMMANDS. FAILURE TO DO SO WILL LIKELY
RESULT IN DUPLICATE CHARACTERS BEING SENT TO THE VM FROM PACKER DURING THE BOOT SEQUENCE.

Once your configuration is in place, run the script to stand up your new developer VM:

```bash
$ python create_vms.py
```

Note that the above will take some time to complete - in addition, you will likely see a graphical
interface corresponding to the new VirtualBox image being created, which is expected.

Once everything completes, you should have a fully-provisioned Vagrant developer environment ready
for use. You should receive some text at the end of the provisioning instructing next steps, which
will indicate how to initiate a VM using the Packer image created.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
