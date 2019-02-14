#!/usr/bin/python

import gitlab,click,os,json
from click_help_colors import HelpColorsGroup, HelpColorsCommand

def checkCredentials():
    if('GITLABCTL_TOKEN' in os.environ):
        return True
    else:
        return False

def defineGitlabHost(url):
    if url:
        return url
    else:
        return getGitlabURL()

def defineGitlabToken(token):
    if token:
        return token
    else:
        return os.environ.get('GITLABCTL_TOKEN')

def getGitlabURL():
    if('GITLABCTL_URL' in os.environ):
        return os.environ.get('GITLABCTL_URL')
    else:
        return "http://localhost"

def performConnection(url, token):
    connection_host = defineGitlabHost(url)
    connection_token = defineGitlabToken(token)
    return gitlab.Gitlab(connection_host, private_token=connection_token)

#gl = gitlab.Gitlab('http://localhost', private_token='77w9Sb_BDf_xRUW9WEan')
host = "http://localhost"

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def main():
    """A command-line tool to control Gitlab from its API.

    \b
    This tool can get, describe, create, modify or delete multiple
    Gitlab elements through the use of its API to provide an easy
    way to control your own Gitlab installation without the need
    of accessing It through a Web Browser!

    It might be useful for automated processes of a CI/CD pipeline
    or as a workaround for Tools which can't control Gitlab natively.

    -----------------------------------------

    Created by: Óscar Díaz Domínguez    

    -----------------------------------------

    Github: https://github.com/devopstf                                                    
    Personal Github: https://github.com/odiazdom
    """
    pass

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def get():
    """Get any element listed in 'Commands' section.

    You can obtain data from Gitlab Projects, Users, Groups, etc...
    Some of the commands have internal options.
    """
    pass


@get.command('projects', short_help="Get all projects in Gitlab")
@click.option('--group', '-g', required=False, help="Specific group to search in")
@click.option('--url', '-u',required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def projects(group, url, token):
    """A subcommand to list all projects in Gitlab
    
    You can filter by Gitlab group using the corresponding option!
    """
    gl = performConnection(url, token)

    try:
        if group:
            search_group = gl.groups.get(group)
            projects = search_group.projects.list()
        else:
            projects = gl.projects.list()
        for p in projects:
            print(p)
    except Exception as e:
        raise click.ClickException(e)


@get.command('branches', short_help='Get all branches inside a Project')
@click.option('--team', '-t', required=True, default='phG1TL4BCTL', help="Team name to use")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def branches(team, url, token, project_name):
    """With this command you can get a list of all branches inside a Project."""
    if(team != "phG1TL4BCTL"):
        gl = performConnection(url, token)

        try:
            project_full_name = team + '/' + project_name
            project = gl.projects.get(project_full_name)
            branches = project.branches.list()
            for b in branches:
                print(b.name)
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
def users(username, url, token):
    """Simple users list, with some filters"""
    gl = performConnection(url, token)

    try:
        users = gl.users.list(search=username)
        for u in users:
            print(u)
    except Exception as e:
        raise click.ClickException(e)


@get.command('groups', short_help='Get groups created on Gitlab')
@click.option('--groupname', '--name', '-gn', required=False, help="Username to search")
@click.option('--url', '-u', required=False, help="URL directing to Gitlab")
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
def groups(groupname, url, token):
    """Simple groups list"""
    gl = performConnection(url, token)

    try:
        if not groupname:
            groups = gl.groups.list()
            for g in groups:
                print(g)
        else:
            groups = gl.groups.get(groupname)
            print(groups)

    except Exception as e:
        raise click.ClickException(e)


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
    
    gl = performConnection(url, token)
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
        gl = performConnection(url, token)
        project_full_name = team + '/' + project
        branch_project = gl.projects.get(project_full_name)
        branch_project.branches.create({'branch': branch_name, 'ref': ref})
        click.echo('[' + click.style('OK', fg='green') + '] Branch "' + click.style(branch_name, fg='yellow') + '" was created correctly in project "' + click.style(project_full_name, fg='yellow') + '"')
    except Exception as e:
        raise click.ClickException(e)


main.add_command(get)
main.add_command(create)

if __name__ == "__main__":
    main()
