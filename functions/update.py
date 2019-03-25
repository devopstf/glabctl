#!/usr/bin/python3

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

def addToChanges(changes_json, key, old_value, new_value):
    changes_json[key] = { "before": old_value, "after": new_value }
    return changes_json

"""
def optionsBoolValidator(option_value, project_value):
    if (option_value == "False" or option_value == "True") and option_value != str(project_value):
        return True
    else:
        return False
"""

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def update():
    """Update values from already existing objects on Gitlab.

    Make sure the Token you're using can update the element you want!
    """
    pass


@update.command('project', short_help="Update projects values")
@click.option('--description', type=str, help="Edit project's description")
@click.option('--enable-lfs', type=click.Choice(['True', 'False']), help="Modify LFS status")
@click.option('--default-branch', type=str, help="Edit default branch")
@click.option('--access-request', type=click.Choice(['True', 'False']), help="Edit the Request Access option")
@click.option('--owner', type=int, help="Change project's owner. Must be ID")
@click.option('--visibility', type=click.Choice(['public', 'private', 'internal']), help="Change the project's visibility")
@click.option('--archive', type=click.Choice(['True', 'False']), help="Archive the project")
@click.option('--enable-c-reg', type=click.Choice(['True', 'False']), help="Enable/disable Container Registry for this project")
@click.option('--enable-issues', type=click.Choice(['True', 'False']), help="Enable/disable the creation of Issues")
@click.option('--enable-merge-requests', type=click.Choice(['True', 'False']), help="Toggle the creation of Merge Request")
@click.option('--enable-wiki', type=click.Choice(['True', 'False']), help="Toggle WIKI for this project")
@click.option('--enable-jobs', type=click.Choice(['True', 'False']), help="Toggle Jobs creation")
@click.option('--enable-snippets', type=click.Choice(['True', 'False']), help="Toggle Snippets")
@click.option('--enable-shared-runners', type=click.Choice(['True', 'False']), help="Toggle Shared Runners")
@click.option('--jobs-visibility', type=click.Choice(['True', 'False']), help="Toggle Jobs visibility")
@click.option('--url', '-u', required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def updateCommandProject(project_name, description, enable_lfs, default_branch, access_request, 
                         owner, visibility, archive, enable_c_reg, enable_issues, enable_merge_requests,
                         enable_wiki, enable_jobs, enable_snippets, enable_shared_runners, jobs_visibility, url, token):
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

            # Placeholder IF logic until a better process is developed.
            if (description != None and project.description != description):
                changes = addToChanges(changes, 'description', project.description, description)
                project.description = description

            if (enable_lfs != None and enable_lfs != str(project.lfs_enabled)):
                changes = addToChanges(changes, 'lfs_enabled', project.lfs_enabled, enable_lfs)
                project.lfs_enabled = bool(enable_lfs)

            if (default_branch != None and project.default_branch != default_branch):
                try:
                    project.branches.get(default_branch) # Validate the branch exists
                    changes = addToChanges(changes, 'default-branch', project.default_branch, default_branch)
                    project.default_branch = default_branch

                except Exception:
                    failures[failures_counter] = "Could not edit default-branch value. Branch <" + click.style(default_branch, fg='yellow') + "> might not exist"
                    failures_counter += 1
                    pass

            if (access_request != None and access_request != str(project.request_access_enabled)):
                changes = addToChanges(changes, 'request_access_enabled', project.request_access_enabled, access_request)
                project.request_access_enabled = bool(access_request)

            if owner != None:
                try:
                    gl.users.get(owner) # Validate the user ID exists

                    if (project.owner['id'] != str(owner)):
                        changes = addToChanges(changes, 'owner', project.owner['id'], owner)
                        project.owner['id'] = owner

                except Exception:
                    failures[failures_counter] = "Could not edit owner value. Owner ID <" + click.style(owner, fg='yellow') + "> might not exist or project doesn't have an <owner> field."
                    failures_counter += 1
                    pass

            if visibility != None:
                if (gl.groups.get(project_name.split('/')[0]).visibility in ["private", "internal"]):
                    failures[failures_counter] = "Could not update visibility, seems the group's and the defined visibility are uncompatible."
                    failures_counter += 1
                else: 
                    changes = addToChanges(changes, 'visibility', project.visibility, visibility)
                    project.visibility = visibility

            if (archive != None and archive != str(project.archived)): # Doesn't work, although it detects it.
                changes = addToChanges(changes, 'archived', project.archived, archive)
                project.archived = bool(archive)

            if (enable_c_reg != None and enable_c_reg != str(project.container_registry_enabled)):
                changes = addToChanges(changes, 'container_registry_enabled', project.container_registry_enabled, enable_c_reg)
                project.container_registry_enabled = enable_c_reg

            if (enable_issues != None and enable_issues != str(project.issues_enabled)): 
                changes = addToChanges(changes, 'issues_enabled', project.issues_enabled, enable_issues) 
                project.issues_enabled = bool(enable_issues)

            if (enable_merge_requests != None and enable_merge_requests != str(project.merge_requests_enabled)):
                changes = addToChanges(changes, 'merge_requests_enabled', project.merge_request_enabled, enable_merge_requests)
                project.merge_request_enabled = enable_merge_requests

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




