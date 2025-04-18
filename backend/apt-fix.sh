#!/bin/bash
set -e

# Fetch updated keys
apt-get update -y
apt-get install -y --no-install-recommends gnupg curl ca-certificates
apt-get clean
rm -rf /var/lib/apt/lists/*

# Add Debian keys from a trusted source
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0E98404D386FA1D9 6ED0E7B82643E131 54404762BBB6E853

# Update and proceed with installation
apt-get update -y
apt-get install -y --no-install-recommends build-essential curl git
apt-get clean
rm -rf /var/lib/apt/lists/*