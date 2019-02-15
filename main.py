#!/usr/bin/python


import gitlab,click,os
from functions import create,get
from click_help_colors import HelpColorsGroup, HelpColorsCommand


def defineGitlabHost(url): # Simple checker for host
    if url:
        return url
    else:
        return os.environ.get('GITLABCTL_URL')


def defineGitlabToken(token): # Simple checker for private token
    if token:
        return token
    else:
        return os.environ.get('GITLABCTL_TOKEN')


def performConnection(url, token): # Gitlab connection function (url + private token)
    connection_host = defineGitlabHost(url)
    connection_token = defineGitlabToken(token)
    return gitlab.Gitlab(connection_host, private_token=connection_token)


@click.group(cls=HelpColorsGroup, help_headers_color='yellow', help_options_color='green')
def main(): # Main help & commands
    """A command-line tool to control Gitlab from its API.

    \b
    This tool can get, describe, create, modify or delete multiple
    Gitlab elements through the use of its API to provide an easy
    way to control your own Gitlab installation without the need
    of accessing It through a Web Browser!

    It might be useful for automated processes of a CI/CD pipeline
    or as a workaround for Tools which can't control Gitlab natively.
    """
    pass

# Build Click command
main.add_command(get.get)
main.add_command(create.create)

if __name__ == "__main__":
    main()
