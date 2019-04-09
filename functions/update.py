#!/usr/bin/python3

import gitlab,click,os
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common


def beautifullyDisplayChanges(changes_json, failures_json):
    changes = ""

    # Output detected changes in configuration...
    if changes_json:
        print('--------------------------------------------------------------------------------------')
        for ki,vi in changes_json.items():
            for kj,vj in vi.items():
                if kj == 'before':
                    changes = click.style(str(vj), fg='red')
                else:
                    changes = changes + ' --> ' + click.style(str(vj), fg='yellow')
            common.clickOutputMessage(ki, 'green', changes) 

    # Output detected errors...
    if failures_json:
        print('--------------------------------------------------------------------------------------')
        print("We detected some errors when updating certain values: ")
        for failure_key, failure_value in failures_json.items():
            click.echo('   ' + click.style('>', fg='yellow') + ' ' + failure_value)
    
    print('--------------------------------------------------------------------------------------')
    print(' Take in consideration that If you specified a change but It is not shown it is       ')
    print(' probably due to the value being already present in the current state of the element  ')
    print('--------------------------------------------------------------------------------------')


def addToChanges(changes_json, key, old_value, new_value):
    changes_json[key] = { "before": old_value, "after": new_value }
    return changes_json


def applyChanges(element, gl_object, changes_json, auto_confirm, failures_json):
    if changes_json:
        common.clickOutputMessage('NEW STATE', 'yellow', 'The ' + element + ' parameters are about to change.')
        beautifullyDisplayChanges(changes_json, failures_json)
        
        if not common.askForConfirmation(auto_confirm, ' >>> Do you want to update the ' + element + '? (yes/no): ', 'You decided not to save the modifications'):
            return 1

        if 'archived' in changes_json:
            hideElement(gl_object, changes_json, auto_confirm, 'archived')
        elif 'state' in changes_json:
            hideElement(gl_object, changes_json, auto_confirm, 'state')

        print('--------------------------------------------------------------------------------------')
        common.clickOutputMessage('SAVING', 'yellow', 'Applying all defined changes')
        gl_object.save()
        print('--------------------------------------------------------------------------------------')
        common.clickOutputMessage('OK', 'green', 'Your changes have been applied correctly')

    else:
        common.clickOutputMessage('OK', 'green', 'The changes history is empty. There is nothing to change')
        return 1


def hideElement(gl_object, changes, auto_confirm, key):
    print('--------------------------------------------------------------------------------------')
    if changes[key]['after'] in ('True', 'blocked'):
        if key == 'archived':
            common.clickOutputMessage('ARCHIVING', 'yellow', 'Changes include archiving the project...')
        
            if common.askForConfirmation(auto_confirm, ' >>> Do you really want to archive this project? (yes/no): ', 'Project will not be archived', 'ARCHIVING CANCELLED'):
                gl_object.archive() 

        elif key == 'state':
            if common.askForConfirmation(auto_confirm, ' >>> Do you really want to block this user? (yes/no): ', 'User will remain unblocked in this system', 'BLOCK CANCELLED'):
                gl_object.block()

    else:
        if key == 'archived':
            if common.askForConfirmation(auto_confirm, ' >>> Do you really want to unarchive this project? (yes/no): ', 'Project will remain archived', 'UNARCHIVING CANCELLED'):
                gl_object.unarchive()

        elif key == 'state':
            if common.askForConfirmation(auto_confirm, ' >>> Do you really want to unblock this user? (yes/no): ',
                                         'User will remain blocked in this system', 'UNBLOCK CANCELLED'):
                gl_object.unblock()


@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def update():
    """Update values from already existing objects on Gitlab.

    Make sure the Token you're using can update the element you want!
    """
    pass


