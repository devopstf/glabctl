#!/usr/bin/python3

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from ..classes import GitlabCTL as glabctl

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def create():
    """Create any element listed in 'Commands' section.

    You can create projects, users, groups, branches...
    Based on your current permission in the Gitlab installation!
    """
    pass

@create.command('project', short_help='Create a project')
@click.option('--description', '--desc', '-d', help="Description for the project")
@click.option('--default-branch', '--branch', '-b', '-defb', help='Default branch to use')
@click.option('--group', '--namespace', '-g', '-ns', help="Which group/namespace to use")
@click.option('--visibility', '-v', help="Visibility of this project")
@click.option('--initialize', '--init', '-i', is_flag=True, help="Initialize project with README.md")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('project_name')
def createCommandProject(project_name, description, default_branch, group, visibility, initialize, url, token):
    """Create a project & configure its different parameters, as default-branch, visibility, which group does it belong to...

    You can also initialize the project with the default branch using the --init flag! If a default branch is not defined, It'll create a master branch by default!"""
    
    gl = glabctl.GitlabCTL(url, token)
    gl.createProject(project_name, description, default_branch, group, visibility, initialize)

@create.command('branch', short_help='Create a branch from another one')
@click.option('--reference', '--ref', '-r', default='master', help="Choose which branch to use as a reference")
@click.option('--project-name', '-p', required=True, help="Select which project to use. Must be <group>/<project_path>.")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('branch_name')
def createCommandBranch(branch_name, project_name, reference, url, token):
    """Easily create a new branch in a specific project in your Gitlab!

    Useful when implementing a process where a branch is created due to
    a Client creating a new feature to be developed, or simply automating the branches creation.
    """
    gl = glabctl.GitlabCTL(url, token)
    gl.createBranch(branch_name, project_name, reference)


@create.command('tag', short_help='Create a tag inside a project')
@click.option('--reference', '--ref', '-r', default="master", help="Choose which branch to use as a reference")
@click.option('--project-name', '-p', required=True, help="Select the project in which to create the branch. Must be <group>/<project_path>.")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('tag_name')
def createCommandTag(tag_name, reference, project_name, url, token):
    """Create a Tag inside a project using the specified branch as a reference.
    
    Project name MUST be provided in the form <group>/<project_name>."""

    gl = glabctl.GitlabCTL(url, token)
    gl.createTag(tag_name, reference, project_name)


@create.command('user', short_help='Create an user in Gitlab')
@click.option('--mail', '-m', required=True, help="Mail to attach to this user")
@click.option('--name', '-n', help="Display name for the user")
@click.option('--password', '-pw', help="Define a password")
@click.option('--external', '-ext', is_flag=True, help="Make this user an external user")
@click.option('--make-admin', '--admin', '-adm', is_flag=True, help="Make this user an admin")
@click.option('--group-creator', '-gcreate', is_flag=True, help="Grant group creation permission")
@click.option('--private', '-pvt', is_flag=True, help="Make this user private")
@click.option('--skip-confirmation', '--skip', is_flag=True, help="Skip user confirmation")
@click.option('--reset-password', '--reset', is_flag=True, help="Send the user a reset link")
@click.option('--auto-confirm', '--yes', is_flag=True, help="Autoconfirm any prompt")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('username')
def createCommandUser(username, mail, name, password, external, make_admin, group_creator, private, skip_confirmation, reset_password, auto_confirm, url, token):
    """Create an user inside Gitlab

    You can define basic parameters as flags for creation permission and even define an user as an administrator.
    """

    gl = glabctl.GitlabCTL(url, token)
    gl.createUser(username, mail, name, password, external, make_admin, group_creator, private, skip_confirmation, reset_password, auto_confirm)


@create.command('group', short_help='Create a group in Gitlab')
@click.option('--path', help="Path to use for the group")
@click.option('--description', help="Add a description to the group")
@click.option('--visibility', help="Set up the visibility of this group")
@click.option('--enable-lfs', is_flag=True, help="Enable EFS on this group")
@click.option('--enable-access-request', '--access-request', is_flag=True, help="Enable access request")
@click.option('--parent-id', '--parent', help="Specify if there's a parent group, by ID")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('group_name')
def createCommandGroup(group_name, path, description, visibility, enable_lfs, enable_access_request, parent_id, url, token):
    """Create a Group for Gitlab repositories

    You can create a subgroup inside another group, but you'll need that group ID!"""
    
    gl = glabctl.GitlabCTL(url, token)
    gl.createGroup(group_name, path, description, visibility, enable_lfs, enable_access_request, parent_id)
