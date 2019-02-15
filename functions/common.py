#!/usr/bin/python

import gitlab,os

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

