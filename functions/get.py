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
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output")
@click.option('--url', '-u',required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def getCommandProjects(group, url, token, verbose):
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
            click.echo('[' + click.style(p.name, fg='yellow') + ']')
            if verbose:
                print(p)
                print()

    except Exception as e:
        raise click.ClickException(e)

@get.command('project', short_help="Get exact parameters from project")
@click.option('--project-name', '-p', required=True, help="The project to use")
@click.option('--url', '-u',required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('parameter')
def getCommandProject(project_name, parameter, url, token):
    """This subcommand can return a value depending on parameter.

    Available parameters are: 
    
    [id, namespace, namespace_id, members, description, visibility]
    """

    gl = common.performConnection(url, token)

    try:
        project = gl.projects.list(search=project_name)
        project_obj = gl.projects.get(project[0].id)
        
        if parameter == "id":
            print(project[0].id)
        elif parameter == "namespace":
            print(project[0].namespace['name'])
        elif parameter == "namespace_id":
            print(project[0].namespace['id'])
        elif parameter == "members":
            print(project_obj.members.list())
        elif parameter == "description":
            print(project[0].description)
        elif parameter == "visibility":
            print(project[0].visibility)
        else:
            click.echo('[' + click.style('ERROR', fg='red') + '] The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter')

    except Exception as e:
        raise click.ClickException(e)


@get.command('branches', short_help='Get all branches inside a Project')
@click.option('--team', '-t', required=True, default='phG1TL4BCTL', help="Team name to use")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def getCommandBranches(team, url, token, project_name):
    """With this command you can get a list of all branches inside a Project."""
    if(team != "phG1TL4BCTL"):
        gl = common.performConnection(url, token)

        try:
            project_full_name = team + '/' + project_name
            project = gl.projects.get(project_full_name)
            branches = project.branches.list()
            for b in branches:
                print(b)
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
def getCommandUsers(username, url, token):
    """Simple users list, with some filters"""
    gl = common.performConnection(url, token)

    try:
        users = gl.users.list(search=username)
        for u in users:
            print(u)
    except Exception as e:
        raise click.ClickException(e)


@get.command('user', short_help='Get an specific user values')
@click.option('--username', '-u', required=True, help="The user to search with")
@click.option('--url' ,required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('parameter')
def getCommandUser(username, parameter, url, token):
    """Get specific values from an user.

    Parameters could be:

    [id, name, email, identities]
    """
    
    gl = common.performConnection(url, token)

    try:
        user = gl.users.list(search=username)
        
        if parameter == "id":
            print(user[0].id)
        elif parameter == "name":
            print(user[0].name)
        elif parameter == "email":
            print(user[0].email)
        elif parameter == "identities":
            print(user[0].identities)
        else:
            click.echo('[' + click.style('ERROR', fg='red') + '] The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter')

    except Exception as e:
        raise click.ClickException(e)

@get.command('groups', short_help='Get groups created on Gitlab')
@click.option('--groupname', '--name', '-gn', required=False, help="Groups to search")
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output")
@click.option('--no-style', is_flag=True, help="Disable style for Pipeline usage")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def getCommandGroups(groupname, verbose, no_style, url, token):
    """Simple groups list"""
    gl = common.performConnection(url, token)

    try:
        if not groupname:
            groups = gl.groups.list()
            for g in groups:
                if verbose:
                    click.echo('[' + click.style(g.name, fg='yellow') + ']')
                    print(g)
                    print()
                elif no_style:
                    print(g)
                else:
                    click.echo('[' + click.style(g.name, fg='yellow') + ']')
        else:
            groups = gl.groups.get(groupname)
            print(groups)

    except Exception as e:
        raise click.ClickException(e)

@get.command('group', short_help='Get specific field from a group')
@click.option('--groupname', '-g', required=True, help="Group name to search with")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('parameter')
def getCommandGroup(groupname, parameter, url, token):
    """Get a specific field from a Group.
    
    Parameters/fields could be:

    [id, description, visibility, full_name, parent_id, web_url]
    """

    gl = common.performConnection(url, token)

    try:
        group = gl.groups.list(search=groupname)

        if parameter == "id":
            print(group[0].id)
        elif parameter == "description":
            print(group[0].description)
        elif parameter == "visibility":
            print(group[0].visibility)
        elif parameter == "full_name":
            print(group[0].full_name)
        elif parameter == "parent_id":
            print(group[0].parent_id)
        elif parameter == "web_url":
            print(group[0].web_url)
        else:
            click.echo('[' + click.style('ERROR', fg='red') + '] The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter')
            
    except Exception as e:
        raise click.ClickException(e)
