#!/bin/bash
# args: user, password, projectprefix, emaildomain

if [ x"$1" != x"" ]; then
   USER="$1"
   PASSWORD="capitek"
   PROJECTPREFIX="capitek"
   EMAILDOMAIN="capitek.com.cn"
   if [ x"$2" != x"" ]; then
       PASSWORD="$2"
   fi
   if [ x"$3" != x"" ]; then
       PROJECTPREFIX="$3"
   fi
   if [ x"$4" != x"" ]; then
       EMAILDOMAIN="$4"
   fi

   # admin token
   export OS_PROJECT_DOMAIN_NAME=Default
   export OS_USER_DOMAIN_NAME=Default
   export OS_PROJECT_NAME=admin
   export OS_USERNAME=admin
   export OS_PASSWORD=password_to_change
   export OS_AUTH_URL=http://controller:35357/v3
   export OS_IDENTITY_API_VERSION=3
   export OS_IMAGE_API_VERSION=2
   ## create project and user
   openstack project create --domain default --description "$PROJECTPREFIX Project Member" "$PROJECTPREFIX:$USER"
   openstack user create --domain default --description "$PROJECTPREFIX User Member" --project "$PROJECTPREFIX:$USER" --password $PASSWORD --email "$USER@$EMAILDOMAIN" $USER
   openstack role add --project "$PROJECTPREFIX:$USER" --user $USER user

   # user token
   export OS_PROJECT_NAME="$PROJECTPREFIX:$USER"
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
