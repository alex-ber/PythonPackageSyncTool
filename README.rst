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



====

python3 -m pip install https://github.com/alex-ber/PythonPackageSyncTool/archive/master.zip

cd /opt/anaconda3/lib/python3.7/site-packages/alexber/reqsync/data/

Note: This is Path where you're actually install my utility, it can be different in your machine.

If you use venv it will look something like:

cd /opt/MyProject/venv/Lib/site-packages/alexber/reqsync

====

Alternatively you can create these file for yourself, named driver.py:

```python
   #!/usr/bin/python3

   import alexber.reqsync.app as app

   if __name__ == "__main__":
       app.main()

```

And create requirements-src.txt in the pip freeze format and put it near your script.

====

After you'll go to the directory with driver script (whether provided or that you've just written). Type


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

s