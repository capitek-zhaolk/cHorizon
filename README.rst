=============================
Horizon (OpenStack Dashboard)
=============================

Horizon is a Django-based project aimed at providing a complete OpenStack
Dashboard along with an extensible framework for building new dashboards
from reusable components. The ``openstack_dashboard`` module is a reference
implementation of a Django site that uses the ``horizon`` app to provide
web-based interactions with the various OpenStack projects.

* Release management: https://launchpad.net/horizon
* Blueprints and feature specifications: https://blueprints.launchpad.net/horizon
* Issue tracking: https://bugs.launchpad.net/horizon

.. image:: http://governance.openstack.org/badges/horizon.svg
    :target: http://governance.openstack.org/reference/tags/index.html

Using Horizon
=============

See ``doc/source/topics/install.rst`` about how to install Horizon
in your OpenStack setup. It describes the example steps and
has pointers for more detailed settings and configurations.

It is also available at http://docs.openstack.org/developer/horizon/topics/install.html.

Running Horizon
=============

* Install::

    安装必要软件
    $ apt-get update -y
    $ apt-get upgrade -y
    $ apt-get install git -y
    $ apt-get install gettext -y
    $ apt-get install python-pip -y
    $ pip install --upgrade pip
    $ pip install tox
    获取代码
    # git clone https://github.com/CloudPlatformDev/cHorizon.git -b stable/ocata
    # cd cHorizon
    更新依赖库
    $ pip install -c http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata .
    
* Debugging::

    运行
    $ ./runserver.sh

Getting Started for Developers
==============================

``doc/source/quickstart.rst`` or
http://docs.openstack.org/developer/horizon/quickstart.html
describes how to setup Horizon development environment and start development.

Building Contributor Documentation
==================================

This documentation is written by contributors, for contributors.

The source is maintained in the ``doc/source`` directory using
`reStructuredText`_ and built by `Sphinx`_

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org/

* Building Automatically::

    $ ./run_tests.sh --docs

* Building Manually::

    $ tools/with_venv.sh sphinx-build doc/source doc/build/html

Results are in the ``doc/build/html`` directory
