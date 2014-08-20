# -*- coding: utf-8 -*-
__author__ = 'Comix'
from connection import Connection, Configuration
import logging
import json
import os
import zipfile
import io

logger = logging.getLogger('crowdin')


class Methods:
    def get_info(self):
        # POST https://api.crowdin.com/api/project/{project-identifier}/info?key={project-key}
        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par3': '/info'}
        params = {'json': 'json'}
        data = json.loads(Connection(url, params).connect())

        return data['files']

    def get_info_lang(self):
        # POST https://api.crowdin.com/api/project/{project-identifier}/info?key={project-key}
        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par3': '/info'}
        params = {'json': 'json'}
        data = json.loads(Connection(url, params).connect())
        #for key, value in data.iteritems():
        #    if key == "languages":
        #        print value[]
        lang = []

        for langs in data['languages']:
            lang.append(langs)
        for key, value in data['details']['source_language'].iteritems():
            lang.append({key: value})
        return lang





    def exists(self, name):

        for f in name:
            for i in f.split():
                yield i


    # def test(self, tre):
    # for i in tre:
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


    def upload_files(self, file, **kwargs):
        # POST https://api.crowdin.com/api/project/{project-identifier}/add-file?key={project-key}

        logger.info("Uploading file to remote directory {0}".format(file))

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par3': '/add-file'}
        # params = {'titles': kwargs['titles'], 'export_patterns': kwargs['export_patterns'],
        #           'type': kwargs['type'], 'json': json}
        params = {'json': json}
        if file[0] == '/':ff = file[1:]
        else: ff = file
        with open(ff, 'rb') as f:
            files = {'files[{0}]'.format(ff): f}
            return Connection(url, params, files).connect()


    def update_files(self, file, kwargs=None):
        # POST https://api.crowdin.com/api/project/{project-identifier}/update-file?key={project-key}

        logger.info("Updating file to remote directory {0}".format(file))

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par3': '/update-file'}
        params = {'json': json}
        if file[0] == '/' :ff = file[1:]
        else: ff = file

        with open(ff, 'rb') as f:
            files = {'files[{0}]'.format(ff): f}
            #print files
            return Connection(url, params, files).connect()


    def upload_sources(self, dirss=False):
        dirs = []
        files = []

        for item in Methods().parse(Methods().get_info()):

            p = "/"
            f = item[:item.rfind("/")]
            l = f[1:].split("/")
            i = 0
            while i < len(l):
                p = p + l[i] + "/"
                i = i + 1
                if not p in dirs:
                    dirs.append(p)

            if not item.endswith("/"):
                files.append(item)

        for item in self.exists(Configuration().get_files_source()):
            if '/' in item and not item[:item.rfind("/")] in dirs:
                items = item[:item.rfind("/")]

                p = "/"
                l = items[1:].split("/")
                i = 0
                while i < len(l):
                    p = p + l[i] + "/"
                    i = i + 1
                    if not p in dirs:
                        dirs.append(p)
                        self.create_directory(p)
            if item[0] != '/': ite="/"+item
            else: ite = item

            if not ite in files:
                self.upload_files(item)
            else:
                self.update_files(item)
        if dirss:
            return dirs



            #self.create_directory(item[:item.rfind("/")])
            #print dirs


    def supported_languages(self):
        # GET https://api.crowdin.com/api/supported-languages
        logger.info("Getting supported languages list with Crowdin codes mapped to locale name and standardized codes.")


    def download_project(self):
        # GET https://api.crowdin.com/api/project/{project-identifier}/download/{package}.zip?key={project-key}
        logger.info("Downloading translations")

        url = {'post': 'GET', 'url_par1': '/api/project/', 'url_par3': '/download/all.zip'}
        params = {'json': 'json'}

        # files that exists in archive and doesn't match current project configuration
        unmatched_files = []

        with zipfile.ZipFile(io.BytesIO(Connection(url, params).connect())) as z:
            for i in self.exists(Configuration().get_files_source()):
                for structure in z.namelist():
                    if structure.endswith(i):
                        with open(os.path.join(i[1:][:i.rfind("/")], os.path.basename(structure)), 'wb') as f:
                            f.write(z.read(structure))
                        #z.extract(structure, i[1:][:i.rfind("/")])

                    else:
                        unmatched_files = structure

        if unmatched_files:
            logger.info("Warning: Downloaded translations do not match current project "
                         "configuration. Some of the resulted files will be omitted.")
            print unmatched_files


#for i in Methods().get_info_lang():
#    print i['name']

# Methods().create_directory("/locale/fr/LC_MESSAGES/")