#!/usr/bin/python3

import gitlab,os
from . import _GitlabCTLCreate

class GitlabCTL(_GitlabCTLCreate.Mixin):

    def __init__(self, url, token):
        self._url = self.__defineGitlabUrl(url)
        self._token = self.__defineGitlabToken(token)

        self._connection = self.__performConnection()


    def __performConnection(self):
        return gitlab.Gitlab(self._url, private_token=self._token)


    def __defineGitlabToken(self, token):
        if token == None:
            return os.environ.get('GLABCTL_TOKEN')
        else:
            return token


    def __defineGitlabUrl(self, url):
        if url == None:
            return os.environ.get('GLABCTL_URL')
        else:
            return url

