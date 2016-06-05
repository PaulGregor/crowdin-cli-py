# -*- coding: utf-8 -*-
from __future__ import division, print_function
try:
    from crowdin.__init__ import __version__
except ImportError:
    from __init__ import __version__
import six
import sys
import json
import os
import traceback
import re
import logging
import requests
import fnmatch


logger = logging.getLogger('crowdin')


class CliException(Exception):
    pass


class Configuration(object):
    def __init__(self, options_config):
        # print "__init__ configurations"
        config = options_config     # assigning configuration values

        # print "Reading configuration from the file was successful"
        if config.get('project_identifier_env'):
            self.project_identifier = os.environ.get(config.get('project_identifier_env'))
        elif config.get('project_identifier'):
            self.project_identifier = config['project_identifier']
        if self.project_identifier is None:
            print("Hey, it seems like project_identifier is missing in config file. "
                  "You need to fix it.")
            exit()
        if config.get('api_key_env'):
            self.api_key = os.environ.get(config.get('api_key_env'))
        elif config.get('api_key'):
            self.api_key = config['api_key']
        if self.api_key is None:
            print("Hey, it seems like api_key is missing in config file. "
                  "You need to fix it.")
            exit()
        if 'preserve_hierarchy' in config:
            # print config['base_path']
            if config['preserve_hierarchy'] == True or config['preserve_hierarchy'] == False:
                self.preserve_hierarchy = config['preserve_hierarchy']
            else:
                print("Parameter `preserve_hierarchy` allows values of True or False. \n")
        else:
            self.preserve_hierarchy = False
        if config.get('base_url'):
            self.base_url = config['base_url']
        else:
            self.base_url = 'https://api.crowdin.com'
        if config.get('base_path'):
            # print config['base_path']
            self.base_path = config['base_path']
        else:
            self.base_path = os.getcwd().decode(sys.getfilesystemencoding())
        # self.files_source = config['files'][0]['source']
        if config.get('files'):
            self.files_source = config['files']
        else:
            print("Configuration file misses required section `files`"
                  "\n See http://crowdin.com/page/cli-tool#configuration-file for more details")
            exit()

    def get_project_identifier(self):
        return self.project_identifier

    def get_api_key(self):
        return self.api_key

    def get_base_url(self):
        return self.base_url

    def get_base_path(self):
        return self.base_path

    def get_doubled_asterisk(self, f_sources):
        root = self.base_path.replace("\\", r'/')
        if '**' in f_sources:
            if f_sources[0] != '/':
                f_sources = '/' + f_sources
            items = root + f_sources[:f_sources.rfind("**")]
        else:
            items = root + f_sources[:f_sources.rfind('/')]
        dirs_after = f_sources[2:][f_sources.rfind("**"):]
        fg = dirs_after[:dirs_after.rfind("/")][1:]
        return root, items, fg

    # Method for getting parameters from configuration file.
    @staticmethod
    def metacharacter(name_filter):
        if name_filter.find('\\') > -1:
            r = name_filter.find('\\') + 1
            name_filter = name_filter.replace(
                name_filter[r], "[{0}]".format(name_filter[r])
            ).replace(name_filter[r-1], '')
        return name_filter

    def get_files_source(self):
        sources = []
        for f in self.files_source:
            f['source'] = f['source'].replace('^', '!')
            if f['source'].count('**') > 1:
                logger.info("Source pattern {0} is not valid. The mask `**` "
                            "can be used only once in the source pattern.".format(f['source']))
                exit()
            ignore_list = []
            parameters = {}

            if 'titles' in f:
                parameters['titles'] = f['titles']

            if 'type' in f:
                parameters['type'] = f['type']

            if 'translate_content' in f:
                parameters['translate_content'] = f['translate_content']

            if 'translate_attributes' in f:
                parameters['translate_attributes'] = f['translate_attributes']

            if 'content_segmentation' in f:
                parameters['content_segmentation'] = f['content_segmentation']

            if 'translatable_elements' in f:
                parameters['translatable_elements'] = f['translatable_elements']

            if 'update_option' in f:
                parameters['update_option'] = f['update_option']

            if 'first_line_contains_header' in f:
                parameters['first_line_contains_header'] = f['first_line_contains_header']

            if 'scheme' in f:
                parameters['scheme'] = f['scheme']

            if 'multilingual_spreadsheet' in f:
                parameters['multilingual_spreadsheet'] = f['multilingual_spreadsheet']

            if 'import_duplicates' in f:
                parameters['import_duplicates'] = f['import_duplicates']

            if 'import_eq_suggestions' in f:
                parameters['import_eq_suggestions'] = f['import_eq_suggestions']

            if 'auto_approve_imported' in f:
                parameters['auto_approve_imported'] = f['auto_approve_imported']

            if 'languages_mapping' in f:
                parameters['languages_mapping'] = f['languages_mapping']

            if 'dest' in f:
                parameters['dest'] = f['dest']

            if 'escape_quotes' in f:
                parameters['escape_quotes'] = f['escape_quotes']

            file_name = f['source'][1:][f['source'].rfind("/"):]
            if 'ignore' in f:
                for ign in f['ignore']:
                    if '*' in ign or '?' in ign or '[' in ign:
                        ign = ign.replace('^', '!')
                        root, items, fg = self.get_doubled_asterisk(ign)
                        # walk through folders and file in local directories
                        for dp, dn, filenames in os.walk(items):
                            for ff in filenames:
                                if fnmatch.fnmatch(ff, self.metacharacter(ign[ign.rfind('/'):][1:])):
                                    ignore_list.append(os.path.join(dp.replace(root, ''), ff).replace("\\", r'/'))
                    else:
                        ignore_list.append(ign.replace("\\", r'/'))

            root, items, fg = self.get_doubled_asterisk(f['source'])
            if '*' in file_name or '?' in file_name or '[' in file_name:
                    if '**' in f['source']:

                        for dp, dn, filenames in os.walk(items):
                            for ff in filenames:

                                if fnmatch.fnmatch(ff, self.metacharacter(f['source'][f['source'].rfind('/'):][1:])):
                                    if fg in dp.replace("\\", r'/'):
                                        fgg = ''
                                        if fg:
                                            fgg = '/' + fg
                                        value = os.path.join(dp.replace(root, ''), ff).replace("\\", r'/')

                                        if not [s for s in ignore_list if s in value]:
                                            sources.append(value)
                                            f['translation'] = f['translation'].replace("\\", r'/')
                                            fgg = fgg.replace("\\", r'/')
                                            items = items.replace("\\", r'/')
                                            dp = dp.replace("\\", r'/')
                                            sources.append(
                                                f['translation'].replace('**', dp.replace(items, '').replace(fgg, ''))
                                            )
                                            sources.append(parameters)

                    else:
                        # print items
                        for dp, dn, filenames in os.walk(items):
                            for ff in filenames:
                                # if os.path.splitext(ff)[1] == os.path.splitext(f['source'])[1]:
                                if fnmatch.fnmatch(ff, self.metacharacter(f['source'][f['source'].rfind('/'):][1:])):
                                    value = os.path.join(dp.replace(root, ''), ff).replace("\\", r'/')

                                    if not [s for s in ignore_list if s in value]:
                                        sources.append(value)
                                        sources.append(f['translation'])
                                        sources.append(parameters)
                            break

            elif '**' in f['source']:
                for dp, dn, filenames in os.walk(items):
                    for ff in filenames:
                        if ff == f['source'][f['source'].rfind('/'):][1:]:
                            if fg in dp.replace("\\", r'/'):
                                fgg = ''
                                if fg:
                                    fgg = '/' + fg
                                value = os.path.join(dp.replace(root, ''), ff).replace("\\", r'/')
                                if not [s for s in ignore_list if s in value]:
                                    sources.append(value)
                                    f['translation'] = f['translation'].replace("\\", r'/')
                                    fgg = fgg.replace("\\", r'/')
                                    items = items.replace("\\", r'/')
                                    dp = dp.replace("\\", r'/')
                                    sources.append(
                                        f['translation'].replace('**', dp.replace(items, '').replace(fgg, ''))
                                    )
                                    sources.append(parameters)

            else:
                if not [s for s in ignore_list if s in f['source']]:
                    sources.append(f['source'])
                    sources.append(f['translation'])
                    sources.append(parameters)
        if not sources:
            print('It seems that there are none files to upload. Please check your configuration')
        return sources

    @staticmethod
    def android_locale_code(locale_code):
        if locale_code == "he-IL":
            locale_code = "iw-IL"
        elif locale_code == "yi-DE":
            locale_code = "ji-DE"
        elif locale_code == "id-ID":
            locale_code = "in-ID"
        return locale_code.replace('-', '-r')

    @staticmethod
    def osx_language_code(locale_code):
        if locale_code == "zh-TW":
            locale_code = "zh-Hant"
        elif locale_code == "zh-CN":
            locale_code = "zh-Hans"
        return locale_code.replace('-', '_')

    def export_pattern_to_path(self, lang, download=None):
        # translation = {}
        lang_info = []
        get_sources_translations = self.get_files_source()
        for value_source, value_translation, translations_params in zip(get_sources_translations[::3],
                                                                        get_sources_translations[1::3],
                                                                        get_sources_translations[2::3]):
            translation = {}

            if '**' in value_translation:
                logger.info("Translation pattern `{0}` is not valid. The mask `**` "
                            "can't be used. When using `**` in 'translation' pattern it will always "
                            "contain sub-path from 'source' for certain file.".format(value_translation))

            for l in lang:
                path = value_source
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
                    '%osx_xliff%': self.osx_language_code(l['crowdin_code']) + '.xliff',
                }
                if not download:
                    if 'languages_mapping' in translations_params:
                        try:
                            for i in six.iteritems(translations_params['languages_mapping']):
                                if not i[1] is None:
                                    true_key = ''.join(('%', i[0], '%'))
                                    for k, v in six.iteritems(i[1]):
                                        if l['crowdin_code'] == k:
                                            for key, value in pattern.items():
                                                if key == true_key:
                                                    pattern[key] = v

                        # for i in translations_params['languages_mapping'].iteritems():
                        #     if not i[1] is None:
                        #         rep = dict((re.escape(k), v) for k, v in i[1].iteritems())
                        #         patter = re.compile("|".join(rep.keys()))
                        #         true_key = ''.join(('%', i[0], '%'))
                        #         for key, value in pattern.items():
                        #             if key == true_key:
                        #                 pattern[key] = patter.sub(lambda m: rep[re.escape(m.group(0))], value)

                        except Exception as e:
                            print(e, 'It seems that languages_mapping is not set correctly')
                            exit(1)
                m = re.search("%[a-z0-9_]*?%", value_translation)
                if m.group(0) not in pattern:
                    print('Warning: {} is not valid variable supported by Crowdin. See '
                          'http://crowdin.com/page/cli-tool#configuration-file for more details.'.format(m.group(0)))
                    exit()
                path_lang = value_translation
                rep = dict((re.escape(k), v) for k, v in six.iteritems(pattern))
                patter = re.compile("|".join(rep.keys()))
                text = patter.sub(lambda m: rep[re.escape(m.group(0))], path_lang)
                if text not in translation:
                    translation[l['crowdin_code']] = (text[1:] if text[:1] == '/' else text).replace('//', '/', 1)

                if path not in lang_info:
                    lang_info.append(path)
                    lang_info.append(translation)
                    lang_info.append(translations_params)
        return lang_info


