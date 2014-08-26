Crowdin-cli-py
==============


A client for the `Crowdin`_ API which lets you upload sources and translations to
crowdin and download translated content.

.. _Crowdin: http://crowdin.com/

Installation
------------

::

    (sudo) pip install crowdin-cli-py

If you don't have ``pip``::

    (sudo) easy_install pip
    (sudo) pip install crowdin-cli-py
	

Configuration
-------------

When the tool is installed, you would have to configure your project. Basically, `crowdin-cli` go through project directory, and looks for `crowdin.yaml` file that contains project information.

Create `crowdin.yaml` YAML file in your root project directory with the following structure:

```
project_identifier: test
api_key: KeepTheAPIkeySecret
base_path: /path/to/your/project

files:
  -
    source: /locale/en/LC_MESSAGES/messages.po
    translation: /locale/%two_letters_code%/LC_MESSAGES/%original_file_name%
```

* `api_key` - Crowdin Project API key
* `project_identifier` - Crowdin project name
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
      * `%original_path%` - Take parent folders names in Crowdin project to build file path in resulted bundle
      * `%file_extension%` - Original file extension
      * `%file_name%` - File name without extension
	  
Usage
-----

When the configuration file is created, you are ready to start using `crowdin-cli` to manage your localization resources and automate files synchronization.

We listed most typical commands that crowdin-cli is used for:

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