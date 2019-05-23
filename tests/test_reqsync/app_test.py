import logging
logger = logging.getLogger(__name__)

import pytest

import alexber.reqsync.app as app
from alexber.reqsync.app import conf as app_conf
from contextlib import ExitStack

_real_parse_config = app_conf.parse_config
from importlib.resources import path
from alexber.utils.parsers import is_empty

def _extract_pck(element):
    if element is None or is_empty(element):
        return ''
    elif '==' not in element:
        pck = element
    else:
        pck, _ = element.split('==')
    return pck


def validate_result(input_path, output_path, **kwargs):
    assert not is_empty(input_path)
    assert not is_empty(output_path)

    with open(output_path, 'rt') as f:
        out_requirements = [line.rstrip() for line in f.readlines()]

    sorted_requirements = sorted(out_requirements, key=lambda line: line.split('==')[0].casefold())
    pytest.assume(sorted_requirements==out_requirements)

    new_lines = kwargs.get('new_lines', [])
    for line in new_lines:
        pytest.assume(line in sorted_requirements)

    removed_lines = kwargs.get('removed_lines', [])
    for line in removed_lines:
        pytest.assume(line not in sorted_requirements)


    with open(input_path, 'rt') as f:
        in_requirements = [line.rstrip() for line in f.readlines()]
    for line in in_requirements:
        if line in new_lines:
            continue
        if _extract_pck(line) in removed_lines:
            continue
        pytest.assume(line in sorted_requirements)


def test_main(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    _parse_config_return_value = None

    def _mock_parse_config(args=None):
        ret = _real_parse_config(args)
        nonlocal _parse_config_return_value
        _parse_config_return_value = ret
        return ret

    #mocker.spy(app_conf, 'parse_config')
    mocker.patch.object(app_conf, 'parse_config', side_effect=_mock_parse_config, autospec=True, spec_set=True)
    mocker.patch.object(app, 'run', autospec=True, spec_set=True)

    exp_source = '--source=requirements-src.txt'
    exp_destination = '-destination=requirements-dest.txt'
    exp_remove = '-remove=datashape,menuinst'

    argsv = f'{exp_source} ' \
    f'{exp_destination} ' \
    f'{exp_remove} ' \
        .split()

    app.main(argsv)

    pytest.assume(app_conf.parse_config.call_count == 1)
    ((source, destination, remove),), _ =  app_conf.parse_config.call_args
    pytest.assume( (exp_source, exp_destination, exp_remove) == (source, destination, remove) )

    pytest.assume(app.run.call_count == 1)
    _, run_d = app.run.call_args

    pytest.assume(_parse_config_return_value == run_d)


def test_run(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_removes = ['datashape','menuinst']


    d = {'config_file': str(exp_config_yml),
        'source': str(exp_input),
        'destination': str(exp_output),
        'remove':exp_removes,
        'add': None
             }

    app.run(**d)

    validate_result(input_path=exp_input, output_path=exp_output, removed_lines=exp_removes)

def test_run_unsorted_src_req(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'unsorted_src_req'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_removes = ['datashape','menuinst']


    d = {'config_file': str(exp_config_yml),
         'source': str(exp_input),
        'destination': str(exp_output),
        'remove':exp_removes,
        'add': None
             }

    with pytest.raises(ValueError, match='xpected to be sorted'):
        app.run(**d)


def test_run_no_change(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))


    d = {'config_file': str(exp_config_yml),
        'source': str(exp_input),
        'destination': str(exp_output),
        'remove':None,
        'add': None
             }

    app.run(**d)

    validate_result(input_path=exp_input, output_path=exp_output)




if __name__ == "__main__":
    pytest.main([__file__])
