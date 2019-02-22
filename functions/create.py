#!/usr/bin/python

import click,gitlab
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common,get

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def create():
    """Create any element listed in 'Commands' section.

    You can create projects, users, groups, branches...
    Based on your current permission in the Gitlab installation!
    """
    pass

@create.command('project', short_help='[WIP] Create a project')
@click.option('--description', required=False, default="None", help="Description for the project")
@click.option('--default-branch', '-defb', required=False, default="None", help='Default branch to use')
@click.option('--namespace', '-ns', required=False, default="None", help="Which group/namespace to use")
@click.option('--visibility', '-v', required=False, default="None", help="Visibility of this project")
@click.option('--initialize', '--init', required=False, is_flag=True, help="Initialize project with README.md")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def createCommandProject(project_name, description, defaultbranch, namespace, visibility, initialize, url, token):
    gl = common.performConnection(url, token)
    project_json = {}

    # Check If any of the command options were defined, then If true, add them to the project JSON
    if namespace != "None":
        namespace_json = {}
        if gl.groups.list(search=namespace): # Check If group exists before doing anything...
            project_json['namespace_id'] = gl.groups.list(search=namespace)[0].id
        else:
            click.echo("[" + click.style('ERROR', fg='red') + "] The group doesn't exist.")
            return 1
    if visibility != "None": 
        project_json['visibility'] = visibility
    if description != "None":
        project_json['description'] = description
    if default_branch != "None":
        project_json['default-branch'] = default_branch

    # Generic data 
    project_json['name'] = project_name
    
    # Output messages & project creation
    click.echo('[' + click.style('CREATING', fg='yellow') + '] Project <' 
               + click.style(project_name, fg='yellow') + '> is being created, please wait...')
    project = gl.projects.create(project_json)
    click.echo('[' + click.style('OK', fg='green') + '] Your project has been created! Please, check your Gitlab UI!')

    # In case of initialization, create the README.md (or not!)
    if initialize:
        if namespace != "None": # If namespace were defined, we must adjust the init_project value so we don't point to a wrong project
            init_project = gl.projects.get(namespace + '/' + project_name)
        else:
            init_project = gl.projects.get('Administrator/' + project_name)

        # Check If there's a default branch so project is initialized with it!
        if defaultbranch != "None":
            branch = defaultbranch
        else:
            branch = 'master'

        click.echo('[' + click.style('INITIALIZING', fg='yellow') + '] Initializing your project with a README.md on <' 
                   + click.style(branch, fg='yellow') + '> branch') 

        # File creation
        init_file = init_project.files.create({'file_path': 'README.md',
                                              'branch': branch,
                                              'content': '# Initial README of project ' + project_name,
                                              'commit_message': 'Initial commit'})
        
        click.echo('[' + click.style('OK', fg='green') + '] The project has been initialized!')
    


@create.command('branch', short_help='Create a branch from another one')
@click.option('--reference', '--ref', '-r', required=False, default='master', help="Choose which branch to use as a reference")
@click.option('--project', '-p', required=True, help="Select which project to use")
@click.option('--team', '-t', required=True, help="Select the team")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('branch_name')
def createCommandBranch(branch_name, project, reference, url, token, team):
    """Easily create a new branch in a specific project in your Gitlab!

    Useful when implementing a process where a branch is created due to
    a Client creating a new feature to be developed, or simply automating the branches creation.
    """
    try:
        gl = common.performConnection(url, token)
        project_full_name = team + '/' + project
        branch_project = gl.projects.get(project_full_name)
        branch_project.branches.create({'branch': branch_name, 'ref': reference})
        click.echo('[' + click.style('OK', fg='green') + '] Branch "' 
                   + click.style(branch_name, fg='yellow') + '" was created correctly in project "' 
                   + click.style(project_full_name, fg='yellow') + '"')
    except Exception as e:
        raise click.ClickException(e)


# TODO - Create a validation in --project-name option
@create.command('tag', short_help='Create a tag inside a project')
@click.option('--reference', '--ref', '-r', required=False, default="master", help="Choose which branch to use as a reference")
@click.option('--project-name', '-p', required=True, help="Select the project in which to create the branch. Must be namespace/name.")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('tag_name')
def createCommandTag(tag_name, reference, project_name, url, token):
    """Create a Tag inside a project using the specified branch as a reference.
    
    Project name MUST be provided in the form <group>/<project_name>."""

    try:
        gl = common.performConnection(url, token)

        project = gl.projects.get(project_name)
        tag_project = gl.projects.get(project.id)
        click.echo('[' + click.style('TAGGING', fg='yellow') + '] Creating the tag <' 
                   + click.style(tag_name, fg='yellow') + '> in the project <' 
                   + click.style(project_name, fg='yellow')  + '> ... Please, wait.')
        tag_project.tags.create({'tag_name': tag_name, 'ref': reference})
        click.echo('[' + click.style('OK', fg='green') + '] Tag created successfully!')
    except Exception as e:
        raise click.ClickException(e)
