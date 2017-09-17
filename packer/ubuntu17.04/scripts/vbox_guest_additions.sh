#!/usr/bin/env bash
# Purpose: Install the VirtualBox Guest Additions.

# vars
TMP_DIR=/tmp/vbox_guest_additions
ISO=/home/vagrant/VBoxGuestAdditions.iso

# create a temp dir and mount the ISO
mkdir $TMP_DIR
mount -o loop $ISO $TMP_DIR

# run the guest additions installer
sh $TMP_DIR/VBoxLinuxAdditions.run

# clean up
umount $TMP_DIR
rm -rf $TMP_DIR
rm -f $ISO
