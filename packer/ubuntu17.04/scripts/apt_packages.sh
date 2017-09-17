#!/usr/bin/env bash
# Purpose: Install any user-specified packages beyond the base install.

# attempt to install any additional packages required, if any are specified
if [ -n "$apt_packages" ]; then
    # ensure we have the most recent list of packages
    apt-get update

    # remove any quotes in the string (translation from input configuration)
    apt_packages=${apt_packages//[\',\"]/}

    # install each package
    for package in $apt_packages; do
        apt-get --yes install $package
    done
fi