@update.command('project', short_help="Update projects values")
@click.option('--name', type=str, help="Change project's name")
@click.option('--path', type=str, help="Change project's path")
@click.option('--sync', is_flag=True, help="Toggle to update the path value with the name one and viceversa")
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
@click.option('--public-jobs', type=click.Choice(['True', 'False']), help="Toggle Jobs visibility")
@click.option('--auto-confirm', '--yes', is_flag=True, help="Activate automatic confirmation of steps")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('project_name')
def updateCommandProject(project_name, name, path, sync, description, enable_lfs, default_branch, access_request, 
                         owner, visibility, archive, enable_c_reg, enable_issues, enable_merge_requests, enable_wiki,
                         enable_jobs, enable_snippets, enable_shared_runners, public_jobs, auto_confirm, url, token):
    """Update most of the configurable values of a Project.

    Project must be defined in the form of '<group>/<project_path>'. Also, values must be in range for it 
    to work (i.e. if you define a default-branch, It must exists previously)
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
            
            common.clickOutputHeader('Updating', 'Project', project.path_with_namespace)
            common.clickOutputMessage('VALIDATING...', 'yellow', 'The process of checking your changes is being done.')
            print('--------------------------------------------------------------------------------------')

            # Placeholder IF logic until a better process is developed.
            if name != None and name != project.name:
                changes = addToChanges(changes, 'name', project.name, name)
                project.name = name
                if sync and name != project.path:
                    changes = addToChanges(changes, 'path', project.path, name)
                    project.path = name

            if path != None and path != project.path:
                changes = addToChanges(changes, 'path', project.path, path)
                project.path = path
                if sync and path != project.name:
                    changes = addToChanges(changes, 'name', project.name, path)
                    project.name = path

            
            if (description != None and project.description != description):
                changes = addToChanges(changes, 'description', project.description, description)
                project.description = description

            if (enable_lfs != None and enable_lfs != str(project.lfs_enabled)):
                changes = addToChanges(changes, 'lfs_enabled', project.lfs_enabled, enable_lfs)
                project.lfs_enabled = enable_lfs

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
                project.request_access_enabled = access_request

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
                project.issues_enabled = enable_issues

            if (enable_merge_requests != None and enable_merge_requests != str(project.merge_requests_enabled)):
                changes = addToChanges(changes, 'merge_requests_enabled', project.merge_requests_enabled, enable_merge_requests)
                project.merge_requests_enabled = enable_merge_requests

            if (enable_wiki != None and enable_wiki != str(project.wiki_enabled)):
                changes = addToChanges(changes, 'wiki_enabled', project.wiki_enabled, enable_wiki)
                project.wiki_enabled = enable_wiki

            if (enable_jobs != None and enable_jobs != str(project.jobs_enabled)):
                changes = addToChanges(changes, 'jobs_enabled', project.jobs_enabled, enable_jobs)
                project.jobs_enabled = enable_jobs

            if (enable_snippets != None and enable_snippets != str(project.snippets_enabled)):
                changes = addToChanges(changes, 'snippets_enabled', project.snippets_enabled, enable_snippets)
                project.snippets_enabled = enable_snippets

            if (enable_shared_runners != None and enable_shared_runners != str(shared_runners_enabled)):
                changes = addToChanges(changes, 'shared_runners_enabled', project.shared_runners_enabled, enable_shared_runners)
                project.shared_runners_enabled = enable_shared_runners

            if (public_jobs != None and public_jobs != str(public_jobs)):
                changes = addToChanges(changes, 'public_jobs', project.public_jobs, public_jobs)
                project.public_jobs = public_jobs

            applyChanges('project', project, changes, auto_confirm, failures)

        except Exception as e:
            raise click.ClickException(e)


@update.command('group', short_help="Update groups values")
@click.option('--name', type=str, help="Change group's name")
@click.option('--path', type=str, help="Change group's path")
@click.option('--sync', is_flag=True, help="Toggle to update the path value with the name one and viceversa")
@click.option('--description', type=str, help="Edit group's description")
@click.option('--enable-lfs', type=click.Choice(['True', 'False']), help="Modify LFS status")
@click.option('--access-request', type=click.Choice(['True', 'False']), help="Edit the Request Access option")
@click.option('--visibility', type=click.Choice(['public', 'private', 'internal']), help="Change the group's visibility")
@click.option('--parent-id', type=int, help="Toggle Jobs visibility")
@click.option('--auto-confirm', '--yes', is_flag=True, help="Auto confirm any change")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('group_name')
def updateCommandGroup(group_name, name, path, sync, description, enable_lfs, access_request, visibility, parent_id, auto_confirm, url, token):
    """Update a Group's values and flags."""

    try:
        gl = common.performConnection(url, token)
        changes = {}
        failures = {}
        group = gl.groups.get(group_name)

        common.clickOutputHeader('Updating', 'Group', group.full_path)
        common.clickOutputMessage('VALIDATING...', 'yellow', 'The process of checking your changes is being done.')
        print('--------------------------------------------------------------------------------------')

        if name != None and name != group.name:
            changes = addToChanges(changes, 'name', group.name, name)
            group.name = name
            if sync:
                changes = addToChanges(changes, 'path', group.path, name)
                group.path = name

        if path != None and path != group.path:
            changes = addToChanges(changes, 'path', group.path, path)
            group.path = path
            if sync:
                changes = addToChanges(changes, 'name', group.name, path)
                group.name = path

        if description != None and description != group.description:
            changes = addToChanges(changes, 'description', group.description, description)
            group.description = description

        if enable_lfs != None and enable_lfs != group.lfs_enabled:
            changes = addToChanges(changes, 'lfs_enabled', group.lfs_enabled, enable_lfs)
            group.lfs_enabled = enable_lfs

        if access_request != None and access_request != group.request_access_enabled:
            changes = addToChanges(changes, 'request_access_enabled', group.request_access_enabled, access_request)
            group.request_access_enabled = access_request

        if visibility != None and visibility != group.visibility:
            changes = addToChanges(changes, 'visibility', group.visibility, visibility)
            group.visibility = visibility

        if parent_id != None and parent_id != group.parent_id:
            changes = addToChanges(changes, 'parent_id', group.parent_id, parent_id)
            parent_group_name = gl.groups.get(parent_id).name
            print(parent_group_name)
            group.full_path = str(parent_group_name) + '/' + str(group.name)
            print(group.full_path)

        applyChanges('group', group, changes, auto_confirm, failures)

    except Exception as e:
        raise click.ClickException(e)


