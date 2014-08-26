# -*- coding: utf-8 -*-
import json
import os
import re
import logging
import yaml
import requests


LOCATION_TO_CONFIGURATION_FILE = 'crowdin.yaml'

logger = logging.getLogger('crowdin')


class CliException(Exception):
    pass


class Configuration(object):
    def __init__(self):

        # reading configuration file
        try:
            fh = open(LOCATION_TO_CONFIGURATION_FILE, "r")
            config = yaml.load(fh)
        except(OSError, IOError) as e:
            print e, "\n Please check your config file"
            exit()

        else:

            fh.close()

            # assigning configuration values
            # print "Reading configuration from the file was successful"
            if config['project_identifier']:
                self.project_identifier = config['project_identifier']
            else:
                print "project_identifier is required in config file."
                exit()
            if config['api_key']:
                self.api_key = config['api_key']
            else:
                print "api_key is required in config file."
                exit()

            self.base_url = 'https://api.crowdin.com'
            if config['base_path']:
                #print config['base_path']
                self.base_path = config['base_path']
            else:
                self.base_path = os.getcwd()
            # self.files_source = config['files'][0]['source']
            if config['files']:
                self.files_source = config['files']
            else:
                print "You didn't set any files in your config. It's very sad."



    def get_project_identifier(self):
        return self.project_identifier

    def get_api_key(self):
        return self.api_key

    def get_base_url(self):
        return self.base_url

    def get_base_path(self):
        return self.base_path

    def get_files_source(self):
        sources = []
        for f in self.files_source:
            sources.append(f['source'])
            sources.append(f['translation'])
        return sources

    def android_locale_code(self, locale_code):
        if locale_code == "he-IL":
            locale_code = "iw-IL"
        elif locale_code == "yi-DE":
            locale_code = "ji-DE"
        elif locale_code == "id-ID":
            locale_code = "in-ID"
        return locale_code.replace('-', '-r')

    def osx_language_code(self, locale_code):
        if locale_code == "zh-TW":
            locale_code = "zh-Hant"
        elif locale_code == "zh-CN":
            locale_code = "zh-Hans"
        return locale_code.replace('-', '_')

    def export_pattern_to_path(self, lang):
        translation = {}
        lang_info = []
        for value in self.files_source:
            translation = {}
            for l in lang:
                path = value['source']
                if '/' in path:
                    original_file_name = path[1:][path.rfind("/"):]
                    file_name = path[1:][path.rfind("/"):].split(".")[0]
                    original_path = path[:path.rfind("/")]
                else:
                    original_file_name = path
                    original_path = ''
                    file_name = path.split(".")[0]

                file_extension = path.split(".")[-1]

                pattern = {
                    '%original_file_name%': original_file_name,
                    '%original_path%': original_path,
                    '%file_extension%': file_extension,
                    '%file_name%': file_name,
                    '%language%': l['name'],
                    '%two_letters_code%': l['iso_639_1'],
                    '%three_letters_code%': l['iso_639_3'],
                    '%locale%': l['locale'],
                    '%crowdin_code%': l['crowdin_code'],
                    '%locale_with_underscore%': l['locale'].replace('-', '_'),
                    '%android_code%': self.android_locale_code(l['locale']),
                    '%osx_code%': self.osx_language_code(l['crowdin_code']) + '.lproj',
                }

                path_lang = value['translation']
                rep = dict((re.escape(k), v) for k, v in pattern.iteritems())
                patter = re.compile("|".join(rep.keys()))
                text = patter.sub(lambda m: rep[re.escape(m.group(0))], path_lang)
                if not text in translation:
                    translation[l['crowdin_code']] = text

                if not path in lang_info:
                    lang_info.append(path)
                    lang_info.append(translation)
        return lang_info


class Connection(Configuration):
    def __init__(self, url, params, api_files=None):
        super(Connection, self).__init__()
        self.url = url
        self.params = params
        self.files = api_files

    def connect(self):
        valid_url = self.base_url + self.url['url_par1']
        if self.url['url_par2']: valid_url += self.get_project_identifier()
        valid_url += self.url['url_par3']
        if self.url['url_par4']: valid_url += '?key=' + self.get_api_key()

        response = requests.request(self.url['post'], valid_url, data=self.params, files=self.files)
        if response.status_code != 200:
            return result_handling(response.text)
        # raise CliException(response.text)
        else:
            # logger.info("Operation was successful")
            return response.content
            #return response.text


def result_handling(self):
    data = json.loads(self)
    # msg = "Operation was {0}".format()
    if data["success"] is False:
        # raise CliException(self)
        logger.info("Operation was unsuccessful")
        print "Error code: {0}. Error message: {1}".format(data["error"]["code"], data["error"]["message"])