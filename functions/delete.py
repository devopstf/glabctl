#!/usr/bin/python3

import gitlab,click,os,json
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common

def deleteGitlabElement(kind, gitlab_object, auto_confirm, project_name = '', branch_name = '', tag_name = '', user_id = '', group_id = ''):
    user_name = group_name = ''
    
    if 'project' in kind or 'branch' in kind or 'tag' in kind:
        element = gitlab_object.projects.get(project_name)
    elif user_id != '': 
        user_name = gitlab_object.users.get(user_id).username
    elif group_id != '':
        group_name = gitlab_object.groups.get(group_id).name

    print_dictionary = {'project': { 'object_to_delete': project_name, 'delete_from': 'Gitlab' },
                        'branch': { 'object_to_delete': branch_name, 'delete_from': project_name },
                        'tag': { 'object_to_delete': tag_name, 'delete_from': project_name },
                        'user': { 'object_to_delete': user_name, 'delete_from': 'Gitlab' },
                        'group': { 'object_to_delete': group_name, 'delete_from': 'Gitlab' }}


    common.clickOutputMessage('WARNING', 'yellow', 'You are about to delete the ' + kind + ' <'
                              + click.style(print_dictionary[kind]['object_to_delete'], fg='yellow') + '> from <' 
                              + click.style(print_dictionary[kind]['delete_from'], fg='yellow') + '>.')
        
    if not common.askForConfirmation(auto_confirm, 'Are you sure you want to do this? (yes/no): ', 'You decided not to delete the ' + kind + '.'):
        return 1
    
    if kind == 'project':
        element.delete()
    elif kind == 'branch':
        element.branches.delete(branch_name)
    elif kind == 'tag':
        element.tags.delete(tag_name)
    elif kind == 'user':
        gitlab_object.users.delete(user_id)
    elif kind == 'group':
        gitlab_object.groups.delete(group_id)    
    
    print('--------------------------------------------------------------------------------------')
    common.clickOutputMessage('OK', 'green', kind.capitalize() + ' has been deleted successfuly')


@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def delete():
    """Delete any element listed in 'Commands' section.

    Gitlab user permissions won't be violated. 
    You must use a token from an account that can delete the elements you want to!
    """
    pass


@delete.command('project', short_help="Delete a Project from Gitlab")
@click.option('--auto-confirm', '--yes', is_flag=True, help="Enable auto confirm")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('project_name')
def deleteCommandProject(project_name, auto_confirm, url, token):
    """Delete a project from Gitlab.

    You must define the project in the form of '<group>/<project_path>' or It won't work!"""

    # Check if project name is the one we can use
    if not common.validateProjectName(project_name):
        return 1
    else:
        try:
            gl = common.performConnection(url, token)
            common.clickOutputHeader('Deleting', 'Project', project_name)
            deleteGitlabElement('project', gl, auto_confirm, project_name)
        except Exception as e:
            raise click.ClickException(e)


@delete.command('branch', short_help="Delete a Branch from a Project")
@click.option('--project-name', '-p', required=True, help="Project to delete the branch from. Must be '<group>/<project_path>'")
@click.option('--auto-confirm', '--yes', is_flag=True, help="Enable auto confirm")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('branch_name')
def deleteCommandBranch(branch_name, project_name, auto_confirm, url, token):
    """Delete a Branch from a Gitlab Project

    You must define the --project-name option in the form of '<group>/<project_path>' or It won't work!"""
    
    if not common.validateProjectName(project_name):
        return 1
    else:
        try:
            gl = common.performConnection(url, token)
            common.clickOutputHeader('Deleting', 'Branch', branch_name, project_name)
            deleteGitlabElement('branch', gl, auto_confirm, project_name, branch_name)
        except Exception as e:
            raise click.ClickException(e)


@delete.command('tag', short_help="Delete a Tag from a Branch inside a Project")
@click.option('--project-name', '-p', required=True, help="Project to delete the tag from. Must be '<group>/<project_path>'")
@click.option('--auto-confirm', '--yes', is_flag=True, help="Enable auto confirm")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('tag_name')
def deleteCommandTag(tag_name, project_name, auto_confirm, url, token):
    """Delete a Tag from a Gitlab Project

    You must define the --project-name option in the form of '<group>/<project_path>' or It won't work!
    """

    if not common.validateProjectName(project_name):
        return 1
    else:
        try:
            gl = common.performConnection(url, token)
            common.clickOutputHeader('Deleting', 'Tag', tag_name, project_name)
            deleteGitlabElement('tag', gl, auto_confirm, project_name, '', tag_name)
        except Exception as e:
            raise click.ClickException(e)


@delete.command('user', short_help="Delete an user from Gitlab")
@click.option('--auto-confirm', '--yes', required=False, is_flag=True, help="Enable auto confirm")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('user_id', type=int)
def deleteCommandUser(user_id, auto_confirm, url, token):
    """Delete an User from Gitlab

    You must define the user by ID. You can find it by using the subcommand 'gcli get user id -u <user_name>'.
    """
    
    try:
        gl = common.performConnection(url, token)
        common.clickOutputHeader('Deleting', 'User', gl.users.get(user_id).username)
        deleteGitlabElement('user', gl, auto_confirm, '', '', '', user_id)
    except Exception as e:
        raise click.ClickException(e)


@delete.command('group', short_help="Delete a group from Gitlab")
@click.option('--auto-confirm', '--yes', is_flag=True, help="Enable auto confirm")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('group_id', type=int)
def deleteCommandGroup(group_id, auto_confirm, url, token):
    """Delete a Group from Gitlab

    You must define the group by its ID. You can find it by using the subcommand 'gcli get group id -g <group_name>'
    """

    try:
        gl = common.performConnection(url, token)
        common.clickOutputHeader('Deleting', 'Group', gl.groups.get(group_id).name)
        deleteGitlabElement('group', gl, auto_confirm, '', '', '', '', group_id)
    except Exception as e:
        raise click.ClickException(e)

