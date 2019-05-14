#!/usr/bin/python3

import gitlab,click
from .. import common

class Mixin:
    
    ### Start private methods --
    def __findSpecificValue(self, kind, search_result, search_element):
        try:
            for i in search_result:
                if kind == 'user':
                    if i.username == search_element:
                        return i
                elif kind == 'group':
                    if i.path == search_element:
                        return i

        except:
            common.clickOutputMessage('ERROR', 'red', 'Could not find ' + kind + ' <' + click.style(search_element, fg='yellow') + '> in Gitlab...')

    def __printParameters(self, gl_object, parameter, sub_parameter, pretty_print, pretty_sort): # Prints parameters from non-plural 'get' subcommands
        try:
            dict_object = common.transformToDict(gl_object)

            if parameter == 'all':
                self.__outputResultsList(False, gl_object, False, pretty_print, pretty_sort, False)
            elif sub_parameter is not None:
                print(dict_object[parameter][sub_parameter])
            else:
                print(dict_object[parameter])

        except Exception as e:
            if not self.__outputParameterError(parameter, sub_parameter, e):
                raise click.ClickException(e)


    def __outputResultsList(self, raw, gl_object, specific_value, pretty_print, sort_json, use_path): # Prints different outputs: JSON, colorful value, raw value...
        if sort_json or pretty_print:
            specific_value = False
            pretty_print = True

        if specific_value:
            if use_path == "namespace":
                printable = gl_object.path_with_namespace
            elif use_path == "username":
                printable = gl_object.username
            elif use_path == "path":
                printable = gl_object.path
            else:
                printable = gl_object.name
        else:
            printable = common.transformToDict(gl_object)

        if raw and not pretty_print:
            print(printable)
        elif not specific_value:
            if pretty_print:
                json_object = common.transformToJson(printable)
                common.prettyPrintJson(json_object, sort_json)
            else:
                print(printable)
        else:
            click.echo('[' + click.style(printable, fg='yellow') + ']')


    def __outputParameterError(self, parameter, sub_parameter, e): # Function to return failure on parameter retrieval
        if sub_parameter is None:
            sub_parameter = "pl4c3h0ld3r"

        if str("'" + str(sub_parameter) + "'") == str(e):
            common.clickOutputMessage('ERROR', 'red', 'The sub-parameter <' + click.style(sub_parameter, fg='yellow') + '>, along with the parameter <'
                                      + click.style(parameter, fg='yellow') + '> is not an expected parameter or It does not exist for this element.')
            return True

        elif str(e) == str("'" + str(parameter) + "'"):
            common.clickOutputMessage('ERROR', 'red', 'The parameter <' + click.style(parameter, fg='yellow') + '> is not an expected parameter or It does not exist for this element.')
            return True

        else:
            return False

    ### End private methods ---

    ### Start public methods
    def getProjects(self, group, raw, verbose, with_namespace, pretty_print, pretty_sort):
        try:
            if group:
                search_group = self._connection.groups.get(group)
                projects = search_group.projects.list()
            else:
                projects = self._connection.projects.list()

            for p in projects:
                if with_namespace:
                    output_parameter = "namespace"
                else:
                    output_parameter = "placeholder"

                self.__outputResultsList(raw, p, not verbose, pretty_print, pretty_sort, output_parameter)

        except Exception as e:
            raise click.ClickException(e)


    def getProject(self, project_name, pretty_print, pretty_sort, parameter, sub_parameter):
        if not common.validateProjectName(project_name):
            return 1
        else:
            self.__printParameters(self._connection.projects.get(project_name), parameter, sub_parameter, pretty_print, pretty_sort)

    def getBranches(self, project_name, raw, verbose, pretty_print, pretty_sort):
        if common.validateProjectName(project_name):
            try:
                project = self._connection.projects.get(project_name)
                branches = project.branches.list()
                for b in branches:
                    self.__outputResultsList(raw, b, not verbose, pretty_print, pretty_sort, False)

            except Exception as e:
                raise click.ClickException(e)

    def getUsers(self, username, output_username, raw, verbose, pretty_print, pretty_sort):
        try:
            users = self._connection.users.list(username=username)
            for u in users:
                if output_username:
                    output_parameter = "username"
                else:
                    output_parameter = "placeholder"

                self.__outputResultsList(raw, u, not verbose, pretty_print, pretty_sort, output_parameter)

        except Exception as e:
            raise click.ClickException(e)


    def getUser(self, username, parameter, pretty_print, pretty_sort):
        try:
            self.__printParameters(self._connection.users.list(username=username)[0], parameter, None, pretty_print, pretty_sort)

        except Exception as e:
            raise click.ClickException(e)


    def getGroups(self, group_name, get_path, verbose, raw, pretty_print, pretty_sort):
        try:
            if get_path:
                output_parameter = "path"
            else:
                output_parameter = "placeholder"

            if group_name == None:
                groups = self._connection.groups.list()
                for g in groups:
                    self.__outputResultsList(raw, g, not verbose, pretty_print, pretty_sort, output_parameter)
            else:
                groups = self._connection.groups.get(group_name)
                self.__outputResultsList(raw, groups, not verbose, pretty_print, pretty_sort, output_parameter)

        except Exception as e:
            raise click.ClickException(e)

    def getGroup(self, group_name, parameter, pretty_print, pretty_sort):
        try:
            self.__printParameters(self._connection.groups.get(group_name), parameter, None, pretty_print, pretty_sort)

        except Exception as e:
            raise click.ClickException(e)
