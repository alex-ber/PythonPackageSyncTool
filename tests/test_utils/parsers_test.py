import logging
import pytest

from alexber.reqsync.utils.parsers import ConfigParser, ArgumentParser, safe_eval
from alexber.reqsync import app_conf

logger = logging.getLogger(__name__)
from pathlib import Path
import yaml


def test_parse_yaml(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'source': 'requirements-src.txt',
             'destination': 'requirements-dest.txt',
             'remove': ['datashape', 'menuinst']}

    dir = Path(__file__).parent

    with open(dir / 'config.yml') as f:
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
    dir = Path(__file__).parent

    full_path = Path(dir / 'config.ini')

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



if __name__ == "__main__":
    pytest.main([__file__])