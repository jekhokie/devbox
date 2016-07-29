#!/usr/bin/env bash
# Purpose: Inject any home directory contents desired from a GitHub repo.

# clone the repository containing the home directory files
git clone $homedir_files /home/vagrant/homedir

# remove the repository contents
rm -rf /home/vagrant/homedir/.git

# move all files, including dot files, into the home directory
shopt -s dotglob
mv /home/vagrant/homedir/* /home/vagrant/

# clean up the existing repository
rm -rf /home/vagrant/homedir

# remove any git ignore file in case there was one in the repo
rm /home/vagrant/.gitignore
