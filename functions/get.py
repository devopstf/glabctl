#!/usr/bin/python

import gitlab,click,os,json
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common

def findSpecificValue(kind, search_result, search_element):
    for i in search_result:
        if kind == 'user':
            if i.username == search_element:
                found_element = i
        elif kind == 'group':
            if i.name == search_element:
                found_element = i
    try:
        return found_element
    except:
        click.echo('[' + click.style('ERROR', fg='red') + '] Could not find ' + kind + '<' + click.style(search_element, fg='yellow') + '> in Gitlab...')


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
    """This subcommand can return a project value depending on parameter.

    Project name must be defined through --project-name option and it has to be in the form of '<group>/<project_name>'

    Available parameters are: 
    
    [id, namespace, namespace_id, members, description, visibility]
    """
    
    if not common.validateProjectName(project_name):
        return 1
    
    else:
        try:
            gl = common.performConnection(url, token)
            project = gl.projects.get(project_name)
            
            parameters_dict = { 'id': project.id, 'namespace': project.namespace['name'], 'namespace_id': project.namespace['id'],
                                'members': project.members.list(), 'description': project.description, 'visibility': project.visibility }
            
            try:
                print(parameters_dict[parameter])
            except:
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
        specific_user = findSpecificValue('user', user, username)

        parameter_dict = { 'id': specific_user.id, 'name': specific_user.name, 'email': specific_user.email, 'identities': specific_user.identities }

        try:
            print(parameter_dict[parameter])
        except:
            click.echo('[' + click.style('ERROR', fg='red') + '] The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter')
            return 1
            
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
        specific_group = findSpecificValue('group', group, groupname)

        parameters_dict = { 'id': specific_group.id, 'description': specific_group.description, 'visibility': specific_group.visibility, 
                            'full_name': specific_group.full_name, 'parent_id': specific_group.parent_id, 'web_url': specific_group.web_url }

        try:
            print(parameters_dict[parameter])
        except:
            click.echo('[' + click.style('ERROR', fg='red') + '] The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter')
            return 1

    except Exception as e:
        raise click.ClickException(e)
