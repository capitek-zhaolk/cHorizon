
##########################################################################################################
apt-get update -y
apt-get upgrade -y
apt-get install git -y
apt-get install gettext -y
apt-get install python-pip -y

pip install --upgrade pip
pip install tox

##########################################################################################################
git clone https://github.com/linfengplus/horizon.git -b stable/ocata
cd horizon

pip install -c http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata .
