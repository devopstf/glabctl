#!/usr/bin/python3


import gitlab,click,os,json,ast
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common


def findSpecificValue(kind, search_result, search_element):
    for i in search_result:
        if kind == 'user':
            if i.username == search_element:
                found_element = i
        elif kind == 'group':
            if i.path == search_element:
                found_element = i
    
    
    try:
        return found_element
    
    except:
        common.clickOutputMessage('ERROR', 'red', 'Could not find ' + kind + ' <' + click.style(search_element, fg='yellow') + '> in Gitlab...')


def outputResultsList(raw, gl_object, get_name, use_path):
    if get_name:
        if use_path:
            printable = gl_object.path_with_namespace
        else:
            printable = gl_object.name
    else:
        printable = gl_object

    if raw:
        print(printable)
    elif not get_name:
        print(str(printable).split(' => ')[1])
    else:
        click.echo('[' + click.style(printable, fg='yellow') + ']')
        

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def get():
    """Get any element listed in 'Commands' section.

    You can obtain data from Gitlab Projects, Users, Groups, etc...
    Some of the commands have internal options.
    """
    pass


@get.command('projects', short_help="Get all projects in Gitlab")
@click.option('--group', '-g', help="Specific group to search in")
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output, full JSON string")
@click.option('--with-namespace', is_flag=True, help="Show project name in namespace form")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.option('--raw', is_flag=True, help="Display results in raw format (just text), not available if using --verbose")
def getCommandProjects(group, raw, verbose, with_namespace, url, token):
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
            outputResultsList(raw, p, not verbose, with_namespace)

    except Exception as e:
        raise click.ClickException(e)

@get.command('project', short_help="Get exact parameters from project")
@click.option('--project-name', '-p', required=True, help="The project to use")
@click.option('--url', required=False, help='URL directing to Gitlab')
@click.option('--token', required=False, help="Private token to access Gitlab")
@click.argument('parameter')
@click.argument('sub_parameter', required=False)
def getCommandProject(project_name, parameter, sub_parameter,  url, token):
    """This subcommand can return a project value depending on parameter.

    Project name must be defined through --project-name option and it has to be in the form of '<group>/<project_path>'

    Available parameters are: 
    
    [all (full JSON), id, namespace, namespace_id, members, description, visibility]
    """

    if not common.validateProjectName(project_name):
        return 1
    
    else:
        try:
            gl = common.performConnection(url, token)
            project = common.transformToDict(gl.projects.get(project_name))

            if parameter == 'all':
                print(project)
                return 0
            elif sub_parameter is not None:
                print(project[parameter][sub_parameter])
            else:
                print(project[parameter])


        except Exception as e:
           raise click.ClickException(e)


@get.command('branches', short_help='Get all branches inside a Project')
@click.option('--raw', is_flag=True, help="")
@click.option('--verbose', '-v', is_flag=True, help="")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('project_name')
def getCommandBranches(project_name, raw, verbose, url, token):
    """With this command you can get a list of all branches inside a Project."""
    
    if common.validateProjectName(project_name):
        gl = common.performConnection(url, token)

        try:
            project = gl.projects.get(project_name)
            branches = project.branches.list()
            for b in branches:
                outputResultsList(raw, b, not verbose, False)
        except Exception as e:
            raise click.ClickException(e)


@get.command('users', short_help='Get registered users')
@click.option('--username', '-u', required=False, help="Username to search")
@click.option('--raw', is_flag=True, help="")
@click.option('--verbose', '-v', is_flag=True, help="")
@click.option('--url', required=False, help="URL directing to Gitlab")
@click.option('--token', required=False, help="Private token to access Gitlab")
def getCommandUsers(username, raw, verbose, url, token):
    """Simple users list, with some filters"""
    gl = common.performConnection(url, token)

    try:
        users = gl.users.list(search=username)
        for u in users:
            outputResultsList(raw, u, not verbose, False)

    except Exception as e:
        raise click.ClickException(e)


@get.command('user', short_help='Get an specific user values')
@click.option('--username', '--user', '-u', required=True, help="The user to search with")
@click.option('--url' ,required=False, help='URL directing to Gitlab')
@click.option('--token', required=False, help="Private token to access Gitlab")
@click.argument('parameter')
def getCommandUser(username, parameter, url, token):
    """Get specific values from an user.

    Parameters could be:

    [all, id, name, email, identities]
    """
    
    gl = common.performConnection(url, token)
    try:
        user = gl.users.list(search=username)
        specific_user = findSpecificValue('user', user, username)
        
        parameter_dict = { 'id': specific_user.id, 'name': specific_user.name }

        # User might not have a public email defined
        if parameter == "email":
            parameter_dict['email'] = specific_user.email
        elif parameter == "identities":
            parameter_dict['identities'] = specific_user.identities

        try:
            if parameter != "all":
                print(parameter_dict[parameter])
            else:
                print(str(specific_user).split(' => ')[1])
        except:
            common.clickOutputMessage('ERROR', 'red', 'The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter')
            return 1
            
    except Exception as e:
        if str(e) == str(parameter):
            common.clickOutputMessage('ERROR', 'red', 'Seems this user does not have the parameter <' + click.style(parameter, fg='yellow') + '> or you do not have the proper permission to see it...')
        else:
            raise click.ClickException(e)

@get.command('groups', short_help='Get groups created on Gitlab')
@click.option('--group-name', '--group', '-g', required=False, help="Groups to search")
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output")
@click.option('--raw', is_flag=True, help="Disable style for Pipeline usage")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def getCommandGroups(group_name, verbose, raw, url, token):
    """Simple groups list"""
    gl = common.performConnection(url, token)

    try:
        if group_name == None:
            groups = gl.groups.list()
        else:
            groups = gl.groups.get(group_name)
            
        for g in groups:
            outputResultsList(raw, g, not verbose, False)

    except Exception as e:
        raise click.ClickException(e)

@get.command('group', short_help='Get specific field from a group')
@click.option('--group-name', '--group', '-g', required=True, help="Group name to search with")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('parameter')
def getCommandGroup(group_name, parameter, url, token):
    """Get a specific field from a Group.
    
    Parameters/fields could be:

    [id, description, visibility, full_name, parent_id, web_url]
    """

    gl = common.performConnection(url, token)

    try:
        group = gl.groups.list(search=group_name)
        specific_group = findSpecificValue('group', group, group_name)

        parameters_dict = { 'id': specific_group.id, 'description': specific_group.description, 'visibility': specific_group.visibility, 
                            'full_name': specific_group.full_name, 'parent_id': specific_group.parent_id, 'web_url': specific_group.web_url }

        try:
            print(parameters_dict[parameter])
        except:
            common.clickOutputMessage('ERROR', 'red', 'The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter')
            return 1

    except Exception as e:
        raise click.ClickException(e)
