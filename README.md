<p align="center"><img src="https://i.imgur.com/lhmy9yN.png"></p><p></p><p></p>


# GLABCTL - A Gitlab API Scraper 
A Python script to scrape Gitlab API and interact with it. Might help If you need to control the different Gitlab elements creation through a pipeline in an automated way. 

With this, you won't need to ``curl`` to a messed up URL for automated Gitlab management (i.e Create a project branch dinamically because a business petition needs so due to the need of develop a new application feature).

This project is still in development, made in first place to practice Python scripting, so don't expect much!


# Usage example

[![asciicast](https://asciinema.org/a/kbTUTcwSSJQT4rSPGfMYxlylZ.svg)](https://asciinema.org/a/kbTUTcwSSJQT4rSPGfMYxlylZ)

# Pre-requisites
This section only applies If you're not using ``glabctl``.

This scraper works in Python, and until there's an alternative way to execute it, you'll need Python installed in your host!


### Python installation
You can do so by executing the following shell command using **apt-get** package manager:
``apt-get install python3``
Or If you're using **yum** instead:
``yum install python3``


### Make installation
This tool comes with a Makefile. You'll need to have **make** installed on your host. To do so, simply execute the following command.

Using **apt-get**:
``apt-get install make``
Or **yum**:
``yum install make``
Or **apk**:
``apk add make``


### Pip installation
This tool comes with some dependencies, as it uses [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/install.html) and [Click](https://click.palletsprojects.com/en/7.x/) (as well as [click_help_colors](https://github.com/r-m-n/click-help-colors)) libraries to build the CLI & access Gitlab. To install them, the easiest way is using Pip, which you can install using the following commands.

Using **apt-get**:
``apt-get install python3-pip``
Or **yum**:
``yum install python3-pip``
Or **apk**: 
``apk add py-pip``


# Installation
Once all pre-requisites are cleared, you can begin the installation! Before we begin, you should decide in which directory to install the tool. We recommend **/opt**, as It's the common one to use, but you can decide one that fits your needs!

To install everything, It's as simple as executing the following make commands inside the directory:
1. ``make resolve-dependencies``
2. ``make install``

If **you don't have permission or don't want to use 'root' user explicitly**, try using ``sudo`` instead. Take in consideration that you'll need to execute them in the following form:
1. ``sudo su -c "make resolve-dependencies"``
2. ``sudo su -c "make install"`` 


### Using Docker
In case you want to use this pgcli as a [Docker](https://www.docker.com) container because you don't want to install Python in your host machine, you can install it using the following ``make`` command:

1. ``make install-docker``

You might **need** to execute this as an administrator. In that case, use this:

1. ``sudo su -c "make install-docker"``

This will generate an image based on the Dockerfile located under the project's ``docker`` folder. This image is based on [Alpine](https://alpinelinux.org) for the sake of not using much disk space for this solution. An additional bash script to execute this image correctly as a Docker container will be linked in */usr/local/bin* so you can only call ``glabctl`` and nothing more!

Currently, you only need ``112MB`` disk space for using pgcli!


# Help documentation
Once you've installed this scraper, you should be able to execute ``glabctl --help`` and get a result!

The ``--help`` option will guide you through the different subcommand this scraper has and should be all you need to use it properly.

[![asciicast](https://asciinema.org/a/Vr48OdxiBlOigmVNMBbz16CL8.svg)](https://asciinema.org/a/Vr48OdxiBlOigmVNMBbz16CL8)


# Configuration
The ``glabctl`` Gitlab scraper needs you to point to a Gitlab server, as well as to specify a way to connect to it. 

You can do so by defining these environment variables on your host:
- ``GLABCTL_URL``: which is the URL where your Gitlab installation is located
- ``GLABCTL_TOKEN``: which is the private token of the user you want to use

If you don't want to define environment variables on your system, you can also append the flags ``--url`` and ``--token`` in each of the tool's sub-commands.

You have the info on how to use those flags in the ``--help`` documentation of each sub-command, although!
