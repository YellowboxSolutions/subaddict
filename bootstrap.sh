#!/usr/bin/env bash

sudo yum -y install epel-release
sudo yum -y install ansible
ansible-playbook -i "localhost, " -c local /vagrant/ansible/site.yml
