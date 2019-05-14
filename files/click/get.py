#!/usr/bin/python3

import gitlab,click,os
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from .. import common


def findSpecificValue(kind, search_result, search_element):
    try:
        for i in search_result:
            if kind == 'user':
                if i.username == search_element:
                    return i
            elif kind == 'group':
                if i.path == search_element:
                    return i

    except:
        common.clickOutputMessage('ERROR', 'red', 'Could not find ' + kind + ' <' + click.style(search_element, fg='yellow') + '> in Gitlab...')


def printParameters(gl_object, parameter, sub_parameter, pretty_print, pretty_sort): # Prints parameters from non-plural 'get' subcommands
    try:
        dict_object = common.transformToDict(gl_object)
    
        if parameter == 'all':
            outputResultsList(False, gl_object, False, pretty_print, pretty_sort, False)
        elif sub_parameter is not None:
            print(dict_object[parameter][sub_parameter])
        else:
            print(dict_object[parameter])

    except Exception as e:
        if not outputParameterError(parameter, sub_parameter, e):
            raise click.ClickException(e)


def outputResultsList(raw, gl_object, specific_value, pretty_print, sort_json, use_path): # Prints different outputs: JSON, colorful value, raw value...
    if sort_json or pretty_print:
        specific_value = False
        pretty_print = True

    if specific_value:
        if use_path == "namespace":
            printable = gl_object.path_with_namespace
        elif use_path == "username":
            printable = gl_object.username
        elif use_path == "path":
            printable = gl_object.path
        else:
            printable = gl_object.name
    else:
        printable = common.transformToDict(gl_object)

    if raw and not pretty_print:
        print(printable)
    elif not specific_value:
        if pretty_print:
            json_object = common.transformToJson(printable)
            common.prettyPrintJson(json_object, sort_json)
        else:
            print(printable)
    else:
        click.echo('[' + click.style(printable, fg='yellow') + ']')


def outputParameterError(parameter, sub_parameter, e): # Function to return failure on parameter retrieval
    if sub_parameter is None:
        sub_parameter = "pl4c3h0ld3r"

    if str("'" + sub_parameter + "'") == str(e):
        common.clickOutputMessage('ERROR', 'red', 'The sub-parameter <' + click.style(sub_parameter, fg='yellow') + '>, along with the parameter <'
                                  + click.style(parameter, fg='yellow') + '> is not an expected parameter or It does not exist for this element.')
        return True

    elif str(e) == str("'" + parameter + "'"):
        common.clickOutputMessage('ERROR', 'red', 'The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter or It does not exist for this element.')
        return True

    else:
        return False


@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def get():
    """Get any element listed in 'Commands' section.

    You can obtain data from Gitlab Projects, Users, Groups, etc...
    Some of the commands have internal options.
    """
    pass


@get.command('projects', short_help="Get all projects in Gitlab")
@click.option('--group', '-g', help="Specific group to search in")
@click.option('--raw', is_flag=True, help="Display results in raw format (just text), not available if using --verbose")
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output, full JSON string")
@click.option('--with-namespace', is_flag=True, help="Show project name in namespace form")
@click.option('--pretty-print', '--pretty', is_flag=True, help="Show JSON beautifully")
@click.option('--pretty-sort', '--sort', '-s', is_flag=True, help="Sort output of pretty-print option")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
def getCommandProjects(group, raw, verbose, with_namespace, pretty_print, pretty_sort, url, token):
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
            if with_namespace:
                output_parameter = "namespace"
            else:
                output_parameter = "placeholder"
            
            outputResultsList(raw, p, not verbose, pretty_print, pretty_sort, output_parameter)

    except Exception as e:
        raise click.ClickException(e)


@get.command('project', short_help="Get exact parameters from project")
@click.option('--project-name', '-p', required=True, help="The project to use")
@click.option('--pretty-print', '--pretty', is_flag=True, help="Show 'all' parameter output as Pretty JSON")
@click.option('--pretty-sort', '--sort', '-s', is_flag=True, help="Sort the --pretty-print JSON output")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('parameter')
@click.argument('sub_parameter', required=False)
def getCommandProject(project_name, pretty_print, pretty_sort, parameter, sub_parameter,  url, token):
    """This subcommand can return a project value depending on parameter. 
    
    Asking for 'all' parameter would output the full JSON of the project!

    Project name must be defined through --project-name option and it has to be in the form of '<group>/<project_path>'
    """

    if not common.validateProjectName(project_name):
        return 1
    
    else:
        gl = common.performConnection(url, token)
        printParameters(gl.projects.get(project_name), parameter, sub_parameter, pretty_print, pretty_sort)


