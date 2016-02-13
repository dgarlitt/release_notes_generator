# Release Notes Generator
***

### Setup
***

 - Clone your project
 - Clone your wiki
 - Clone this project
 - Edit the ```props.json``` file
    - Paths specified in this file can be absolute or relative and can optionally have a slash on the end
    - Update any regex patterns to fit your project needs


### Usage
***

The ```main.py``` script is the main script that triggers the generation of release notes. There is a props.json file in the same directory that can be used to configure the script to fit an individual's development environment. The main script can take one of two arguments.

To generate release notes for all release tags past to present, it can be run as:

```
./main.py all
```

To generate release notes for an individual release, run:

```
./main.py 1.2.3.4
```

where __1.2.3.4__ would be substituted for an individual release number.

Each time release notes are generated, the index file is updated to contain a link to the newly created release notes.

After the release notes are generated, the script will automatically add, commit and push the changes to the wiki.

Release notes are derived from the release tags in your git repository. It is assumed that release tags in your project contain the release's version number. A regex pattern can be specified to recognize your version numbers. Also, a __prefix__ and/or a __suffix__ can be set to identify release tags.

For instance, if the prefix is __project-v__ and the suffix is __-release__ and the version number pattern is __\\d.\\.\\d\\.\\d\\.\\d__, then the generator will find all tags matching the pattern:

```
project-v\d.\.\d\.\d\.\d-release
```

Therefore, you can conclude that the following tag names will match the pattern:

```
project-v1.2.3.4-release

project-v2.3.4.5-release

project-v3.4.5.6-release
```

### Running the unit tests
***

You will need the following python libraries installed to run the tests:

```
nose
mock
coverage
```

These can be installed either through [easy_install](https://pythonhosted.org/setuptools/easy_install.html) or [pip](https://pypi.python.org/pypi/pip). If you are using pip,
then simply run the following command from the same directory as ```main.py```:

```
pip install -r requirements.txt
```

To run the tests, ```cd``` into the ```scripts/release_notes_gen``` directory and then run:

```
nosetests --nocapture
```

To see a coverage report, run:

```
nosetests --nocapture --with-coverage --cover-erase --cover-package=lib
```
