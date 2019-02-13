#!/usr/bin/python

import gitlab
import click


def getProjects():
    projects = gl.projects.list()
    for i in projects:
        print(i.id)

gl = gitlab.Gitlab('http://localhost', private_token='77w9Sb_BDf_xRUW9WEan')

@click.group()
def main():
    pass

@click.group()
def get():
    pass

@get.command()
def projects():
    """List all projects in Gitlab"""
    projects = gl.projects.list()
    for p in projects:
        print(p.name)

@get.command()
@click.option('--team', required=True, default='Administrator', help="Team name to use")
@click.argument('project_name')
def branches(team, project_name):
    """List all branches in Project""" 
    project_full_name = team + '/' + project_name
    project = gl.projects.get(project_full_name)
    branches = project.branches.list()
    for b in branches:
        print(b.name)

main.add_command(get)

if __name__ == "__main__":
    main()
