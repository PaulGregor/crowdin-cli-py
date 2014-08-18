# -*- coding: utf-8 -*-
__author__ = 'Comix'
from connection import Connection, Configuration
import logging
import json
import os

logger = logging.getLogger('crowdin')



class Methods:


    def get_info(self):
        #POST https://api.crowdin.com/api/project/{project-identifier}/info?key={project-key}
        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par3': '/info'}
        params = {'json': 'json'}
        data = json.loads(Connection(url, params).connect())

        return data['files']

    def exists(self, name):

        for f in name:
            for i in f.split():
                yield i



    # def test(self, tre):
    #     for i in tre:
    #         print u'├─ ' + i['name']
    #         if isinstance(i, dict):
    #             item = self.test(i['files'])
    #             if item is not None:
    #                 return item
    #for index, elm in enumerate(f.split('/')):

    def parse(self, data, parent=''):
        if data is None or not len(data):
            yield parent + ('/' if data is not None and not len(data) else '')
        else:
            for node in data:
                for result in self.parse(
                        node.get('files'), parent + '/' + node.get('name')):
                    yield result


    def create_directory(self, name):
        # POST https://api.crowdin.net/api/project/{project-identifier}/add-directory?key={project-key}


        logger.info("Creating remote directory {0}".format(name))


        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par3': '/add-directory'}
        params = {'name': name, 'json': json}
        return Connection(url, params).connect()

    def upload_sources(self):
        dirs = []

        for item in Methods().parse(Methods().get_info()):
            l=[]
            p = "/"

            f = item[:item.rfind("/")]
            l = f[1:].split("/")
            i = 0
            while i < len(l):
                p = p + l[i] + "/"
                i = i + 1
                if not p in dirs:
                    dirs.append(p)


        for item in self.exists(Configuration().get_files_source()):
            if not item[:item.rfind("/")] in dirs:
                items = item[:item.rfind("/")]
                l=[]
                p = "/"
                l = items[1:].split("/")
                i = 0
                while i < len(l):
                    p = p + l[i] + "/"
                    i = i + 1
                    if not p in dirs:
                        self.create_directory(p)





                #self.create_directory(item[:item.rfind("/")])
       #print dirs






#Methods().upload_sources()
#Methods().create_directory("/locale/fr/LC_MESSAGES/")