#!/usr/bin/env bash
# Purpose: Add passwordless sudo ability for the vagrant user.

sed -i -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
