import setuptools
from setuptools import setup
import os

import sys
from shutil import rmtree

NAME = 'python_package_sync_tool'
VERSION = '0.1.7'

base_dir = os.path.dirname(os.path.realpath(__file__))

def get_content(filename):
    with open(os.path.join(base_dir, filename)) as f:
        content = f.read().splitlines()
    return content

install_requires = get_content('requirements.txt')
tests_require = get_content('requirements-tests.txt')

extras = {
    #'ws': get_content('requirements-ws.txt'),
    'tests': tests_require
}

lnk_data = os.path.join('alexber', 'reqsync', 'data')

def my_rmtree(path, ignore_errors=False, onerror=None):
    try:
        rmtree(path, ignore_errors, onerror)
    except OSError:
        pass

#adapted from https://github.com/kennethreitz/setup.py/blob/master/setup.py
class UploadCommand(setuptools.Command):
    """Support setup.py upload."""
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print(f'\033[1m{s}\033[0m')

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.status('Removing previous builds...')
        # rm -rf build *.egg-info dist
        my_rmtree(os.path.join(base_dir, 'build'))
        my_rmtree(os.path.join(base_dir, 'f{NAME}.egg-info'))
        my_rmtree(os.path.join(base_dir, 'dist'))

        self.status('Building Source and Wheel distribution...')
        os.system(f'{sys.executable} setup.py sdist bdist_wheel')
        #os.system('python3 setup.py sdist bdist_wheel')

        self.status('Uploading the package to PyPI via Twine...')
        # python3 -m keyring set https://upload.pypi.org/legacy/ alex-ber
        os.system('twine upload dist/*')

        self.status('Pushing git tags...')
        os.system('git fetch')
        os.system('git commit -m "setup.py changed" setup.py')
        os.system(f'git tag -d v{VERSION}')
        os.system(f'git tag v{VERSION}')
        os.system(f'git push --delete origin v{VERSION}')
        os.system(f'git push origin tag v{VERSION}')
        #os.system('git push --tags')
        os.system('git push')

        sys.exit()





try:
    try:
        os.unlink(lnk_data)
    except OSError:
        pass
    try:
        os.symlink(os.path.join('..', '..', 'data'), lnk_data)
    except OSError:
        pass

    setup(
        name=NAME,
        version=VERSION,
        url='https://github.com/alex-ber/PythonPackageSyncTool',
        author='Alexander Berkovich',
        description='Small tool to sync package from different machines',
        long_description="\n\n".join([
            open(os.path.join(base_dir, "README.md"), "r").read(),
            open(os.path.join(base_dir, "CHANGELOG.md"), "r").read()
        ]),
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(exclude=('tests*',)),
        #see https://stackoverflow.com/a/26533921
        #see also https://stackoverflow.com/questions/24347450/how-do-you-add-additional-files-to-a-wheel
        # data_files=[('Lib/site-packages/alexber/reqsync', ['data/config.yml', 'data/requirements-src.txt',
        #                                                    'data/driver.py']),
        #             #('lib/python3.7/site-packages/alexber/reqsync', ['requirements-src.txt'])
        #             ],
        # package_data={'alexber.reqsync': ['data/*', 'data/config.yml',
        #                                   'data/requirements-stc.txt', 'data/requirements-dest.txt']},
        package_data={'alexber.reqsync': ['data/*'
                                          ]},
        include_package_data=True,
        install_requires=install_requires,
        entry_points={"console_scripts": [
            "python-package-sync-tool=alexber.data.__main__:main"
        ]},
        # $ setup.py publish support.
        # python3 setup.py upload
        cmdclass={
            'upload': UploadCommand,
        },
        extras_require=extras,
        test_suite="tests",
        tests_require=tests_require,
        setup_requires=['pytest-runner'],
        namespace_packages=('alexber',),
        license='Apache 2.0',
        keywords='tools tool sync package pip',
        classifiers=[
            # See: https://pypi.python.org/pypi?:action=list_classifiers
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'License :: OSI Approved :: BSD License',

            # List of python versions and their support status:
            # https://en.wikipedia.org/wiki/CPython#Version_history
            'Programming Language :: Python',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            "Topic :: Utilities",
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Desktop Environment',
            'Topic :: Education',
            'Operating System :: OS Independent',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Natural Language :: English',
        ],
        python_requires='>=3.7.1',
        zip_safe=False,

    )

finally:
    try:
        os.unlink(lnk_data)
    except OSError:
        pass




