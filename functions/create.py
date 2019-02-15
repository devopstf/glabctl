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
@click.option('--defaultbranch', '-defb', required=False, default="None", help='Default branch to use')
@click.option('--namespace', '-ns', required=False, default="None", help="Which group/namespace to use")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def project(project_name, description, defaultbranch, namespace, url, token):
    my_project = {}
    my_namespace = {}
    my_project['name'] = project_name
    my_project['description'] = description
    my_project['default-branch'] = defaultbranch
    my_namespace['name'] = namespace
    # Get the group ID using the get command!
    #my_namespace['id'] =
    my_project['namespace'] = my_namespace

    gl = common.performConnection(url, token)
    print(my_project)

    #project = gl.projects.create(my_project)


@create.command('branch', short_help='Create a branch from another one')
@click.option('--ref', '-r', required=False, default='master', help="Choose which branch to use as a reference")
@click.option('--project', '-p', required=True, help="Select which project to use")
@click.option('--team', '-t', required=True, help="Select the team")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('branch_name')
def createCommandBranch(branch_name, project, ref, url, token, team):
    """Easily create a new branch in a specific project in your Gitlab!

    Useful when implementing a process where a branch is created due to
    a Client creating a new feature to be developed, or simply automating the branches creation.
    """
    try:
        gl = common.performConnection(url, token)
        project_full_name = team + '/' + project
        branch_project = gl.projects.get(project_full_name)
        branch_project.branches.create({'branch': branch_name, 'ref': ref})
        click.echo('[' + click.style('OK', fg='green') + '] Branch "' + click.style(branch_name, fg='yellow') + '" was created correctly in project "' + click.style(project_full_name, fg='yellow') + '"')
    except Exception as e:
        raise click.ClickException(e)
