import logging
import pytest

import enum
from enum import Enum

from alexber.reqsync.utils.parsers import ConfigParser, ArgumentParser, safe_eval, is_empty, parse_boolean

logger = logging.getLogger(__name__)
from pathlib import Path
import yaml
from importlib.resources import open_text, path


def test_parse_yaml(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'source': 'requirements-src.txt',
             'destination': 'requirements-dest.txt',
             'remove': ['datashape', 'menuinst']}

    with open_text('tests_data.'+ __package__, 'config.yml') as f:
        d = yaml.safe_load(f)

    dd= d['treeroot']
    assert expdd == dd

def test_parse_ini(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'source': 'requirements-src.txt',
             'destination': 'requirements-dest.txt',
             'remove':'datashape,menuinst',
             }

    parser = ConfigParser()
    with path('tests_data.'+ __package__, 'config.ini') as full_path:
        parser.read(full_path)
    dd = parser.as_dict()
    dd = dd['treeroot']

    assert expdd == dd


@pytest.fixture(params=[
    #'args,exp_d',
    ('--key=value --single',
     dict([('key', 'value'), ('single', None)])),

    ('wrong=pair',
         dict([('wrong=pair', None)])),

    ('--conf --prop1=value1 --prop2=value --prop1=value9',
         dict([('conf', None), ('prop1', 'value9'), ('prop2', 'value')])),

])
def arg_parse_param(request):
    return request.param

def test_args_parse(request, mocker, arg_parse_param):
    logger.info(f'{request._pyfuncitem.name}()')
    args, exp_d = arg_parse_param

    parser = ArgumentParser()

    mock_args = mocker.patch('alexber.reqsync.utils.parsers.sys.argv', new_callable=list)
    mock_args.append(__file__)
    mock_args[1:] = args.split()

    d = parser.as_dict()
    assert exp_d==d


def test_args_parse_explicit_args(request, arg_parse_param):
    logger.info(f'{request._pyfuncitem.name}()')
    args, exp_d = arg_parse_param

    parser = ArgumentParser()

    sys_args = args.split()

    d = parser.as_dict(args=sys_args)
    assert exp_d==d


@enum.unique
class Color(Enum):
    RED = 'r'
    BLUE = 'b'
    GREEN = 'g'


@pytest.mark.parametrize(
    'value, exp_result',
    [
     (True, False),
     (False, True),
     (None, True),

     ("something", False),
     #
     (1, False),
     (0, True),
     (0.0, True),

     ("1", False),
     ("0", False),

     (Color.RED, False),
     ([], True),
     ([None], False),
     (['something'], False),
     ]
)
def test_is_empty(request, value, exp_result):
    logger.info(f'{request._pyfuncitem.name}()')

    result = is_empty(value)
    assert exp_result == result


@pytest.mark.parametrize(
    'value, exp_result',
    [
     (True, True),
     (False, False),
     (None, None),

     ("True", True),
     ("False", False),

     ("TRUE", True),
     ("FALSE", False),

     ("tRuE", True),
     ("fALsE", False),

     ("true", True),
     ("false", False),

     (1, True),
     (0, False),
     (0.0, False),
     ]
)
def test_parse_boolean(request, value, exp_result):
    logger.info(f'{request._pyfuncitem.name}()')

    result = parse_boolean(value)
    assert exp_result == result

@pytest.mark.parametrize(
    'value',
    [
     ("gibrish123"),
     ("T"),
     ("F"),

     ("t"),
     ("f"),

     ("1"),
     ("0"),

     (3.5),
     ([]),
     (5),
     (2.01),

    ]
)


def test_parse_boolean_invalid(request, value):
    logger.info(f'{request._pyfuncitem.name}()')

    with pytest.raises(ValueError, match='nknown'):
        parse_boolean(value)




if __name__ == "__main__":
    pytest.main([__file__])
