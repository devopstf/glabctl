#!/usr/bin/python

import gitlab,click,os
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common


def beautifullyDisplayChanges(changes_json):
    print('--------------------------------------------------------------------------------------')
    for ki,vi in changes_json.items():
        for kj,vj in vi.items():
            if kj == 'before':
                changes = click.style(str(vj), fg='red')
            else:
                changes = changes + ' --> ' + click.style(str(vj), fg='yellow')
        click.echo('[' + click.style(ki, fg='green') + '] ' + changes) 
    print('--------------------------------------------------------------------------------------')

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def update():
    """Update values from already existing objects on Gitlab.

    Make sure the Token you're using can update the element you want!
    """
    pass


@update.command('project', short_help="Update projects values")
@click.option('--description', default="None", required=False, help="Edit project's description")
@click.option('--enable-lfs/--disable-lfs', default=True, required=False, help="Modify LFS status")
@click.option('--default-branch', default="None", required=False, help="Edit default branch")
@click.option('--access-request/--no-access-request', default=False, required=False, help="Edit the Request Access option")
@click.option('--owner', required=False, help="Change project's owner")
@click.option('--visibility', required=False, help="Change the project's visibility")
@click.option('--archive/--unarchive', required=False, help="Archive the project")
@click.option('--active/--inactive', required=False, help="Toggle active/inactive project")
@click.option('--enable-c-reg/--disable-c-reg', required=False, help="Enable/disable Container Registry for this project")
@click.option('--enable-issues/--disable-issues', required=False, help="Enable/disable the creation of Issues")
@click.option('--enable-merge-requests/--disable-merge-request', required=False, help="Toggle the creation of Merge Request")
@click.option('--enable-wiki/--disable-wiki', required=False, help="Toggle WIKI for this project")
@click.option('--enable-jobs/--disable-jobs', required=False, help="Toggle Jobs creation")
@click.option('--enable-snippets/--disable-snippets', required=False, help="Toggle Snippets")
@click.option('--enable-shared-runners/--disable-shared-runners', required=False, help="Toggle Shared Runners")
@click.option('--public-jobs/--private-jobs', required=False, help="Toggle Jobs visibility")
@click.option('--url', '-u', required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def updateCommandProject(project_name, description, enable_lfs, default_branch, access_request, 
                         owner, visibility, archive, active, enable_c_reg, enable_issues, enable_merge_requests,
                         enable_wiki, enable_jobs, enable_snippets, enable_shared_runners, public_jobs, url, token):
    
    if not common.validateProjectName(project_name):
        return 1
    else:
        try:
            gl = common.performConnection(url, token)
            project = gl.projects.get(project_name)
            changes = {}

            if description != "None" and project.description != description:
                changes['description'] = { 'before': project.description, 'after': description }
                project.description = description
            if enable_lfs != project.lfs_enabled:
                changes['lfs_enabled'] = { 'before': project.lfs_enabled, 'after': enable_lfs }
                project.lfs_enabled = enable_lfs
            if default_branch != "None" and project.default_branch != default_branch:
                changes['default-branch'] = { 'before': project.default_branch, 'after': default_branch }
                project.default_branch = default_branch
            if access_request != project.request_access_enabled:
                changes['request_access_enabled'] = { 'before': project.request_access_enabled, 'after': access_request }
                project.request_access_enabled = access_request

            if not changes:
                click.echo('[' + click.style('OK', fg='green') + '] The changes history is empty. There is nothing to change.')
                return 1
            else:
                click.echo('[' + click.style('NEW STATE', fg='yellow') + '] The project parameters are about to change. Please, check the JSON output and validate it!')
                beautifullyDisplayChanges(changes)
            
                confirmation = input('Do you want to update the project? (yes/no): ')
                if confirmation != 'yes':
                    click.echo('[' + click.style('TERMINATING...', fg='red') + '] You decided not to delete the ' + kind + '.')
                    return 1
            
                project.save()

        except Exception as e:
            raise click.ClickException(e)




