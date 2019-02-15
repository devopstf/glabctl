<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/GitLab_Logo.svg/1108px-GitLab_Logo.svg.png" width="180"><img src="https://files.realpython.com/media/python-logo.8eb72ea6927b.png" width="200"></p><p></p><p></p>

# python-gitlab-scraper
A Python script to scrape Gitlab API and interact with it. Might help If you need to control the different Gitlab elements creation through a pipeline in an automated way. 

With this, you won't need to ``curl`` to a messed up URL for automated Gitlab management (i.e Create a project branch dinamically because a business petition needs so due to the need of develop a new application feature).

This project is still in development, made in first place to practice Python scripting, so don't expect much!

## Pre-requisites
This scraper works in Python, and until there's an alternative way to execute it, you'll need Python installed in your host!

### Python installation
You can do so by executing the following shell command using **apt-get** package manager:
``apt-get install python``
Or If you're using **yum** instead:
``yum install python``

### Make installation
This tool comes with a Makefile. To make use of Its functions, you'll need to have **make** installed on your host. To do so, simply execute the following command.

Using **apt-get**:
``apt-get install make``
Or **yum**:
``yum install make``

### Pip installation
This tool comes with some dependencies, as it uses [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/install.html) and [Click](https://click.palletsprojects.com/en/7.x/) (as well as [click_help_colors](https://github.com/r-m-n/click-help-colors) libraries to build the CLI & access Gitlab. To install them, the easiest way is using Pip, which you can install using the following commands.

Using **apt-get**:
``apt-get install python3-pip``
Or **yum**:
``yum install python-pip``

## Installation
Once all pre-requisites are cleared, you can begin the installation! Before we begin, you should decide in which directory to install the tool. We recommend **/opt**, as It's the common one to use, but you can decide one that fits your needs!

To install everything, It's as simple as executing the following make commands inside the directory:
1. ``make resolve-dependencies``
2. ``make install``

Once you've executed both commands, you should be able to execute ``gitlabctl --help`` and get a result!

## Configuration
Once installed, you should configure the tool. You can do so by defining these environment variables on your host:
- ``GITLABCTL_URL``: which is the URL where your Gitlab installation is located
- ``GITLABCTL_TOKEN``: which is the private token of the user you want to use

If you don't want to define environment variables on your system, you can also append the flags ``--host`` and ``--token`` in each of the tool's sub-commands (which are ``get`` and ``create``, and below them the ones pointing to the different actions).

You have the info on how to use those flags in the ``--help`` documentation of each sub-command, although!
