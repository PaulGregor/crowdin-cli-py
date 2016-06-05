# Crowdin-cli-py --- 0.95.4
[![Build Status](https://travis-ci.org/PaulGregor/crowdin-cli.svg?branch=master)](https://travis-ci.org/PaulGregor/crowdin-cli)

[Crowdin Integration Utility Homepage](https://crowdin.com/page/cli-tool)
 | [Support](https://crowdin.com/contacts)
 | [crowdin.com Homepage](https://crowdin.com)

A Command-Line Interface to sync files between local computer/server and [Crowdin](https://crowdin.com).

It is cross-platform and can be run in a terminal (Linux, MacOS X) or in cmd.exe (Windows).

![ScreenShot](http://i.imgur.com/uZDUvPt.png)

> **WARNING**: This is a development version: It contains the latest changes, but may also have several known issues, including crashes and data loss situations. In fact, it may not work at all.

## Installation
###**Windows**:

[Download link](https://sourceforge.net/projects/crowdin/files/latest/download?source=files)

###**Ubuntu/Debian**:
```
(sudo) pip install crowdin-cli-py
```

If you don't have pip:
```
(sudo) apt-get install pip
(sudo) pip install crowdin-cli-py
```

## Configuration

When the tool is installed, you would have to configure your project. Basically, `crowdin-cli-py` go through project directory, and looks for `crowdin.yaml` file that contains project information.

Create `crowdin.yaml` YAML file in your root project directory with the following structure:

```
project_identifier: test
api_key: KeepTheAPIkeySecret
base_url: https://api.crowdin.com
base_path: /path/to/your/project

files:
  -
    source: /locale/en/LC_MESSAGES/messages.po
    translation: /locale/%two_letters_code%/LC_MESSAGES/%original_file_name%
```

* `api_key` - Crowdin Project API key
* `project_identifier` - Crowdin project name
* `base_url` - (default: https://api.crowdin.com)
* `base_path` - defines what directory have to be scaned(default: current directory)
* `files`
  * `source` - defines only files that should be uploaded as sources
  * `translation` - defines where translations should be placed after downloading (also the path have to be checked to detect and upload existing translations)

        Use the following placeholders to put appropriate variables into the resulting file name:
      * `%language%` - Language name (i.e. Ukrainian)
      * `%two_letters_code%` - Language code ISO 639-1 (i.e. uk)
      * `%three_letters_code%` - Language code ISO 639-2/T (i.e. ukr)
      * `%locale%` - Locale (like uk-UA)
      * `%locale_with_underscore%` - Locale (i.e. uk_UA)
      * `%original_file_name%` - Original file name
      * `%android_code%` - Android Locale identifier used to name "values-" directories
      * `%original_path%` - Take parent folders names in Crowdin project to build file path in resulted bundle
      * `%file_extension%` - Original file extension
      * `%file_name%` - File name without extension
	  * `%osx_code%` - OS X Locale identifier used to name ".lproj" directories
      * `%osx_xliff%` - OS X Locale used to name xliff files (i.e. uk.xliff)

         Example for Android projects:
          ```
          /values-%android_code%/%original_file_name%
          ```
         Example for Gettext projects:
          ```
          /locale/%two_letters_code%/LC_MESSAGES/%original_file_name%
          ```

Also you can add and upload all directories matching the pattern, including all nested files and localizable files.

Configuration example provided above has 'source' and 'translation' attributes containing standard wildcards (also known as globbing patterns) to make it easier to work with multiple files.

Here's patterns you can use:

* `*` (asterisk)

 Match zero or more characters in file name. A glob consisting of only the asterisk and no other characters will match all files in the directory. If you specified a `*.json` it will include all files like `messages.json`, `about_us.json` and anything that ends with `.json`.c* will match all files beginning with c; `*c` will match all files ending with c; and `*c*` will match all files that have c in them (including at the beginning or end). Equivalent to `/ .* /x` in regexp.

* `**` (doubled asterisk)

 Match all the directories recursively. Note that you can use `**` in `source` and in `translation` pattern. When using `**` in `translation` pattern it will always contain sub-path from `source` for certain file. The mask `**` can be used only once in the pattern and must be surrounded by backslashes `/`.

* `?` (question mark)

 Matches any one character.

* `[set]`

 Matches any one character in set. Behaves exactly like character sets in `Regexp`, including set negation (`[^a-z]`).

* `\` (backslash)

 Escapes the next metacharacter.

 Say, you can have source: `/en/**/*.po` to upload all `*.po` files to Crowdin recursively. `translation` pattern will be `/translations/%two_letters_code%/**/%original_file_name%'`.

See sample configuration below::
```
---
project_identifier: test
api_key: KeepTheAPIkeySecret
base_url: https://api.crowdin.com
base_path: /path/to/your/project

files:
  -
    source: /locale/en/**/*.po
    translation: /locale/%two_letters_code%/**/%original_file_name%
```

### API Credentials from environment variables

You could load the API Credentials from an environment variable, e.g.

```
api_key_env: 'CROWDIN_API_KEY'
project_identifier_env: 'CROWDIN_PROJECT_ID'

```

If mix, `api_key` and `project_identifier` have priority:

```
api_key_env: CROWDIN_API_KEY            # Low priority
project_identifier_env: CROWDIN_PROJECT # Low priority
api_key: xxx                            # High priority
project_identifier: yyy                 # Hight priority
```

### Split project configuration and user credentials

The `crowdin.yaml` file contains project-specific configuration and user credentials(`api_key`, `project_identifier`).
This means that you can't commit this file in the code repository, because the API key would leak to other users. `crowdin-cli` allow 2 configuration files:

* a project-specific, residing in the project directory (required)
* a user-specific, probably residing in `$HOME/.crowdin.yaml` (optional)

**NOTE**: user credentials in user-specific configuration file is higher priority than project-specific.

### Languages mapping

Often software projects have custom names for locale directories. `crowdin-cli` allows you to map your own languages to understandable by Crowdin.

Let's say your locale directories named 'en', 'uk', 'fr', 'de'. All of them can be represented by `%two_letters_code%` placeholder. Still, you have one directory named 'zh_CH'. In order to make it work with `crowdin-cli` without changes in your project you can add `languages_mapping` section to your files set. See sample configuration below:

```
---
project_identifier: test
api_key: KeepTheAPIkeySecret
base_url: https://api.crowdin.com
base_path: /path/to/your/project

files:
  -
    source: /locale/en/**/*.po
    translation: /locale/%two_letters_code%/**/%original_file_name%
    languages_mapping:
      two_letters_code:
        # crowdin_language_code: local_name
        ru: ros
        uk: ukr
```
Mapping format is the following: `crowdin_language_code : code_use_use`.

Check [complete list of Crowdin language codes](https://crowdin.com/page/api/language-codes) that can be used for mapping.

You can also override language codes for other placeholders like `%android_code%`, `%locale%` etc...

### Ignoring directories

From time to time there are files and directories you don't want translate on Crowdin.
Local per-file rules can be added to the config file in your project.

```
files:
  -
    source: /locale/en/**/*.po
    translation: /locale/%two_letters_code%/**/%original_file_name%
    ignore:
      - /locale/en/templates
      - /locale/en/**/test-*.po
      - /locale/en/**/[^abc]*.po

```

### Preserving directories hierarchy

By default CLI tool tries to optimize your Crowdin project hierarchy and do not repeats complete path of local files online.
In case you need to keep directories structure same at Crowdin and locally you can add `preserve_hierarchy: true` option in main section of the configuration file.

Configuration sample is below:

```
---
project_identifier: test
api_key: KeepTheAPIkeySecret
base_url: https://api.crowdin.com
base_path: /path/to/your/project
preserve_hierarchy: true
```

### Uploading CSV files via API

```
---
project_identifier: test
api_key: KeepTheAPIkeySecret
base_url: https://api.crowdin.com
base_path: /path/to/your/project

files:
  -
   source: '/*.csv'
   translation: '%two_letters_code%/%original_file_name%'
   # Defines whether first line should be imported or it contains columns headers
   first_line_contains_header: true
   # Used only when uploading CSV file to define data columns mapping.
   scheme: "identifier,source_phrase,translation,context,max_length"
```

#### Multicolumn CSV

In case CSV file contains translations to all target languages you can use per-file option `multilingual_spreadsheet`.

CSV file example:
```
identifier,source_phrase,context,Ukrainian,Russian,French
ident1,Source 1,Context 1,,,
ident2,Source 2,Context 2,,,
ident3,Source 3,Context 3,,,
```

Configuration file example:
```
files:
  -
    source: multicolumn.csv
    translation: multicolumn.csv
    first_line_contains_header: true
    scheme: "identifier,source_phrase,context,uk,ru,fr"
    multilingual_spreadsheet: true

```


## Configurations Examples

### GetText Project

```
---
project_identifier: test
api_key: KeepTheAPIkeySecret
base_url: https://api.crowdin.com
base_path: /path/to/your/project

files:
  -
    source: '/locale/en/**/*.po'
    translation: '/locale/%two_letters_code%/LC_MESSAGES/%original_file_name%'
    languages_mapping:
      two_letters_code:
        'zh-CN': 'zh_CH'
        'fr-QC': 'fr'
```

### Android Project

```
---
project_identifier: test
api_key: KeepTheAPIkeySecret
base_url: https://api.crowdin.com
base_path: /path/to/your/project

files:
  -
   source: '/res/values/*.xml'
   translation: '/res/values-%android_code%/%original_file_name%'
   languages_mapping:
     android_code:
       # we need this mapping since Crowdin expects directories
       # to be named like "values-uk-rUA"
       # acording to specification instead of just "uk"
       de: de
       ru: ru
```

## Usage

When the configuration file is created, you are ready to start using `crowdin-cli-py` to manage your localization resources and automate files synchronization.

We listed most typical commands that crowdin-cli-py is used for:

Upload your source files to Crowdin:
```
$ crowdin-cli-py upload sources
```

Upload existing translations to Crowdin project (translations will be synchronized):
```
$ crowdin-cli-py upload translations
```

Download latest translations from Crowdin:
```
$ crowdin-cli-py download
```

Build latest Crowdin project configuration:
```
$ crowdin-cli-py build
```

List information about the files that already exists in current project:
```
$ crowdin-cli-py list project
```

List information about the sources files in current project that match the wild-card pattern:
```
$ crowdin-cli-py list sources
```

List information about the translations files in current project that match the wild-card pattern:
```
$ crowdin-cli-py list translations
```

By default, `list` command print a list of all the files


Get help on `upload` command:
```
$ crowdin-cli-py -h upload
```


Use `help` or `-h` provided with an application to get more information about available commands and options.


## Supported Pythons

Tested with the following Python versions:

- Python 2.6
- Python 2.7
- Python 3.2+

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## Changelog
**Version 0.95.4** - 25.04.2016:

* Added branches support see https://support.crowdin.com/articles/versions-management/

**Version 0.95.3** - 20.04.2016:

* During download process directories for translations file will be created if not exist.

**Version 0.95.2** - 19.11.2015:

* Error with finding translations files path on Python 2.7 have been fixed.

**Version 0.95.1** - 04.03.2015:

* Errors with non-ascii characters and troubles with import have been fixed.
	
**Version 0.94.5** - 28.02.2015:

* Support for Python 3.2+ was implemented.
* Environment variable for API Credentials.

## License and Author

Author: Paul Gregor (comixan@gmail.com)

Copyright: 2012-2014 [crowdin.com](https://crowdin.com/)

This project is licensed under the MIT license, a copy of which can be found in the LICENSE file.

       # acording to specification instead of just 
