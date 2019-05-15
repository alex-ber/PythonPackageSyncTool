import setuptools
from setuptools import setup
import os

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

try:
    os.symlink(os.path.join('..', '..', 'data'), lnk_data)
    setup(
        name='python-package-sync-tool',
        version='0.1.3',
        url='https://github.com/alex-ber/PythonPackageSyncTool',
        author='Alexander Berkovich',
        description='Small tool to sync package from different machines',
        long_description="\n\n".join([
            open(os.path.join(base_dir, "README.rst"), "r").read(),
            open(os.path.join(base_dir, "CHANGELOG.rst"), "r").read()
        ]),
        packages=setuptools.find_packages(exclude=('tests*',)),
        #see https://stackoverflow.com/a/26533921
        # data_files=[('Lib/site-packages/alexber/reqsync', ['data/config.yml', 'data/requirements-src.txt',
        #                                                    'data/driver.py']),
        #             #('lib/python3.7/site-packages/alexber/reqsync', ['requirements-src.txt'])
        #             ],
        package_data={'alexber.reqsync': ['data/*']},
        include_package_data=True,
        install_requires=install_requires,
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
            'Programming Language :: Python :: 3.7.1',
            'Programming Language :: Python :: 3.7.2',
            'Programming Language :: Python :: Implementation :: CPython'
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
    os.unlink(lnk_data)
    pass