@get.command('branches', short_help='Get all branches inside a Project')
@click.option('--raw', is_flag=True, help="Output branches without color")
@click.option('--verbose', '-v', is_flag=True, help="Output branches JSON object")
@click.option('--pretty-print', '--pretty', is_flag=True, help="Show JSON beautifully")
@click.option('--pretty-sort', '--sort', '-s', is_flag=True, help="Sort output of pretty-print option")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('project_name')
def getCommandBranches(project_name, raw, verbose, pretty_print, pretty_sort, url, token):
    """With this command you can get a list of all branches inside a Project."""
    
    if common.validateProjectName(project_name):
        gl = common.performConnection(url, token)

        try:
            project = gl.projects.get(project_name)
            branches = project.branches.list()
            for b in branches:
                outputResultsList(raw, b, not verbose, pretty_print, pretty_sort, False)
        except Exception as e:
            raise click.ClickException(e)


@get.command('users', short_help='Get registered users')
@click.option('--username', '-u', help="Username to search")
@click.option('--output-username', is_flag=True, help="Output results using username")
@click.option('--raw', is_flag=True, help="")
@click.option('--verbose', '-v', is_flag=True, help="")
@click.option('--pretty-print', '--pretty', is_flag=True, help="Show JSON beautifully")
@click.option('--pretty-sort', '--sort', '-s', is_flag=True, help="Sort output of pretty-print option")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
def getCommandUsers(username, output_username, raw, verbose, pretty_print, pretty_sort, url, token):
    """Simple users list, with some filters"""
    gl = common.performConnection(url, token)

    try:
        users = gl.users.list(username=username)
        for u in users:
            if output_username:
                output_parameter = "username"
            else:
                output_parameter = "placeholder"
                
            outputResultsList(raw, u, not verbose, pretty_print, pretty_sort, output_parameter)

    except Exception as e:
        raise click.ClickException(e)


@get.command('user', short_help='Get an specific user values')
@click.option('--username', '--user', '-u', required=True, help="The user to search with")
@click.option('--pretty-print', '--pretty', is_flag=True, help="Show JSON beautifully")
@click.option('--pretty-sort', '--sort', '-s', is_flag=True, help="Sort output of pretty-print option")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('parameter')
def getCommandUser(username, parameter, pretty_print, pretty_sort, url, token):
    """Get specific values from an user, or even the full JSON output!
    
    To get this full JSON, define the 'all' parameter when calling this subcommand."""
    
    gl = common.performConnection(url, token)
    printParameters(gl.users.list(username=username)[0], parameter, None, pretty_print, pretty_sort)


@get.command('groups', short_help='Get groups created on Gitlab')
@click.option('--group-name', '--group', '-g', help="Groups to search")
@click.option('--get-path', '--path', is_flag=True, help="Return the path parameter instead of the name one")
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output")
@click.option('--raw', is_flag=True, help="Disable style for Pipeline usage")
@click.option('--pretty-print', '--pretty', is_flag=True, help="Show JSON beautifully")
@click.option('--pretty-sort', '--sort', '-s', is_flag=True, help="Sort output of pretty-print option")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
def getCommandGroups(group_name, get_path, verbose, raw, pretty_print, pretty_sort, url, token):
    """Simple groups list"""
    gl = common.performConnection(url, token)

    try:
        if get_path:
            output_parameter = "path"
        else:
            output_parameter = "placeholder"

        if group_name == None:
            groups = gl.groups.list()
            for g in groups:
                outputResultsList(raw, g, not verbose, pretty_print, pretty_sort, output_parameter)
        else:
            groups = gl.groups.get(group_name)
            outputResultsList(raw, groups, not verbose, pretty_print, pretty_sort, output_parameter)

    except Exception as e:
        raise click.ClickException(e)


@get.command('group', short_help='Get specific field from a group')
@click.option('--group-name', '--group', '-g', required=True, help="Group name to search with")
@click.option('--pretty-print', '--pretty', is_flag=True, help="Show JSON beautifully")
@click.option('--pretty-sort', '--sort', '-s', is_flag=True, help="Sort output of pretty-print option")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('parameter')
def getCommandGroup(group_name, parameter, pretty_print, pretty_sort, url, token):
    """Get a specific field from a Group, or even the full JSON output!
    
    To get this full JSON, define the 'all' parameter when calling this subcommand."""
    
    gl = common.performConnection(url, token)
    printParameters(gl.groups.get(group_name), parameter, None, pretty_print, pretty_sort)
