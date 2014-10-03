# -*- coding: utf-8 -*-
from connection import Connection, Configuration
import logging
import json
import zipfile
import io
import os

logger = logging.getLogger('crowdin')


class Methods:
    def __init__(self, any_options, options_config):
        # Get options arguments from console input
        self.any_options = any_options
        #Get parsed config file
        self.options_config = options_config

    # Main connection method to interact with connection.py
    def true_connection(self, url, params, api_files=None):
        return Connection(self.options_config, url, params, api_files, self.any_options).connect()

    def get_info(self):
        # POST https://api.crowdin.com/api/project/{project-identifier}/info?key={project-key}
        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/info', 'url_par4': True}
        params = {'json': 'json'}
        data = json.loads(self.true_connection(url, params))

        return data['files']

    def get_info_lang(self):
        # POST https://api.crowdin.com/api/project/{project-identifier}/info?key={project-key}
        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/info', 'url_par4': True}
        params = {'json': 'json'}

        data = json.loads(self.true_connection(url, params))
        #for key, value in data.iteritems():
        #    if key == "languages":
        #        print value[]
        return data['languages']

    def lang(self):
        languages_list = []
        data = json.loads(self.supported_languages())
        my_lang = self.get_info_lang()
        for i in data:
            for l in my_lang:
                if i['crowdin_code'] == l['code']:
                    languages_list.append(i)
        return languages_list

    #It'a awful function T_T
    #def exists(self, name):
    #   for f in name:
    #        for i in f.split():
    #            yield i

    #def list_sources(self):
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
        return self.true_connection(url, params)

    def upload_files(self, files, export_patterns, parameters, item):
        # POST https://api.crowdin.com/api/project/{project-identifier}/add-file?key={project-key}
        logger.info("Uploading source file: {0}".format(item))

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/add-file', 'url_par4': True}

        if item[0] == '/':
            sources = item[1:]
        else:
            sources = item

        params = {'json': json, 'export_patterns[{0}]'.format(sources): export_patterns,
                  'titles[{0}]'.format(sources): parameters.get('titles'),
                  'type': parameters.get('type'),
                  'first_line_contains_header': parameters.get('first_line_contains_header'),
                  'scheme': parameters.get('scheme'), 'translate_content': parameters.get('translate_content'),
                  'translate_attributes': parameters.get('translate_attributes'),
                  'content_segmentation': parameters.get('content_segmentation'),
                  'translatable_elements': parameters.get('translatable_elements'), 'file_name': item,
                  'action_type': "Uploading"}
        try:
            with open(files, 'rb') as f:
                api_files = {'files[{0}]'.format(sources): f}
                return self.true_connection(url, params, api_files)
        except(OSError, IOError) as e:
            print e, "\n Skipped"

    def update_files(self, files, export_patterns, parameters, item):
        # POST https://api.crowdin.com/api/project/{project-identifier}/update-file?key={project-key}
        logger.info("Updating source file: {0}".format(item))

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/update-file', 'url_par4': True}

        if item[0] == '/':
            sources = item[1:]
        else:
            sources = item

        params = {'json': json, 'export_patterns[{0}]'.format(sources): export_patterns,
                  'titles[{0}]'.format(sources): parameters.get('titles'),
                  'type': parameters.get('type'),
                  'first_line_contains_header': parameters.get('first_line_contains_header'),
                  'scheme': parameters.get('scheme'), 'translate_content': parameters.get('translate_content'),
                  'translate_attributes': parameters.get('translate_attributes'),
                  'content_segmentation': parameters.get('content_segmentation'),
                  'translatable_elements': parameters.get('translatable_elements'), 'file_name': item,
                  'action_type': "Updating"}
        try:
            with open(files, 'rb') as f:
                api_files = {'files[{0}]'.format(sources): f}
                #print files
                return self.true_connection(url, params, api_files)
        except(OSError, IOError) as e:
            print e, "\n Skipped"

    def upload_translations_files(self, translations, language, source_file, parameters):
        # POST https://api.crowdin.com/api/project/{project-identifier}/upload-translation?key={project-key

        logger.info("Uploading {0} translation for source file: {1}".format(language, source_file))

        url = dict(post='POST', url_par1='/api/project/', url_par2=True, url_par3='/upload-translation', url_par4=True)
        options_dict = vars(self.any_options)
        for k, v in options_dict.items():
            if v == False:
                options_dict[k] = "0"
            if v == True:
                options_dict[k] = "1"

        params = {'json': 'json', 'language': language,
                  'auto_approve_imported': options_dict.get('imported', '0'),
                  'import_eq_suggestions': options_dict.get('suggestions', '0'),
                  'import_duplicates': options_dict.get('duplicates', '0')}

        try:
            with open(translations, 'rb') as f:
                api_files = {'files[{0}]'.format(source_file): f}
                #print files
                return self.true_connection(url, params, api_files)
        except(OSError, IOError) as e:
            print e, "\n Skipped"

    def preserve_hierarchy(self, common_path):
        preserve_hierarchy = Configuration(self.options_config).preserve_hierarchy
        if preserve_hierarchy is False and common_path.count('/') >= 2:
            common_path = [s.replace(os.path.commonprefix(common_path)[:-1], '', 1) for s in common_path]
        return common_path

    def upload_sources(self, dirss=False):
        dirs = []
        files = []
        info1 = self.parse(self.get_info())
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

        all_info = Configuration(self.options_config).get_files_source()

        base_path = os.path.normpath(Configuration(self.options_config).get_base_path()) + os.sep
        common_path = self.preserve_hierarchy(all_info[::3])
        #sources_path = common_path
        translations_path = all_info[1::3]
        sources_parameters = all_info[2::3]

        #Creating directories
        for item in common_path:
            if '/' in item and not item[:item.rfind("/")] in dirs:
                items = item[:item.rfind("/")]
                #print items
                p = "/"
                l = items[1:].split("/")
                i = 0
                while i < len(l):
                    p = p + l[i] + "/"
                    i += 1
                    if not p in dirs:
                        dirs.append(p)
                        self.create_directory(p)

        #Uploading/updating files
        for item, export_patterns, true_path, parameters in zip(common_path, translations_path,
                                                                all_info[::3], sources_parameters):

            if parameters.get('dest'):
                if '/' in item:
                    items = item[item.rfind("/"):]
                    item = parameters.get('dest').join(item.rsplit(items, 1))
                else:
                    item = parameters.get('dest')
            if item[0] != '/':
                ite = "/" + item
            else:
                ite = item
            full_path = base_path.replace('\\', '/') + true_path

            if not ite in files:
                self.upload_files(full_path, export_patterns, parameters, item)
            else:
                self.update_files(full_path, export_patterns, parameters, item)
        if dirss:
            return dirs

    def upload_translations(self):
        info2 = Configuration(self.options_config).export_pattern_to_path(self.lang())
        base_path = os.path.normpath(Configuration(self.options_config).get_base_path()) + os.sep

        translations_language = info2[1::3]
        translations_path = self.preserve_hierarchy(info2[::3])
        translations_parameters = info2[2::3]

        for i, source_file, params in zip(translations_language, translations_path, translations_parameters):
            for language, item in i.iteritems():
                if params.get('dest'):
                    if '/' in item:
                        items = source_file[source_file.rfind("/"):]
                        source_file = params.get('dest').join(source_file.rsplit(items, 1))
                    else:
                        source_file = params.get('dest')
                full_path = base_path.replace('\\', '/') + item
                check_l_option = self.any_options.language
                if check_l_option:
                    if language == check_l_option:
                        self.upload_translations_files(full_path, language, source_file, params)
                else:
                    self.upload_translations_files(full_path, language, source_file, params)
                    #print item, language, source_file, params

    def supported_languages(self):
        # GET https://api.crowdin.com/api/supported-languages
        #logger.info("Getting supported languages list with Crowdin codes mapped to locale name and standardized codes.")
        url = {'post': 'POST', 'url_par1': '/api/', 'url_par2': False,
               'url_par3': 'supported-languages', 'url_par4': False}
        params = {'json': 'json'}
        return self.true_connection(url, params)

    def download_project(self):
        # GET https://api.crowdin.com/api/project/{project-identifier}/download/{package}.zip?key={project-key}
        self.build_project()
        base_path = os.path.normpath(Configuration(self.options_config).get_base_path()) + os.sep
        if self.any_options.dlanguage:
            lang = self.any_options.dlanguage
        else:
            lang = "all"
        url = {'post': 'GET', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/download/{0}.zip'.format(lang), 'url_par4': True}
        params = {'json': 'json'}

        # files that exists in archive and doesn't match current project configuration
        unmatched_files = []

        with zipfile.ZipFile(io.BytesIO(self.true_connection(url, params))) as z:
            #for i in self.exists(Configuration().get_files_source()):

            for structure in z.namelist():
                # if structure.endswith(i):
                #     # with open(os.path.join(i[1:][:i.rfind("/")], os.path.basename(structure)), 'wb') as f:
                #     #     f.write(z.read(structure))
                if not structure.endswith("/"):
                    logger.info("Download: {0}".format(structure))
                    z.extract(structure, base_path)
                    #         else:
                    #             unmatched_files.append(structure)
                    #
                    # if unmatched_files:
                    #     logger.info("Warning: Downloaded translations do not match current project "
                    #                  "configuration. Some of the resulted files will be omitted.")
                    #     print unmatched_files
                    # use export API method before to download the most recent translations


    def build_project(self):
        #GET https://api.crowdin.com/api/project/{project-identifier}/export?key={project-key}
        logger.info("Build ZIP archive with the latest translations ")

        url = {'post': 'POST', 'url_par1': '/api/project/', 'url_par2': True,
               'url_par3': '/export', 'url_par4': True}
        params = {'json': 'json'}
        data = json.loads(self.true_connection(url, params))
        if data["success"]["status"] == 'built':
            print "- OK"
        elif data["success"]["status"] == 'skipped':
            print "- Skipped"
            print "Warning: Export was skipped. Please note that this method can be invoked only once per 30 minutes."

    def list_project_files(self):
        #print self.any_options
        if self.any_options.sources == 'project':
            project_files = self.parse(self.get_info())
            for i in project_files:
                print i
        if self.any_options.sources == 'sources':
            sources_files = Configuration(self.options_config).get_files_source()
            for i in sources_files[::3]:
                print i
        if self.any_options.sources == 'translations':
            translations_file = Configuration(self.options_config).export_pattern_to_path(self.lang())
            for i in translations_file[1::3]:
                for key, value in i.iteritems():
                    print value

    def test(self):
        print Configuration(self.options_config).get_files_source()
