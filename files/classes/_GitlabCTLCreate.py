#!/usr/bin/python3

import click,gitlab
from .. import common

class Mixin:
    def returnValues(self):
        print("URL: " + self._url + "; TOKEN: " + self._token)

    def createProject(self, project_name, description, default_branch, group, visibility, initialize):
        project_json = {}

        try:
            # Check If any of the command options were defined, then If true, add them to the project JSON
            if group != None:
                common.clickOutputHeader('Creating', 'Project', group + '/' + project_name)
                if self._connection.groups.list(search=group): # Check If group exists before doing anything...
                    project_json['namespace_id'] = self._connection.groups.list(search=group)[0].id
                else:
                    common.clickOutputMessage('ERROR', 'red', 'The group does not exist.')
                    return 1
            else:
                common.clickOutputHeader('Creating', 'Project', common.getTokenUsername(self._connection) + '/' + project_name)
            
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
            project = self._connection.projects.create(project_json)
            common.clickOutputMessage('OK', 'green', 'Your project has been created! Please, check your Gitlab UI!')

            # In case of initialization, create the README.md (or not!)
            if initialize or default_branch == None:
                if group != None: # If namespace were defined, we must adjust the init_project value so we don't point to a wrong project
                    init_project = self._connection.projects.get(group + '/' + project_name)
                else:
                    init_project = self._connection.projects.get(common.getTokenUsername(self._connection) + '/' + project_name)

                # Check If there's a default branch so project is initialized with it!
                if default_branch != None:
                    branch = default_branch
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


    def createBranch(self, branch_name, project_name, reference):
        try:
            branch_project = self._connection.projects.get(project_name)
            branch_project.branches.create({'branch': branch_name, 'ref': reference})
            common.clickOutputHeader('Creating', 'Branch', branch_name, project_name + ' (' + reference + ')')
            common.clickOutputMessage('OK', 'green', 'Branch <'
                                      + click.style(branch_name, fg='yellow') + '> was created correctly in project <'
                                      + click.style(project_name, fg='yellow') + '>')
        except Exception as e:
            raise click.ClickException(e)

    
    def createTag(self, tag_name, reference, project_name):
        if(len(project_name.split('/')) != 2):
            common.clickOutputMessage('ERROR', 'red', 'The --project-name or -p option should be defined as <group>/<project_path>.')
            return 1

        try:
            common.clickOutputHeader('Creating', 'Tag', tag_name, project_name + ' (' + reference + ')')
            project = self._connection.projects.get(project_name)
            tag_project = self._connection.projects.get(project.id)
            common.clickOutputMessage('TAGGING', 'yellow', 'Creating the tag <'
                                       + click.style(tag_name, fg='yellow') + '> in the project <'
                                       + click.style(project_name, fg='yellow')  + '> ... Please, wait.')
            tag_project.tags.create({'tag_name': tag_name, 'ref': reference})
            common.clickOutputMessage('OK', 'green', 'Tag created successfully!')
        except Exception as e:
            raise click.ClickException(e)


    def createUser(self, username, mail, name, password, external, make_admin, group_creator, private, skip_confirmation, reset_password, auto_confirm):
        try:
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
            user = self._connection.users.create(user_json)
            print('--------------------------------------------------------------------------------------')
            common.clickOutputMessage('OK', 'green', 'User created successfully!')

        except Exception as e:
            raise click.ClickException(e)

    def createGroup(self, group_name, path, description, visibility, enable_lfs, enable_access_request, parent_id):
        try:
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
            group = self._connection.groups.create(group_json)
            common.clickOutputMessage('OK', 'green', 'Group created successfully!')

        except Exception as e:
            raise click.ClickException(e)
