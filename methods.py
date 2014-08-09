# -*- coding: utf-8 -*-
__author__ = 'Comix'
from connection import Connection


class Methods:


    def create_directory(self, name, json, jsonp):
        # POST https://api.crowdin.net/api/project/{project-identifier}/add-directory?key={project-key}

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par3': '/add-directory'}
        params = {'name': name, 'json': json, 'jsonp': jsonp}
        return Connection(url, params).connect()
