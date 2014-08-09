import argparse
import gettext
import methods


def create_directory(string):

    print methods.Methods().create_directory(string.dirname, string.json, string.jsonp)


def add_file(string):

    print methods.Methods().add_file(string.dirname, string.json, string.jsonp)




loc = gettext.translation('cli', 'locales', languages=['en'])
_= loc.ugettext
loc.install()


parser = argparse.ArgumentParser(description=_("desc"), )

subparsers = parser.add_subparsers(help='commands')

# A list command
list_parser = subparsers.add_parser('list', help='List contents')
list_parser.add_argument('dirname', action='store', help='Directory to list')

# A create command
create_parser = subparsers.add_parser('create', help='Add directory to Crowdin project.')
create_parser.add_argument('dirname', action='store', help='New directory to create')
create_parser.add_argument('--json', default=False, action='store_true',
                           help='May not contain value. Defines that response should be in JSON format.',
                           )
create_parser.add_argument('--jsonp', default=False, action='store_true',
                           help='Callback function name. Defines that response should be in JSONP format.',
                           )
create_parser.set_defaults(func=create_directory)


# Add file command
add_parser = subparsers.add_parser('addfiles', help='Add new file to Crowdin project.')
add_parser.add_argument('files', action='store', help='Files array that should be added to Crowdin project.')
add_parser.add_argument('--titles', default=False, action='store_true', help='An arrays of strings that defines titles for uploaded files.')
add_parser.add_argument('--export_patterns', default=False, action='store_true', help='An arrays of strings that defines names of resulted files.')
add_parser.add_argument('--type', default=False, action='store_true', help='')
add_parser.add_argument('--first_line_contains_header', default=False, action='store_true', help='')
add_parser.add_argument('scheme', action='store', help='')

add_parser.add_argument('--json', default=False, action='store_true',
                           help='May not contain value. Defines that response should be in JSON format.',
                           )
add_parser.add_argument('--jsonp', default=False, action='store_true',
                           help='Callback function name. Defines that response should be in JSONP format.',
                           )
add_parser.add_argument('--translate_content', default=1, action='store_true',
                           help='Defines whether to translate texts placed inside the tags. Acceptable values are: 0 or 1. Default is 1.',
                           )
add_parser.add_argument('--translate_attributes', default=1, action='store_true',
                           help='Defines whether to translate tags attributes. Acceptable values are: 0 or 1. Default is 1.',
                           )
add_parser.add_argument('--content_segmentation', default=1, action='store_true',
                           help='Defines whether to split long texts into smaller text segments.',
                           )
add_parser.add_argument('--translatable_elements', default=1, action='store_true',
                           help='This is an array of strings, where each item is the XPaths to DOM element that should be imported.',
                           )
add_parser.set_defaults(func=add_file)




# A rename command
rename_parser = subparsers.add_parser('rename', help='Rename directory or modify its attributes.')
rename_parser.add_argument('dirname', action='store', help='New directory to create')


# A delete command
delete_parser = subparsers.add_parser('delete', help='Remove a directory')
delete_parser.add_argument('dirname', action='store', help='The directory to remove')
delete_parser.add_argument('--recursive', '-r', default=False, action='store_true',
                           help='Remove the contents of the directory, too',
                           )


#parser.add_argument('-o','--output',help='Output file name', required=True)
args = parser.parse_args()
args.func(args)
## show values ##

# if args.create == "install":
#     print "You asked for installation"
# else:
#     print "usage: cli.py [-h]"