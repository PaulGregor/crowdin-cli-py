# -*- coding: utf-8 -*-
__author__ = 'Comix'
import yaml, requests, json


LOCATION_TO_CONFIGURATION_FILE = 'crowdin.yaml'
ACCOUNT_KEY = ''
USER_NAME = ''


class Configuration(object):
    def __init__(self, conf_file, account_key=None):

        # reading configuration file
        try:
            fh = open(conf_file, "r")
            config = yaml.load(fh)
        except(OSError, IOError) as e:
            print e, "\n Please check your config file"
            exit()

        else:

            fh.close()

            #assigning configuration values
           # print "Reading configuration from the file was successful"
            self.project_identifier = config['project_identifier']
            self.api_key = config['api_key']
            self.base_url = config['base_url']
            self.base_path = config['base_path']
            self.files_source = config['files'][0]['source']

            self.account_key = account_key

    def get_project_identifier(self):
        return self.project_identifier

    def get_api_key(self):
        return self.api_key

    def get_base_url(self):
        return self.base_url

    def get_base_path(self):
        return self.base_path

    def get_account_key(self):
        return self.account_key


class Connection(Configuration):
    def __init__(self, url, params):
        super(Connection, self).__init__(LOCATION_TO_CONFIGURATION_FILE, ACCOUNT_KEY)
        self.url = url
        self.params = params

    def connect(self):
        valid_url = self.base_url + self.url['url_par1'] + self.get_project_identifier() + self.url['url_par3'] + '?key=' + self.get_api_key()

        f = requests.request(self.url['post'], valid_url,  data=self.params)
        return result_handling(f.text)


def result_handling(self):
    data = json.loads(self)
    #msg = "Operation was {0}".format()
    if data["success"] is False:

        return "Operation was unsuccessful. \nError code: {0}. Error message: {1}".format(data["error"]["code"], data["error"]["message"])
    else:

        return "Operation was successful"








