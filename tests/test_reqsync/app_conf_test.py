import logging
logger = logging.getLogger(__name__)
from pathlib import Path

import pytest
from alexber.reqsync import app_conf
from alexber.reqsync.utils.parsers import ConfigParser

import yaml
from importlib.resources import open_text, path
from contextlib import ExitStack

class TestFreeStyle(object):

    def test_parse_yaml(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'source': 'requirements-src.txt',
                 'destination': 'requirements-dest.txt',
                 'remove': ['datashape', 'menuinst', 'graphviz', 'entrypoints', 'numpy'],
                 'add':None,
                 'mutual_exclusion': True}
        pck = '.'.join(['tests_data', __package__])

        with open_text(pck, 'config.yml') as f:
            d = yaml.safe_load(f)
        d = d['treeroot']
        dd = app_conf.parse_dict(d)
        assert expdd == dd

    def test_parse_dict(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        d =  {'source': 'requirements-src.txt',
                 'destination': 'requirements-dest.txt',
                 'remove': ['datashape', 'menuinst'],
                 }

        expdd = {'source': 'requirements-src.txt',
                 'destination': 'requirements-dest.txt',
                 'remove': ['datashape', 'menuinst'],
                 'add': None,
                 'mutual_exclusion': None}

        dd = app_conf.parse_dict(d)
        assert expdd == dd

    def test_parse_sys_args(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'source': 'requirements-src.txt',
                 'destination': 'requirements-dest.txt',
                 'remove': ['datashape', 'menuinst'],
                 'add': None,
                 'mutual_exclusion': None}


        argsv = '--source=requirements-src.txt ' \
                '--destination=requirements-dest.txt ' \
                '--remove=datashape,menuinst ' \
            .split()

        _, dd = app_conf.parse_sys_args(args=argsv)
        dd = app_conf.parse_dict(dd)

        assert expdd == dd

    def test_parse_ini(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'source': 'requirements-src.txt',
                 'destination': 'requirements-dest.txt',
                 'remove': ['datashape', 'menuinst'],
                 'add':None,
                 'mutual_exclusion': None}

        parser = ConfigParser()

        pck = '.'.join(['tests_data', __package__])

        with path(pck, 'config.ini') as full_path:
            parser.read(full_path)
        dd = parser.as_dict()
        dd= dd['treeroot']
        dd = app_conf.parse_dict(dd)

        assert expdd == dd



    def test_config_with_override(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'source': 'requirements-src.txt',
                 'destination': 'requirements-newdest.txt',
                 'remove': ['datashape', 'menuinst', 'graphviz', 'entrypoints', 'numpy'],
                 'add': None,
                 'mutual_exclusion': True}
        pck = '.'.join(['tests_data', __package__])

        with path(pck, 'config.yml') as config_file:
            argsv = f'--config_file={config_file} ' \
                '--destination=requirements-newdest.txt ' \
            .split()
        dd = app_conf.parse_config(args=argsv)
        assert expdd == dd




def test_parse_config(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, 'parse_sys_args')
    mocker.spy(app_conf, 'parse_yml')
    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__])

    exp_config_yml= file_manager.enter_context(
        path(pck, 'config.yml'))

    argsv = f'--config_file={exp_config_yml} ' \
        '--add=numpy:1.16.2 ' \
        .split()
    app_conf.parse_config(args=argsv)

    pytest.assume(app_conf.parse_sys_args.call_count == 1)
    pytest.assume(app_conf.parse_yml.call_count == 1)

    params, _ = app_conf.parse_sys_args()
    # params return from parse_sys_args() contains exp_config_yml

    pck = '.'.join(['tests_data', __package__])
    actual_config_file = file_manager.enter_context(
        path(pck, params.config_file))

    pytest.assume(exp_config_yml == actual_config_file)

    #exp_config_yml was passed to parse_yml()
    (config_file,), _ =  app_conf.parse_yml.call_args
    pytest.assume(exp_config_yml==Path(config_file))


if __name__ == "__main__":
    pytest.main([__file__])
