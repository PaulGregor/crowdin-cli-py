# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
try:
    from crowdin.__init__ import __version__
    from crowdin import methods
except ImportError:
    from __init__ import __version__
    import methods
import argparse
import gettext
import logging
import os
import sys
import yaml


class Main:
    def __init__(self):
        level = logging.INFO
        formatter = logging.Formatter('%(message)s')
        self.logger = logging.getLogger('crowdin')
        self.logger.setLevel(level)

        self.console = logging.StreamHandler()
        self.console.setLevel(level)
        self.console.setFormatter(formatter)

        self.logger.addHandler(self.console)

        l_dir = os.path.dirname(os.path.realpath(__file__)) + "/locales"

        loc = gettext.translation('cli', l_dir, languages=['en'])
        # _ = loc.ugettext
        _ = loc.gettext
        loc.install()

    def main(self):
        parser = argparse.ArgumentParser(prog='crowdin-cli-py', add_help=False, usage=argparse.SUPPRESS, formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=('''\
NAME:
    Crowdin-cli-py {0}

    This tool requires configuration file to be created.
    See https://crowdin.com/page/cli-tool#configuration-file for more details.

SYNOPSIS:
    crowdin-cli-py [global options] command [command option] [arguments...]

VERSION:
    {1}                                     ''').format(_("desc"), __version__))

        parser._optionals.title = 'GLOBAL OPTIONS'


        parser.add_argument('-c', '--config', action='store', metavar='', dest='config', help='- Project-specific configuration file')
        parser.add_argument('--identity', action='store', dest='identity', metavar='', help='- User-specific configuration file with '
                                                                                'API credentials')
        parser.add_argument('--version', action='version', version="%(prog)s {0}".format(__version__), help='- Display the program version')
        parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose', help='- Be verbose')
        parser.add_argument('--help', action='help', help='- Show this message')

        subparsers = parser.add_subparsers(title='COMMANDS', metavar='')

        # A help command
        help_parser = subparsers.add_parser('help', help='Shows a list of commands or help for one command')

        # A upload command
        upload_parser = subparsers.add_parser('upload', help='Upload files to the server')
        upload_parser.add_argument('sources', help='This argument uploads sources files', nargs='?')
        upload_parser.add_argument('translations',  help='This argument uploads translations files', nargs='?')
        upload_parser.add_argument('-l', '--language', action='store', metavar='', dest='language', help='- Defines the language translations should be uploaded to.')
        upload_parser.add_argument('-b', '--branch', action='store', metavar='', dest='branch', help='- Defines the brahcn should be uploaded to.')

        upload_parser.add_argument('--import-duplicates', action='store_const',  dest='duplicates', const='1', help='- Defines whether to add translation if there is the same translation previously added.')
        upload_parser.add_argument('--no-import-duplicates', action='store_false', dest='duplicates', help='- Defines whether to add translation if there is the same translation previously added.')

        upload_parser.add_argument('--import-eq-suggestions', action='store_const',  dest='suggestions', const='1', help='- Defines whether to add translation if it is equal to source string at Crowdin.')
        upload_parser.add_argument('--no-import-eq-suggestions', action='store_false',  dest='suggestions', help='- Defines whether to add translation if it is equal to source string at Crowdin.')

        upload_parser.add_argument('--auto-approve-imported', action='store_const',  dest='imported', const='1', help='- Mark uploaded translations as approved.')
        upload_parser.add_argument('--no-auto-approve-imported', action='store_false',  dest='imported', help='- Mark uploaded translations as approved.')

        upload_parser.set_defaults(func=self.upload_files)

        # A list command
        list_parser = subparsers.add_parser('list', help='List information about the files')
        list_parser.add_argument('sources', action='store', help='List information about the sources files in current '
                                                                 'project.', nargs='?')
        list_parser.add_argument('translations', action='store', help='List information about the translations '
                                                                      'files in current project.', nargs='?')
        list_parser.add_argument('project', action='store', help='List information about the files that already '
                                                                 'exists in current project', nargs='?')
        list_parser.add_argument('--tree', action='store_true', dest='tree', default=False, help='Built a tree like view')

        list_parser.set_defaults(func=self.list_files)

        # A download command
        download_parser = subparsers.add_parser('download', help='Download projects files')
        download_parser.add_argument('-l', '--language', action='store', metavar='', dest='dlanguage',
                                     help='- If the option is defined the '
                                        'translations will be downloaded for single specified language.'
                                        'Otherwise (by default) translations are downloaded for all languages')
        download_parser.add_argument('-b', '--branch', action='store', metavar='', dest='branch', help='- Defines the brahcn should be downloaded to.')

        download_parser.set_defaults(func=self.download_project)

        # A test command
        # test_parser = subparsers.add_parser('test', help='Test Crowdin project.')
        # test_parser.add_argument('dirname', action='store', help='New directory to create')
        # test_parser.set_defaults(func=self.test)

        if len(sys.argv) == 1 or "help" in sys.argv:
            if "upload" in sys.argv:
                upload_parser.print_help()
            elif "download" in sys.argv:
                download_parser.print_help()
            else:
                parser.print_help()
            sys.exit(1)

        # results = parser.parse_args()
        # print results.config

        if "upload" in sys.argv and not "sources" in sys.argv and not "translations" in sys.argv:
            upload_parser.print_help()
            sys.exit(1)
        if "list" in sys.argv and not "sources" in sys.argv and not "translations" in \
                sys.argv and not "project" in sys.argv:
            list_parser.print_help()
            sys.exit(1)
        # print args.identity
        # print "I'm method main"
        args = parser.parse_args()
        if args.verbose:
            self.logger.setLevel(logging.DEBUG)
            self.console.setLevel(logging.DEBUG)
            self.logger.addHandler(self.console)


        args.func(args)

    def test(self, test):
        return methods.Methods(test, self.open_file(test)).test()
    # Can't Take My Eyes Off You

    def upload_files(self, upload):
        # print(upload)
        if upload.sources == "sources":
            return methods.Methods(upload, self.open_file(upload)).upload_sources()
        if upload.sources == "translations":
            return methods.Methods(upload, self.open_file(upload)).upload_translations()

    def list_files(self, list_f):
        # print(list_f)
        return methods.Methods(list_f, self.open_file(list_f)).list_project_files()

    def download_project(self, download):
        # print(download)
        return methods.Methods(download, self.open_file(download)).download_project()

    def open_file(self, options_config):
        # reading configuration file
        location_to_configuration_file = 'crowdin.yaml'
        home = os.path.expanduser(b"~").decode(sys.getfilesystemencoding()) + "/.crowdin.yaml"

        if options_config.config:
            location_to_configuration_file = options_config.config
        if options_config.identity:
            home = options_config.identity
        try:
            fh = open(location_to_configuration_file, "r")
            try:
                config = yaml.load(fh)
            except yaml.YAMLError as e:
                print(e, '\n Could not parse YAML. '
                         'We were unable to successfully parse the crowdin.yaml file that you provided - '
                         'it most likely is not well-formed YAML. '
                         '\n Please check whether your crowdin.yaml is valid YAML - you can use '
                         'the http://yamllint.com/ validator to do this - and make any necessary changes to fix it.')
                exit()
            if os.path.isfile(home):
                fhh = open(home, "r")
                config_api = yaml.load(fhh)
                if config_api.get('api_key'):
                    config['api_key'] = config_api.get('api_key')
                if config_api.get('project_identifier'):
                    config['project_identifier'] = config_api.get('project_identifier')
                fhh.close()
            # print "I'M robot method open file"
            fh.close()
        except(OSError, IOError) as e:
            print(e, '\nCan''t find configuration file (default `crowdin.yaml`). Type `crowdin-cli-py help` '
                     'to know how to specify custom configuration file. \nSee '
                     'http://crowdin.com/page/cli-tool#configuration-file for more details')
            exit()
        else:
            if not config.get('base_path'):
                print("Warning: Configuration file misses parameter `base_path` that defines "
                      "your project root directory. Using current directory as a root directory.")
            return config

if __name__ == "__main__":
    Main().main()


def start_cli():
    Main().main()
