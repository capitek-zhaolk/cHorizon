apt-get install git python-dev python-virtualenv libssl-dev libffi-dev -y
apt-get install python-pip -y
apt-get install gettext -y
apt install libmysqlclient-dev -y
apt install libpq-dev postgresql-common -y
apt install libnss3-dev -y
apt install libldap2-dev -y
apt install liberasurecode-dev -y
apt install libsasl2-dev -y
apt install pkg-config -y
apt install libvirt-dev -y

pip install --upgrade pip
pip install tox
# pip install -c http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata .
# pip install -c requirements.txt .
