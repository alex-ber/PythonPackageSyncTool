# Changelog
All notable changes to this project will be documented in this file.

\#https://pypi.org/manage/project/python-package-sync-tool/releases/

## [Unrelased]
Add test

+ --add=zzzzzzzzzzzzzzzzzz,
+ --add=awscli
+ --add=awscli,
+ --add=not_exists
+ --add=not_exists,
- --add=aaaaaaaaaaaaaaaaaaa
- Change assert to more thoroguh
- --remove=zzzzzzzzzzzzzzzzzz,
- --remove=awscli
- --remove=awscli,
- --remove=not_exists
- --remove=not_exists,
##
*   Test mutual exclusion

*   Test & fix use of buffer


##
## [0.3.1] 
- Added more detail assertion to integration tests.
- Add unit-test for non-sorted requirements-src.
- Add unit-test that check run with empty add and empty remvoe.
 


## [0.2.11] - 2019-05-22
- Dependency alex-ber-utils bumped up to 0.2.5.

## [0.2.8] - 2019-05-22
- Dependency alex-ber-utils bumped up to 0.2.4.

## [0.2.6] - 2019-05-22
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






