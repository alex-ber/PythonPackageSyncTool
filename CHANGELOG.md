# Changelog
All notable changes to this project will be documented in this file.

\#https://pypi.org/manage/project/python-package-sync-tool/releases/



## [0.5.2rc2] - 2020-12-16
 **TODO: change documentation** (see below)

## [0.5.2rc1] - 2020-12-16
 

## [0.5.2a0] - 2020-11-17
### Removed
- `alexber.reqsync.utils.app_conf` removed.

### Changed
- Pytest version updated (also some tests dependencies changed)
- alex-ber-utils dependency updated.
- Logger information was moved from `app.py` to `config.yml` file.
- config.yml format changed to one that alex-ber-utils support for a long time.

See documentation here

My `parser` module [https://medium.com/analytics-vidhya/my-parser-module-429ed1457718]

My `ymlparsers` module [https://medium.com/analytics-vidhya/my-ymlparsers-module-88221edf16a6]

My major `init_app_conf` module [https://medium.com/analytics-vidhya/my-major-init-app-conf-module-1a5d9fb3998c]

- Logger is enabled, relative path is resolved correctly, and other little tweaks, see

Integrating Python’s logging and warnings packages 
[https://medium.com/analytics-vidhya/integrating-pythons-logging-and-warnings-packages-7ffd6f65e02d]

Making relative path to file to work 
[https://alex-ber.medium.com/making-relative-path-to-file-to-work-d5d0f1da67bf]
 
- config.xml - to remove package was added mkl*-related packagages and anaconda-specific packages.


### Added
- Optional Docker support added. **TODO: change documentation** 


## [0.5.1] - 2020-10-25
### Added
- Support for Python 3.8

### Changed
- 

## [0.4.3] - 2019-10-17
### Changed
- anaconda-navigator and conda-build added to config.yml.

## [0.4.2] - 2019-10-16
### Changed
- navigator-updater added to config.yml.

## [0.4.1] - 2019-05-30
### Changed
- Bug fix: adding packages before all existing one works incorrect.
- Removing alexber.reqsync.utils.parsers. It was fully duplicated by alexber.utils.parsers. 
So, all usage was change to the latest (part of alex-ber-utils).

##
## [0.3.1] - 2019-05-23
### Changed
- Bug fix: adding packages before all existing one works incorrect.

### Added
- Unit test for bug fix that check adding packages before all existing one.
- More detail assertion to integration tests.
- Unit-test for non-sorted requirements-src.
- Unit-test that check run with empty add and empty remvoe.
- Unit-test that check removing single package.
- Unit-test that check remove first package in requirements-src.
- Unit-test that check remove last package in requirements-src.
- Unit-test that check that empty lines in requirements-src are ignored.
- Unit-test that check correct usage of file input buffer and file output buffer.


## [0.2.11] - 2019-05-22
### Changed
- Dependency alex-ber-utils bumped up to 0.2.5.

## [0.2.8] - 2019-05-22
### Changed
- Dependency alex-ber-utils bumped up to 0.2.4.

## [0.2.6] - 2019-05-22
### Changed
- Dependency alex-ber-utils bumped up to 0.2.3.

## [0.2.5] - 2019-05-22
### Changed
- Fixed bug in setup.py, incorrect order between VERSION and UploadCommand (no tag was created on upload)
- Dependency alex-ber-utils bumped up to 0.2.2. 

## [0.2.4] - 2019-05-22
### Changed
- Adding dependency alex-ber-utils 0.2.1 to README.md.


## [0.2.3] - 2019-05-22
### Changed
- Upgrading urllib3, SQLAlchemy, pycrypto dependenies beacause of volnurabilities issues.

## [0.2.2] - 2019-05-22
### Changed
- Fixing python-package-sync-tool.
- Creating alias reqsync to python-package-sync-tool.
- Some minour fixed.


## [0.2.1] - 2019-05-22
### Changed
- Changing dependency version of alex-ber-utils to 0.2.1.


## [0.2.0] - 2019-05-22
### Changed
- Only bumping up version.

## [0.1.9] - 2019-05-22
### Changed
- Added alex-ber-utils as dependency. 
- Deleting old README-old.rst file.
- requirements-src.txt updated.
- Clarification added to README.md that alex_ber_utils should be installed first.
- formatting CHANGELOG.MD (minor fix)
- Added alternative of usage of python_package_sync_tool to README.md
- Fixing bug that --add is empty
- Factor out tests_data to seperate folder, use importlib.resources API.  
- Updated README-old.rst


## [0.1.8] - 2019-05-20
### Changed
- README.md change, key '-U' added to pip3 install.


## [0.1.7] - 2019-05-20
### Removed
- Some project cleanup.

### Changed
- CHANGELOG and REAMDE now use Markdown format.
- REAMDE totally rewritten.
- Fixing bugs in the core algorithm. Simplifying code.
- Fixing correct handling of package adding to the buttom of the list. 


## [0.1.6] - 2019-05-20
### Added
- `__init__.py` file added to alexber.reqsync.data.

## [0.1.5] - 2019-05-20
### Added
- Small tool to sync package from different machines.






