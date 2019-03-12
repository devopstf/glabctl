#!/usr/bin/python

import gitlab,click,os,json
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from . import common

@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def delete():
    """Delete any element listed in 'Commands' section.

    Gitlab user permissions won't be violated. 
    You must use a token from an account that can delete the elements you want to!
    """
    pass

@delete.command('project', short_help="Delete a Project from Gitlab")
@click.option('--auto-confirm', '-y', required=False, is_flag=True, help="Enable auto confirm")
@click.option('--url', '-u',required=False, help='URL directing to Gitlab')
@click.option('--token', '-tk', required=False, help="Private token to access Gitlab")
@click.argument('project_name')
def deleteCommandProject(project_name, auto_confirm, url, token):
    """Delete a project from Gitlab.

    You must define the project in the form or '<group>/<project_name>' or It won't work!"""

    # Check if project name is the one we can use
    if(len(project_name.split('/')) != 2):
        click.echo('[' + click.style('ERROR', fg='red') + '] The project name should be defined as <group>/<project_name>.')
        return 1
    else:
        try:
            gl = common.performConnection(url, token)
 
            # Filtro para ver si existe el proyecto, si no existe, salta excepción y termina
            project = gl.projects.get(project_name)
            if not auto_confirm:
                click.echo('[' + click.style('WARNING', fg='yellow') + '] You are about to delete the project <' 
                           + click.style(project_name, fg='yellow') + '>')
                confirmation = input('Are you sure you want to do this? (y/n): ')
                if confirmation == 'y' or confirmation == 'yes':
                    project.delete()
                else:
                    click.echo('[' + click.style('TERMINATING...', fg='red') + '] You decided not to delete the project.')
                    return 1
            else:
                project.delete()
            
            click.echo('[' + click.style('OK', fg='green') + '] Project has been deleted successfuly')
            
        except Exception as e:
            raise click.ClickException(e)

@delete.command('this', short_help="In case of need...")
def deleteCommandThis():
    click.echo(click.style('     D E L E T E', fg='red'))
    print()
    print('         ^')
    print('         | |')
    print('       @#####@')
    print('     (###   ###)-.')
    print('   .(###     ###) \\')
    print('  /  (###   ###)   )')
    print(' (=-  .@#####@|_--"')
    print(' /\    \_|l|_/ (\\')
    print('(=-\     |l|    /')
    print(' \  \.___|l|___/')
    print(' /\      |_|   /')
    print('(=-\._________/\\')
    print(' \             /')
    print('   \._________/')
    print('     #  ----  #')
    print('     #   __   #')
    print('     \########/')
    print()
    click.echo(click.style('       T H I S', fg='red'))

