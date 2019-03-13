#!/usr/bin/python


import gitlab,click,os
from functions import get,create,delete,update
from click_help_colors import HelpColorsGroup


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
main.add_command(delete.delete)
main.add_command(update.update)


if __name__ == "__main__":
    main()
