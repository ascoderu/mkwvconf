mkwvconf
========

.. image:: https://api.travis-ci.org/ascoderu/mkwvconf.svg?branch=master
    :target: https://travis-ci.org/ascoderu/mkwvconf

.. image:: https://img.shields.io/pypi/v/mkwvconf.svg
    :target: https://pypi.org/project/mkwvconf/

Overview
--------

The :code:`mkwvconf.py` program is a tool that automatically generates a
`wvdial <https://linux.die.net/man/1/wvdial>`_ configuration for mobile
broadband devices using the `mobile-broadband-provider-info <https://github.com/GNOME/mobile-broadband-provider-info>`_ package.

This repo is a fork of mkwvconf modified to work on Python 2.7 and later. The
original mkwvconf can be found at `schuay/mkwvconf <https://github.com/schuay/mkwvconf>`_.

Usage
-----

First, install the tool and its system dependency:

.. sourcecode :: bash

    python3 -m pip install mkwvconf
    apt-get install mobile-broadband-provider-info

After installation, you can run tool to guide you through an interactive
setup experience that generates a wvdial configuration file for you:

.. sourcecode :: bash

    mkwvconf.py
