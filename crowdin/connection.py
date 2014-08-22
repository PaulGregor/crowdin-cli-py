# -*- coding: utf-8 -*-
import yaml, requests, json
import re
import logging

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
            self.project_identifier = config['project_identifier']
            self.api_key = config['api_key']
            self.base_url = 'https://api.crowdin.com'
            self.base_path = config['base_path']
            # self.files_source = config['files'][0]['source']
            self.files_source = config['files']
            

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

    def export_pattern_to_path(self, lang):
        translation = {}
        lang_info = []
        for l in lang:
            for value in self.files_source:
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
                    # '%android_code%'           ; android_locale_code(lang['locale']),
                    #'%osx_code%'               : osx_language_code(lang['crowdin_code']) + '.lproj',
                }


                path_lang = value['translation']
                rep = dict((re.escape(k), v) for k, v in pattern.iteritems())
                patter = re.compile("|".join(rep.keys()))
                text = patter.sub(lambda m: rep[re.escape(m.group(0))], path_lang)
                if not l['crowdin_code'] in translation:
                    translation[l['crowdin_code']]=text

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
            #logger.info("Operation was successful")
            return response.content
            #return response.text


def result_handling(self):
    data = json.loads(self)
    # msg = "Operation was {0}".format()
    if data["success"] is False:
        # raise CliException(self)
        logger.info("Operation was unsuccessful")
        print "Error code: {0}. Error message: {1}".format(data["error"]["code"], data["error"]["message"])