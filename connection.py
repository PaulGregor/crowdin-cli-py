# -*- coding: utf-8 -*-
import yaml, requests, json
import logging

LOCATION_TO_CONFIGURATION_FILE = 'crowdin.yaml'
ACCOUNT_KEY = ''
USER_NAME = ''

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
            self.base_url = config['base_url']
            self.base_path = config['base_path']
            # self.files_source = config['files'][0]['source']
            self.files_source = config['files']
            self.account_key = ACCOUNT_KEY

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
        return sources

    def export_pattern_to_path(self, path, lang):
        translation = []
        original_file_name = path[1:][path.rfind("/"):]
        original_path = path[:path.rfind("/")]
        file_extension = path.split(".")[-1]
        file_name = path[1:][path.rfind("/"):].split(".")[0]

        pattern = {
            '%original_file_name%': original_file_name,
            '%original_path%': original_path,
            '%file_extension%': file_extension,
            '%file_name%': file_name,
            #'%language%': lang['name'],
            #'%two_letters_code%': lang['iso_639_1'],
            #'%three_letters_code%': lang['iso_639_3'],
            #'%locale%': lang['locale'],
            #'%locale_with_underscore%': lang['locale'].gsub('-', '_'),
            # '%android_code%'           ; android_locale_code(lang['locale']),
            #'%osx_code%'               : osx_language_code(lang['crowdin_code']) + '.lproj',
        }
        for f in self.files_source:
            text = f['translation']
            for i, j in pattern.iteritems():
                text = text.replace(i, j)
                #translation.append(text)
                #print text

        return original_file_name, original_path,  file_extension, file_name


class Connection(Configuration):
    def __init__(self, url, params, files=None):
        super(Connection, self).__init__()
        self.url = url
        self.params = params
        self.file = files

    def connect(self):
        valid_url = self.base_url + self.url['url_par1'] + self.get_project_identifier() + self.url[
            'url_par3'] + '?key=' + self.get_api_key()

        response = requests.request(self.url['post'], valid_url, data=self.params, files=self.file)
        if response.status_code != 200:
            return result_handling(response.text)
        # raise CliException(response.text)
        else:
            return response.content
            #return response.text


def result_handling(self):
    data = json.loads(self)
    # msg = "Operation was {0}".format()
    if data["success"] is False:
        # raise CliException(self)
        logger.info("Operation was unsuccessful")
        print "Error code: {0}. Error message: {1}".format(data["error"]["code"], data["error"]["message"])
    else:
        logger.info("Operation was successful")
        return self



print Configuration().export_pattern_to_path("/locale/fr/LC_MESSAGES/messages.po", "fr")




