import argparse
import gettext
import methods
import logging
import sys, os


level = logging.DEBUG
formatter = logging.Formatter('%(message)s')
logger = logging.getLogger('crowdin')
logger.setLevel(level)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)

logger.addHandler(console)


def create_directory(string):
    print methods.Methods().create_directory(string.dirname)


def upload_files(string):
    if string.sources == "sources":
        print methods.Methods().upload_sources()


        # print methods.Methods().upload_files(string.dirname, string.json, string.jsonp)


def download_project():
    print methods.Methods().download_project()


loc = gettext.translation('cli', 'locales', languages=['en'])
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


# A delete command
# delete_parser = subparsers.add_parser('delete', help='Remove a directory')
# delete_parser.add_argument('dirname', action='store', help='The directory to remove')
# delete_parser.add_argument('--recursive', '-r', default=False, action='store_true',
# help='Remove the contents of the directory, too',
#                            )
# create_parser.add_argument('--json', default=False, action='store_true',
#                            help='May not contain value. Defines that response should be in JSON format.',
# )
# create_parser.add_argument('--jsonp', default=False, action='store_true',
#                            help='Callback function name. Defines that response should be in JSONP format.',
# )






if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
    ## show values ##


    # if args == "version":
    #     print sys.stdout.write("crowdin-client 0.1\n" )

    # if args == "no way":
    #     level = logging.INFO
    #     formatter = logging.Formatter('%(levelname)s: %(message)s')
    # else:




    # if args.create == "install":
    #     print "You asked for installation"
    # else:
    #     print "usage: cli.py [-h]"