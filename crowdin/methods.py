# -*- coding: utf-8 -*-
from connection import Connection, Configuration
import logging
import json
import zipfile
import io
#import os

logger = logging.getLogger('crowdin')


class Methods:
    def get_info(self):
        # POST https://api.crowdin.com/api/project/{project-identifier}/info?key={project-key}
        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/info', 'url_par4': True}
        params = {'json': 'json'}
        data = json.loads(Connection(url, params).connect())

        return data['files']

    def get_info_lang(self):
        # POST https://api.crowdin.com/api/project/{project-identifier}/info?key={project-key}
        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/info', 'url_par4': True}
        params = {'json': 'json'}
        data = json.loads(Connection(url, params).connect())
        #for key, value in data.iteritems():
        #    if key == "languages":
        #        print value[]
        lang = []
        for langs in data['languages']:
            lang.append(langs)
        return lang

    def lang(self):
        languages_list = []
        data = json.loads(self.supported_languages())
        my_lang = self.get_info_lang()
        for i in data:
            for l in my_lang:
                if i['crowdin_code'] == l['code']:
                    languages_list.append(i)
        return languages_list




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

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/add-directory', 'url_par4': True}
        params = {'name': name, 'json': 'json'}
        return Connection(url, params).connect()


    def upload_files(self, files, export_patterns):
        # POST https://api.crowdin.com/api/project/{project-identifier}/add-file?key={project-key}

        logger.info("Uploading source file to remote directory: {0}".format(files))

        url = {'post': 'POST', 'url_par1': '/api/project/','url_par2': True,
               'url_par3': '/add-file', 'url_par4': True}
        # params = {'titles': kwargs['titles'], 'export_patterns': kwargs['export_patterns'],
        #           'type': kwargs['type'], 'json': json}

        if files[0] == '/':ff = files[1:]
        else: ff = files
        params = {'json': json, 'export_patterns[{0}]'.format(ff): export_patterns}
        try:
            with open(ff, 'rb') as f:
                api_files = {'files[{0}]'.format(ff): f}
                return Connection(url, params, api_files).connect()
        except(OSError, IOError) as e:
            print e, "\n Skipped"


    def update_files(self, files, export_patterns):
        # POST https://api.crowdin.com/api/project/{project-identifier}/update-file?key={project-key}

        logger.info("Updating source file in remote directory: {0}".format(files))

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/update-file', 'url_par4': True}

        if files[0] == '/' :ff = files[1:]
        else: ff = files
        params = {'json': json, 'export_patterns[{0}]'.format(ff): export_patterns}
        try:
            with open(ff, 'rb') as f:
                api_files = {'files[{0}]'.format(ff): f}
                #print files
                return Connection(url, params, api_files).connect()
        except(OSError, IOError) as e:
            print e, "\n Skipped"

    def upload_translations_files(self, translations, language, source_file):
        # POST https://api.crowdin.com/api/project/{project-identifier}/upload-translation?key={project-key

        logger.info("Uploading {0} translation for source file: {1}".format(language, source_file))

        url = dict(post='POST', url_par1='/api/project/', url_par2=True, url_par3='/upload-translation', url_par4=True)
        params = {'json': 'json', 'language': language, 'auto_approve_imported': 1}
        if translations[0] == '/': ff = translations[1:]
        else: ff = translations
        try:
            with open(ff, 'rb') as f:
                api_files = {'files[{0}]'.format(source_file): f}
                #print files
                return Connection(url, params, api_files).connect()
        except(OSError, IOError) as e:
            print e, "\n Skipped"

    def upload_sources(self, dirss=False):
        dirs = []
        files = []
        info1 = Methods().parse(Methods().get_info())
        for item in info1:

            p = "/"
            f = item[:item.rfind("/")]
            l = f[1:].split("/")
            i = 0
            while i < len(l):
                p = p + l[i] + "/"
                i += 1
                if not p in dirs:
                    dirs.append(p)

            if not item.endswith("/"):
                files.append(item)
        all_info = Configuration().get_files_source()
        info2 = self.exists(all_info[::2])
        for item, export_patterns in zip(info2, all_info[1::2]):
            if '/' in item and not item[:item.rfind("/")] in dirs:
                items = item[:item.rfind("/")]

                p = "/"
                l = items[1:].split("/")
                i = 0
                while i < len(l):
                    p = p + l[i] + "/"
                    i += 1
                    if not p in dirs:
                        dirs.append(p)
                        self.create_directory(p)
            if item[0] != '/': ite="/"+item
            else: ite = item

            if not ite in files:
                self.upload_files(item, export_patterns)
            else:
                self.update_files(item, export_patterns)
        if dirss:
            return dirs


    def upload_translations(self):
        info2 = Configuration().export_pattern_to_path(self.lang())
        dic_info = info2[1::2]
        for i, source_file in zip(dic_info, info2[::2]):
            for language, item in i.iteritems():
                self.upload_translations_files(item, language, source_file)
                #print item, language, source_file



    def supported_languages(self):
        # GET https://api.crowdin.com/api/supported-languages
        #logger.info("Getting supported languages list with Crowdin codes mapped to locale name and standardized codes.")
        url = {'post': 'POST', 'url_par1': '/api/', 'url_par2': False,
               'url_par3': 'supported-languages', 'url_par4': False}
        params = {'json': 'json'}
        return Connection(url, params).connect()

    def download_project(self):
        # GET https://api.crowdin.com/api/project/{project-identifier}/download/{package}.zip?key={project-key}
        logger.info("Downloading translations:")


        url = {'post': 'GET', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/download/all.zip', 'url_par4': True}
        params = {'json': 'json'}

        # files that exists in archive and doesn't match current project configuration
        unmatched_files = []

        with zipfile.ZipFile(io.BytesIO(Connection(url, params).connect())) as z:
            #for i in self.exists(Configuration().get_files_source()):

            for structure in z.namelist():
                    # if structure.endswith(i):
                    #     # with open(os.path.join(i[1:][:i.rfind("/")], os.path.basename(structure)), 'wb') as f:
                    #     #     f.write(z.read(structure))
                if not structure.endswith("/"):
                    logger.info("{0}".format(structure))
                    z.extract(structure)
        #         else:
        #             unmatched_files.append(structure)
        #
        # if unmatched_files:
        #     logger.info("Warning: Downloaded translations do not match current project "
        #                  "configuration. Some of the resulted files will be omitted.")
        #     print unmatched_files


#print Methods().upload_translations()



#Methods().upload_translations_files("/locale/sv/LC_MESSAGES/messages.pot", "Swedish")