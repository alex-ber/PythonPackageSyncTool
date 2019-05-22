# Changelog
All notable changes to this project will be documented in this file.

\#https://pypi.org/manage/project/python-package-sync-tool/releases/

## [Unrelased]
- formatting CHANGELOG.MD (minor fix)
- Added alternative of usage of python_package_sync_tool to README.md
- Fixing bug that --add is empty
- Factor out tests_data to seperate folder, use importlib.resources API.  
- Updated README-old.rst


@ Enhanced test
@ Non-sorted requirements-src
@ Empty add and remove


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




## [0.2.0] - 2019-05-22
### Changed
- Added alex-ber-utils as dependency. 
- Deleting old README-old.rst file.

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






