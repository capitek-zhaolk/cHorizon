#!/bin/bash
if [ x"$1" != x"" ]; then
   USER="$1"
   PASSWORD="capitek"
   if [ x"$2" != x"" ]; then
       PASSWORD="$2"
   fi

   # admin token
   openstack project create --domain default --description "Capitek Member Project" "capitek:$USER"
   openstack user create --domain default --project "capitek:$USER" --password $PASSWORD --email "$1@capitek.com.cn"  $USER
   openstack role add --project "capitek:$USER" --user $USER user

   # user token
   export OS_PROJECT_NAME="capitek:$USER"
   export OS_USERNAME=$USER
   export OS_PASSWORD=$PASSWORD
   ## update default security group
   openstack security group list
   openstack security group rule list
   openstack security group rule create --proto icmp default
   openstack security group rule create --proto tcp --dst-port 1:65535 default
   openstack security group rule create --proto udp --dst-port 1:65535 default
   openstack security group rule list
else
   exit 1
fi

exit 0
