#!/usr/bin/python

import gitlab,click,os
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def get():
    """Get any element listed in 'Commands' section.

    You can obtain data from Gitlab Projects, Users, Groups, etc...
    Some of the commands have internal options.
    """
    pass


@get.command('projects', short_help="Get all projects in Gitlab")
@click.option('--group', '-g', required=False, help="Specific group to search in")
@click.option('--url', '-u',required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def projects(group, url, token):
    """A subcommand to list all projects in Gitlab

    You can filter by Gitlab group using the corresponding option!
    """
    gl = common.performConnection(url, token)

    try:
        if group:
            search_group = gl.groups.get(group)
            projects = search_group.projects.list()
        else:
            projects = gl.projects.list()
        for p in projects:
            print(p)
    except Exception as e:
        raise click.ClickException(e)


@get.command('branches', short_help='Get all branches inside a Project')
@click.option('--team', '-t', required=True, default='phG1TL4BCTL', help="Team name to use")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def branches(team, url, token, project_name):
    """With this command you can get a list of all branches inside a Project."""
    if(team != "phG1TL4BCTL"):
        gl = common.performConnection(url, token)

        try:
            project_full_name = team + '/' + project_name
            project = gl.projects.get(project_full_name)
            branches = project.branches.list()
            for b in branches:
                print(b.name)
        except Exception as e:
            raise click.ClickException(e)
    else:
        print("ERROR: You didn't specify --team flag, which is required...")
        print("-----------------------------------------------------------")
        os.system('gitlabctl get branches --help')


@get.command('users', short_help='Get registered users')
@click.option('--username', '--name', '-n', required=False, help="Username to search")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def users(username, url, token):
    """Simple users list, with some filters"""
    gl = common.performConnection(url, token)

    try:
        users = gl.users.list(search=username)
        for u in users:
            print(u)
    except Exception as e:
        raise click.ClickException(e)


@get.command('groups', short_help='Get groups created on Gitlab')
@click.option('--groupname', '--name', '-gn', required=False, help="Username to search")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def groups(groupname, url, token):
    """Simple groups list"""
    gl = common.performConnection(url, token)

    try:
        if not groupname:
            groups = gl.groups.list()
            for g in groups:
                print(g)
        else:
            groups = gl.groups.get(groupname)
            print(groups)

    except Exception as e:
        raise click.ClickException(e)
