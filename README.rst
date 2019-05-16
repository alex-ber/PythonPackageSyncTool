PythonPackageSyncTool
=======================

PythonPackageSyncTool is a Python utility to "fix" requirements.txt.

TODO

Getting Help
============
TODO

QuickStart
==========
#wget https://github.com/alex-ber/PythonPackageSyncTool/archive/master.zip -O master.zip; unzip master.zip; rm master.zip

pip3 install https://github.com/alex-ber/PythonPackageSyncTool/archive/master.zip#egg=python-package-sync-tool[tests]



===

python3 -m pip install https://github.com/alex-ber/PythonPackageSyncTool/archive/master.zip

cd /opt/anaconda3/lib/python3.7/site-packages/alexber/reqsync/data/

chmod 755 driver.py

./driver.py --add:some_new_package:1.0.0

This will add some_new_package with version 1.0.0 to the requirements-dest.txt

Note:

Semicolomn and not equal sign is used here due to Python limitaion of usage of equal sign in the value in the command line.

====

./driver.py --add:some_new_package:

Note:

Semicolomn add the end.

This will run quick check whether package is not in remove list.







====

python3 -m pip install . # only installs "required"

python3 -m pip install .[test] # installs dependencies for tests

====

From the directory with setup.py

python3 setup.py test #run all tests

pytest




Requirements
============

PythonPackageSyncTool requires the following modules.

* Python 3.7+