@update.command("user", short_help="Update users parameters")
@click.option('--name', help='Change user full name')
@click.option('--projects-limit', type=int, help='Amounts of projects this user can create')
@click.option('--can-create-group', type=click.Choice(['True', 'False']), help='Wether or not this user can create a group')
@click.option('--can-create-project', type=click.Choice(['True', 'False']), help='Wether or not this user can create projects')
@click.option('--external', type=click.Choice(['True', 'False']), help='Turn this to <True> if you want to make this user external')
@click.option('--is-admin', type=click.Choice(['True', 'False']), help='Wether or not you want this user to be an administrator')
@click.option('--blocked', '--banned', type=click.Choice(['True', 'False']), help='Block or unblock this user')
@click.option('--auto-confirm', '--yes', is_flag=True, help='Toggle auto confirm')
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('username')
def updateCommandUser(username, name, projects_limit, can_create_group, can_create_project, external, is_admin, blocked, auto_confirm, url, token):
    """ Update common User values and flags in one go.

    Take in consideration you can't change the email as of yet!"""

    try:
        gl = common.performConnection(url, token)
        changes = {}
        failures = {}
        user = gl.users.list(username=username)[0]

        if name != None and name != user.name:
            changes = addToChanges(changes, 'name', user.name, name)
            user.name = name

        if projects_limit != None and str(projects_limit) != str(user.projects_limit):
            changes = addToChanges(changes, 'project_limit', user.projects_limit, projects_limit)
            user.projects_limit = projects_limit

        if can_create_group != None and str(can_create_group) != str(user.can_create_group):
            changes = addToChanges(changes, 'can_create_group', user.can_create_group, can_create_group)
            user.can_create_group = can_create_group

        if can_create_project != None and str(can_create_project) != str(user.can_create_project):
            changes = addToChanges(changes, 'can_create_project', user.can_create_project, can_create_project)
            user.can_create_project = can_create_project

        if external != None and str(external) != str(user.external):
            changes = addToChanges(changes, 'external', user.external, external)
            user.external = external

        if is_admin != None and str(is_admin) != str(user.is_admin):
            changes = addToChanges(changes, 'is_admin', user.is_admin, is_admin)
            user.is_admin = is_admin

        if blocked != None and str(blocked) == "True" and user.state != 'blocked':
            changes = addToChanges(changes, 'state', user.state, 'blocked')
            user.state = 'blocked'

        elif blocked != None and str(blocked) == "False" and user.state == 'blocked':
            changes = addToChanges(changes, 'state', user.state, 'active')
            user.state = 'active'

        applyChanges('user', user, changes, auto_confirm, failures)

    except Exception as e:
        raise click.ClickException(e)


@update.command("branch", short_help="Update branch protection")
@click.option('--protect', type=click.Choice(['True', 'False']), help="Define if the branch is protected or not")
@click.option('--project-name', '-p', help="The project where the branch is located. Must be <group>/<project_name>")
@click.option('--url', help='URL directing to Gitlab')
@click.option('--token', help="Private token to access Gitlab")
@click.argument('branch_name')
def updateCommandBranch(branch_name, protect, project_name, url, token):
    """Update branch protection status."""
    try:
        gl = common.performConnection(url, token)
        changes = {}
        failures = {}
        project = gl.projects.get(project_name)
        branch = project.branches.get(branch_name)

        if protect != None and str(branch.protected) != str(protect):
            if str(branch.protected) == "True":
                branch.unprotect()
            elif str(branch.protected) == "False":
                branch.protect()

    except Exception as e:
        raise click.ClickException(e)
