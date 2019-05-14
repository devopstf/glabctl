#!/usr/bin/python3

import gitlab,click,os
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from ..classes import GitlabCTL as glabctl
from .. import common


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
    gl = glabctl.GitlabCTL(url, token)
    gl.getProjects(group, raw, verbose, with_namespace, pretty_print, pretty_sort)


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
    gl = glabctl.GitlabCTL(url, token)
    gl.getProject(project_name, pretty_print, pretty_sort, parameter, sub_parameter)


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
    
    gl = glabctl.GitlabCTL(url,token)
    gl.getBranches(project_name, raw, verbose, pretty_print, pretty_sort)


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
    
    gl = glabctl.GitlabCTL(url,token)
    gl.getUsers(username, output_username, raw, verbose, pretty_print, pretty_sort)

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
    
    gl = glabctl.GitlabCTL(url, token)
    gl.getUser(username, parameter, pretty_print, pretty_sort)


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

    gl = glabctl.GitlabCTL(url, token)
    gl.getGroups(group_name, get_path, verbose, raw, pretty_print, pretty_sort)


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
    
    gl = glabctl.GitlabCTL(url, token)
    gl.getGroup(group_name, parameter, pretty_print, pretty_sort)
