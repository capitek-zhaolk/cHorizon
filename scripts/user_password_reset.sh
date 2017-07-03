#!/bin/bash
# args: user, newpassword

if [ x"$1" != x"" ]; then
   USER="$1"
   PASSWORD="capitek"
   if [ x"$2" != x"" ]; then
       PASSWORD="$2"
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
   ## reset user's password
   openstack user set --password $PASSWORD $USER
else
   exit 1
fi

exit 0