class Connection(Configuration):
    def __init__(self, options_config, url, params,  api_files=None, any_options=None, additional_parameters=None):
        super(Connection, self).__init__(options_config)
        # print "__init__ connection"
        self.url = url
        self.params = params
        self.files = api_files
        self.any_options = any_options
        self.additional_parameters = additional_parameters

    def connect(self):
        valid_url = self.base_url + self.url['url_par1']
        if self.url['url_par2']:
            valid_url += self.get_project_identifier()
        valid_url += self.url['url_par3']
        if self.url['url_par4']:
            valid_url += '?key=' + self.get_api_key()
        headers = {
            'User-Agent': 'crowdin-cli-py v.{0}'.format(__version__),
        }
        try:
            logger.debug('Send request: \n{0} \n{1} \n{2} \n{3} \n{4} \n.'.format(
                self.url['post'], valid_url, self.params, self.files, headers
            ))
            response = requests.request(
                self.url['post'], valid_url, data=self.params, files=self.files, headers=headers
            )

        except requests.exceptions.ConnectionError as e:
            if self.any_options.verbose is True:
                traceback.print_exc()
            print("It seems that we have faced some connection problem. It's very sad, please make sure you "
                  "have access to internet.")
            logger.warning(e.args[0].reason)
            exit()
        else:
            try:
                if 'json' in response.headers['content-type']:
                    logger.debug(json.loads(response.text))
            except ValueError:
                pass
            if response.status_code != 200:
                return result_handling(response.text)
            # raise CliException(response.text)

            elif self.additional_parameters:
                data = json.loads(response.text)
                answer = 'skipped'

                # branch name handling
                branch = ''
                expected_file = self.additional_parameters.get("file_name")
                if self.params.get('branch'):
                    expected_file = self.params.get('branch') + '/' + expected_file
                    branch = ' in branch "' + self.any_options.branch + '"'

                if self.additional_parameters.get("action_type") != 'translations':
                    if not data.get('stats'):
                        if self.additional_parameters.get("file_name") in data["files"]:
                            answer = data["files"][self.additional_parameters.get("file_name")]
                    else:
                        answer = "OK"
                    logger.info("{0} source file{1}: {2} - {3}".format(
                        self.additional_parameters.get('action_type'),
                        branch, self.additional_parameters.get("file_name"), answer
                    ))
                else:
                    answer = data["files"][expected_file]
                    logger.info("Uploading {0} translation {1} for source file: {2} - {3}".format(
                        self.additional_parameters.get('t_l'), branch, self.additional_parameters.get("file_name"),
                        answer
                    ))
            else:

                return response.content
                # return response.text


def result_handling(self):
    print(self)
    data = json.loads(self)
    # msg = "Operation was {0}".format()
    if data["success"] is False:
        # raise CliException(self)
        logger.info("Operation was unsuccessful")
        print("Error code: {0}. Error message: {1}".format(data["error"]["code"], data["error"]["message"]))

        if data["error"]["code"] == '3':
            print("Seems Crowdin server API URL is not valid. Please check the "
                  "`api_key` parameter in the configuration file.")
        if data["error"]["code"] == '1':
            print("Seems Crowdin project  is not valid. Please check the "
                  "`project_identifier` parameter in the configuration file.")
        exit()
