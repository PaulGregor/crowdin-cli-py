# -*- coding: utf-8 -*-
from __init__ import __version__
import argparse
import gettext
import methods
import logging
import os
import sys
import yaml


class Main:
    def __init__(self):
        level = logging.DEBUG
        formatter = logging.Formatter('%(message)s')
        logger = logging.getLogger('crowdin')
        logger.setLevel(level)

        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(formatter)

        logger.addHandler(console)

        l_dir = os.path.dirname(os.path.realpath(__file__)) + "/locales"

        loc = gettext.translation('cli', l_dir, languages=['en'])
        _ = loc.ugettext
        loc.install()
        #print "__init__ cli"

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
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='- Be verbose')
        parser.add_argument('--help', action='help', help='- Show this message')

        subparsers = parser.add_subparsers(title='COMMANDS', metavar='')


        # A help command
        help_parser = subparsers.add_parser('help', help='Shows a list of commands or help for one command')


        # A upload command
        upload_parser = subparsers.add_parser('upload', help='Upload files to the server')
        upload_parser.add_argument('sources', action='store', help='This argument uploads sources files', nargs='?')
        upload_parser.add_argument('translations', action='store', help='This argument uploads translations files', nargs='?')
        upload_parser.add_argument('-l', '--language', action='store', metavar='', dest='language', help='- defines the language translations should be uploaded to.')

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
        download_parser.set_defaults(func=self.download_project)

        # A Build project command
        export_parser = subparsers.add_parser('build', add_help=False)
        export_parser.set_defaults(func=self.build_project)

        #A test command
        #test_parser = subparsers.add_parser('test', help='Test Crowdin project.')
        #test_parser.add_argument('dirname', action='store', help='New directory to create')
        #test_parser.set_defaults(func=self.test)

        if len(sys.argv) == 1 or "help" in sys.argv:
            parser.print_help()
            sys.exit(1)

        #results = parser.parse_args()
        #print results.config

        if "upload" in sys.argv and not "sources" in sys.argv and not "translations" in sys.argv:
            upload_parser.print_help()
            sys.exit(1)
        if "list" in sys.argv and not "sources" in sys.argv and not "translations" in \
                sys.argv and not "project" in sys.argv:
            list_parser.print_help()
            sys.exit(1)
        # print args.identity
        #print "I'm method main"
        args = parser.parse_args()
        args.func(args)

    def test(self, test):
        return methods.Methods(test, self.open_file(test)).test()
    #Can't Take My Eyes Off You

    def upload_files(self, upload):
        if upload.sources == "sources":
            return methods.Methods(upload, self.open_file(upload)).upload_sources()
        if upload.sources == "translations":
            return methods.Methods(upload, self.open_file(upload)).upload_translations()

    def list_files(self, list_f):
        return methods.Methods(list_f, self.open_file(list_f)).list_project_files()

    def download_project(self, download):
        return methods.Methods(download, self.open_file(download)).download_project()

    def build_project(self, build):
        return methods.Methods(build, self.open_file(build)).build_project()

    def open_file(self, options_config):
        # reading configuration file
        location_to_configuration_file = 'crowdin.yaml'
        home = os.path.expanduser("~") + "/.crowdin.yaml"

        if options_config.config:
            location_to_configuration_file = options_config.config
        if options_config.identity:
            home = options_config.identity
        try:
            fh = open(location_to_configuration_file, "r")
            config = yaml.load(fh)
            if os.path.isfile(home):
                fhh = open(home, "r")
                config_api = yaml.load(fhh)
                if config_api.get('api_key'):
                    config['api_key'] = config_api.get('api_key')
                if config_api.get('project_identifier'):
                    config['project_identifier'] = config_api.get('project_identifier')
                fhh.close()
            #print "I'M robot method open file"
            fh.close()
        except(OSError, IOError) as e:
            print e, "\n Please check your config file"
            exit()
        else:
            return config

#if __name__ == "__main__":
#    Main().main()


def start_cli():
    Main().main()