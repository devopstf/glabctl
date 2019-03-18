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


def optionsBoolValidator(option_value, project_value):
    if (option_value == "False" or option_value == "True") and option_value != str(project_value):
        return True
    else:
        return False


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
@click.option('--owner', default="None", required=False, help="Change project's owner")
@click.option('--visibility', default="None", required=False, help="Change the project's visibility")
@click.option('--archive/--unarchive', required=False, help="Archive the project")
@click.option('--enable-c-reg', default="None", help="Enable/disable Container Registry for this project")
@click.option('--enable-issues', default="None", required=False, help="Enable/disable the creation of Issues")
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
                         owner, visibility, archive, enable_c_reg, enable_issues, enable_merge_requests,
                         enable_wiki, enable_jobs, enable_snippets, enable_shared_runners, public_jobs, url, token):
    """Update most of the configurable values of a Project.

    Project must be defined in the form of '<group>/<project_name>'. 
    Also, values must be in range for it to work (i.e. if you define a default-branch, It must exists previously)
    """

    if not common.validateProjectName(project_name):
        return 1
    else:
        try:
            gl = common.performConnection(url, token)
            project = gl.projects.get(project_name)
            changes = {}
            failures = {}
            failures_counter = 0

            click.echo('[' + click.style('VALIDATING...', fg='yellow') + '] The process of checking your changes is being done.')

            if description != "None" and project.description != description:
                changes['description'] = { 'before': project.description, 'after': description }
                project.description = description
            if optionsBoolValidator(enable_lfs, project.lfs_enabled):
                changes['lfs_enabled'] = { 'before': project.lfs_enabled, 'after': enable_lfs }
                project.lfs_enabled = enable_lfs
            if default_branch != "None" and project.default_branch != default_branch:
                try:
                    project.branches.get(default_branch) # Validate the branch exists
                    changes['default-branch'] = { 'before': project.default_branch, 'after': default_branch }
                    project.default_branch = default_branch
                except Exception:
                    failures[failures_counter] = "Could not edit default-branch value. Branch <" + click.style(default_branch, fg='yellow') + "> might not exist"
                    failures_counter += 1
                    pass
            if optionsBoolValidator(access_request, project.request_access_enabled):
                changes['request_access_enabled'] = { 'before': project.request_access_enabled, 'after': access_request }
                project.request_access_enabled = access_request
            if owner != "None":
                try:
                    gl.users.get(owner) # Validate the user ID exists
                    changes['owner'] = { 'before': project.owner['id'], 'after': owner }
                    project.owner['id'] = owner
                except Exception:
                    failures[failures_counter] = "Could not edit owner value. Owner ID <" + click.style(owner, fg='yellow') + "> might not exist or project doesn't have an <owner> field."
                    failures_counter += 1
                    pass
            if visibility != "None":
                if visibility == "public" or visibility == "private" or visibility == "internal":
                    changes['visibility'] = { 'before': project.visibility, 'after': visibility }
                    project.visibility = visibility
                else:
                    click.echo('[' + click.style('ERROR', fg='red') + '] You cannot set a project visibility to the value <' 
                                + click.style(visibility, fg='yellow') +  '>. Change will not be done.')
            if archive != project.archived: # Doesn't work, although it detects it.
                changes['archived']  = { 'before': project.archived, 'after': archive }
                project.archived = archive
            if optionsBoolValidator(enable_c_reg, project.container_registry_enabled):
                changes['container_registry_enabled'] = { 'before': project.container_registry_enabled, 'after': enable_c_reg }
                project.container_registry_enabled = enable_c_reg
            if optionsBoolValidator(enable_issues, project.issues_enabled): 
                changes['issues_enabled'] = { 'before': project.issues_enabled, 'after': enable_issues } 
                project.issues_enabled = enable_issues


            if not changes:
                click.echo('[' + click.style('OK', fg='green') + '] The changes history is empty. There is nothing to change.')
                return 1
            else:
                click.echo('[' + click.style('NEW STATE', fg='yellow') + '] The project parameters are about to change. Please, check the JSON output and validate it!')
                beautifullyDisplayChanges(changes)
            
                confirmation = input('Do you want to update the project? (yes/no): ')
                if confirmation != 'yes':
                    click.echo('[' + click.style('TERMINATING...', fg='red') + '] You decided not save the modifications.')
                    return 1
                
                click.echo('[' + click.style('OK', fg='green') + '] Your changes have been applied correctly.')
                project.save()

            if failures:
                print("We detected some errors when updating certain values: ")
                for ki, vi in failures.items():
                    print(vi)
                    

        except Exception as e:
            raise click.ClickException(e)




