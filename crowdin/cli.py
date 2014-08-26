import argparse
import gettext
import methods
import logging
import os


def Main():
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

    parser = argparse.ArgumentParser(description=_("desc"), )

    subparsers = parser.add_subparsers(help='commands')

    # A upload command
    upload_parser = subparsers.add_parser('upload', help='Upload filles to the server')
    upload_parser.add_argument('sources', action='store', help='Sources filles', nargs='?')
    upload_parser.add_argument('translations', action='store', help='Translations filles', nargs='?')

    upload_parser.set_defaults(func=upload_files)


    # A download command
    download_parser = subparsers.add_parser('download', help='Download projects files')

    download_parser.set_defaults(func=download_project)



    # A create command
    create_parser = subparsers.add_parser('create', help='Add directory to Crowdin project.')
    create_parser.add_argument('dirname', action='store', help='New directory to create')

    create_parser.set_defaults(func=create_directory)

    args = parser.parse_args()
    args.func(args)


def create_directory(self):
    return methods.Methods().create_directory(self.dirname)


def upload_files(self):
    if self.sources == "sources":
        return methods.Methods().upload_sources()
    if self.sources == "translations":
        return methods.Methods().upload_translations()


    # print methods.Methods().upload_files(string.dirname, string.json, string.jsonp)


def download_project(self):
    return methods.Methods().download_project()

# if __name__ == "__main__":
#     Main()