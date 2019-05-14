#!/usr/bin/python3

import click,gitlab
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from .. import common
from . import get

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
    
    gl = common.performConnection(url, token)
    project_json = {}
    
    try:
        # Check If any of the command options were defined, then If true, add them to the project JSON
        if group != None:
            common.clickOutputHeader('Creating', 'Project', group + '/' + project_name)
            if gl.groups.list(search=group): # Check If group exists before doing anything...
                project_json['namespace_id'] = gl.groups.list(search=group)[0].id
            else:
                common.clickOutputMessage('ERROR', 'red', 'The group does not exist.')
                return 1
        else:
            common.clickOutputHeader('Creating', 'Project', common.getTokenUsername(gl) + '/' + project_name)
        if visibility != None: 
            project_json['visibility'] = visibility
        if description != None:
            project_json['description'] = description
        if default_branch != None:
            project_json['default-branch'] = default_branch
    
        # Generic data 
        project_json['name'] = project_name
    
        # Output messages & project creation
        common.clickOutputMessage('CREATING', 'yellow', 'Project <'
                                  + click.style(project_name, fg='yellow') + '> is being created, please wait...')
        project = gl.projects.create(project_json)
        common.clickOutputMessage('OK', 'green', 'Your project has been created! Please, check your Gitlab UI!')

        # In case of initialization, create the README.md (or not!)
        if initialize or default_branch == None:
            if group != None: # If namespace were defined, we must adjust the init_project value so we don't point to a wrong project
                init_project = gl.projects.get(group + '/' + project_name)
            else:
                init_project = gl.projects.get(common.getTokenUsername(gl) + '/' + project_name)

            # Check If there's a default branch so project is initialized with it!
            if default_branch != None:
                branch = defaultbranch
            else:
                branch = 'master'

            common.clickOutputMessage('INITIALIZING', 'yellow', 'Initializing your project with a README.md on <' 
                                      + click.style(branch, fg='yellow') + '> branch') 

            # File creation
            init_file = init_project.files.create({'file_path': 'README.md',
                                                  'branch': branch,
                                                  'content': '# Initial README of project ' + project_name,
                                                  'commit_message': 'Initial commit'})
        
            common.clickOutputMessage('OK', 'green', 'The project has been initialized!')

    except Exception as e:
        raise click.ClickException(e)
    

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
    try:
        gl = common.performConnection(url, token)
        branch_project = gl.projects.get(project_name)
        branch_project.branches.create({'branch': branch_name, 'ref': reference})
        common.clickOutputHeader('Creating', 'Branch', branch_name, project_name + ' (' + reference + ')')
        common.clickOutputMessage('OK', 'green', 'Branch <' 
                                  + click.style(branch_name, fg='yellow') + '> was created correctly in project <' 
                                  + click.style(project_name, fg='yellow') + '>')
    except Exception as e:
        raise click.ClickException(e)


@create.command('tag', short_help='Create a tag inside a project')
@click.option('--reference', '--ref', '-r', default="master", help="Choose which branch to use as a reference")
@click.option('--project-name', '-p', required=True, help="Select the project in which to create the branch. Must be <group>/<project_path>.")
@click.option('--url', help="URL directing to Gitlab")
@click.option('--token', help="Private token to access Gitlab")
@click.argument('tag_name')
def createCommandTag(tag_name, reference, project_name, url, token):
    """Create a Tag inside a project using the specified branch as a reference.
    
    Project name MUST be provided in the form <group>/<project_name>."""

    if(len(project_name.split('/')) != 2):
        common.clickOutputMessage('ERROR', 'red', 'The --project-name or -p option should be defined as <group>/<project_path>.')
        return 1

    try:
        gl = common.performConnection(url, token)
        
        common.clickOutputHeader('Creating', 'Tag', tag_name, project_name + ' (' + reference + ')')
        project = gl.projects.get(project_name)
        tag_project = gl.projects.get(project.id)
        common.clickOutputMessage('TAGGING', 'yellow', 'Creating the tag <' 
                   + click.style(tag_name, fg='yellow') + '> in the project <' 
                   + click.style(project_name, fg='yellow')  + '> ... Please, wait.')
        tag_project.tags.create({'tag_name': tag_name, 'ref': reference})
        common.clickOutputMessage('OK', 'green', 'Tag created successfully!')
    except Exception as e:
        raise click.ClickException(e)


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

    try:
        gl = common.performConnection(url, token)
        user_json = {}

        common.clickOutputHeader('Creating', 'User', username)

        user_json['username'] = username
        if name != None:
            user_json['name'] = name
        else:
            user_json['name'] = username.capitalize()
        user_json['email'] = mail
        user_json['password'] = password

        if make_admin:
            common.clickOutputMessage('WARNING', 'yellow', 'You are about to grant the <' + click.style("admin role", fg='red') + "> to this user...")
            print('--------------------------------------------------------------------------------------')
            if common.askForConfirmation(auto_confirm, 'Are you sure you want to do this? (yes/no): ', 'You decided not to create the user ' + username + ' as an admin user.'):
               user_json['admin'] = True 

        if group_creator:
            user_json['can_create_group'] = True
        else:
            user_json['can_create_group'] = False
        if private:
            user_json['private_profile'] = True
        if skip_confirmation:
            user_json['skip_confirmation'] = True
        if reset_password:
            user_json['reset_password'] = True
        if external:
            user_json['external'] = True

        print('--------------------------------------------------------------------------------------')
        common.clickOutputMessage('PROCESSING', 'yellow', 'Creating the user <'
                                  + click.style(username, fg='yellow') + '>')
        user = gl.users.create(user_json)
        print('--------------------------------------------------------------------------------------')
        common.clickOutputMessage('OK', 'green', 'User created successfully!')

    except Exception as e:
        raise click.ClickException(e)


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

    try:
        gl = common.performConnection(url, token)
        group_json = {}
        
        common.clickOutputHeader('Creating', 'Group', group_name)
        group_json['name'] = group_name
        
        if path != None:
            group_json['path'] = path
        else:
            transformed_path = group_name.replace(' ', '-')
            group_json['path'] = transformed_path.lower()
        if description != None:
            group_json['description'] = description
        if visibility != None:
            group_json['visibility'] = visibility
        if enable_lfs:
            group_json['lfs_enabled'] = True
        if enable_access_request:
            group_json['request_access_enabled'] = True
        if parent_id != "None":
            group_json['parent_id'] = parent_id

        common.clickOutputMessage('CREATING', 'yellow', 'Creating the group <'
                                  + click.style(group_name, fg='yellow') + '>')
        group = gl.groups.create(group_json)
        common.clickOutputMessage('OK', 'green', 'Group created successfully!')

    except Exception as e:
        raise click.ClickException(e)
