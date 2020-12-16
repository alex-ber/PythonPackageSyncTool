import logging
logger = logging.getLogger(__name__)

import os
from pathlib import Path
import pytest

import alexber.reqsync.app as app
from alexber.reqsync import conf
from alexber.reqsync.app import init_app_conf, _PythonPackageSyncToolConfParser

from contextlib import ExitStack

_real_parse_config = init_app_conf.parse_config

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
        if is_empty(line):
            continue
        if line in new_lines:
            continue
        if _extract_pck(line) in removed_lines:
            continue
        pytest.assume(line in sorted_requirements)

#_log_config

@pytest.fixture
def initappFixture(mocker):
    app.logger = logging.getLogger(app.__name__)


@pytest.fixture
def initCwd(mocker):
    cwd = os.getcwd()
    #.../PythonPackageSyncTool/data
    new_cwd = Path(__file__).parent.parent.parent /'data'
    os.chdir(str(new_cwd))
    yield cwd
    os.chdir(cwd)


def test_main(request, mocker, initCwd):
    logger.info(f'{request._pyfuncitem.name}()')

    _parse_config_return_value = None

    def _mock_parse_config(argumentParser=None, args=None):
        ret = _real_parse_config(argumentParser, args)
        nonlocal _parse_config_return_value
        _parse_config_return_value = ret
        return ret

    mocker.patch.object(app, 'fixabscwd', autospec=True, spec_set=True)

    #mocker.spy(init_app_conf, 'parse_config')
    mocker.patch.object(init_app_conf, 'parse_config', side_effect=_mock_parse_config, autospec=True, spec_set=True)
    mocker.patch.object(app, 'run', autospec=True, spec_set=True)


    arg_source = 'source=requirements-src.txt'
    arg_destination = 'destination=requirements-dest.txt'
    arg_remove = 'remove=datashape,menuinst'

    exp_source = f'--treeroot.{arg_source}'
    exp_destination = f'--treeroot.{arg_destination}'
    exp_remove = f'--treeroot.{arg_remove}'

    argsv = f'--{arg_source} ' \
    f'--{arg_destination} ' \
    f'--{arg_remove} ' \
        .split()

    app.main(argsv)

    pytest.assume(init_app_conf.parse_config.call_count == 1)
    _, kwargs =  init_app_conf.parse_config.call_args
    source, destination, remove, _ = kwargs['args']
    pytest.assume( (exp_source, exp_destination, exp_remove) == (source, destination, remove) )

    pytest.assume(app.run.call_count == 1)
    _, run_d = app.run.call_args

    pytest.assume(_parse_config_return_value == run_d)


def test_main_unofficial_api(request, mocker, initCwd):
    logger.info(f'{request._pyfuncitem.name}()')

    _parse_config_return_value = None

    def _mock_parse_config(argumentParser=None, args=None):
        ret = _real_parse_config(argumentParser, args)
        nonlocal _parse_config_return_value
        _parse_config_return_value = ret
        return ret

    mocker.patch.object(app, 'fixabscwd', autospec=True, spec_set=True)

    #mocker.spy(init_app_conf, 'parse_config')
    mocker.patch.object(init_app_conf, 'parse_config', side_effect=_mock_parse_config, autospec=True, spec_set=True)
    mocker.patch.object(app, 'run', autospec=True, spec_set=True)


    arg_source = 'treeroot.source=requirements-src.txt'
    arg_destination = 'treeroot.destination=requirements-dest.txt'
    arg_remove = 'treeroot.remove=datashape,menuinst'

    exp_source = f'--{arg_source}'
    exp_destination = f'--{arg_destination}'
    exp_remove = f'--{arg_remove}'

    argsv = f'--{arg_source} ' \
    f'--{arg_destination} ' \
    f'--{arg_remove} ' \
    '--general.config.file=config.yml' \
        .split()

    app.main(argsv)

    pytest.assume(init_app_conf.parse_config.call_count == 1)
    _, kwargs =  init_app_conf.parse_config.call_args
    source, destination, remove, _, _ = kwargs['args']
    pytest.assume( (exp_source, exp_destination, exp_remove) == (source, destination, remove) )

    pytest.assume(app.run.call_count == 1)
    _, run_d = app.run.call_args

    pytest.assume(_parse_config_return_value == run_d)

def test_run(request, mocker, initappFixture):
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

    app.run(**{conf.APP_KEY:d})

    validate_result(input_path=exp_input, output_path=exp_output, removed_lines=exp_removes)

def test_run_unsorted_src_req(request, mocker, initappFixture):
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
        app.run(**{conf.APP_KEY:d})



@pytest.mark.parametrize(
     'source',

    [
        ('requirements-src.txt'),                   #no_change (basic)
        ('requirements-src-middle_empty_lines.txt'),
        ('requirements-src-first_empty_line.txt'),
        ('requirements-src-last_empty_lines.txt'),
        (None),                                     #_READ_BUFFER_SIZE / _WRITE_BUFFER_SIZE

    ]
)
def test_run_no_change(request, mocker, source, initappFixture):
    logger.info(f'{request._pyfuncitem.name}()')

    if source is None: #check correct usage of file input buffer and file output buffer.
        mocker.patch.object(app, '_READ_BUFFER_SIZE', new=40)
        mocker.patch.object(app, '_WRITE_BUFFER_SIZE', new=30)
        source = 'requirements-src.txt'

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, source))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))


    d = {'config_file': str(exp_config_yml),
        'source': str(exp_input),
        'destination': str(exp_output),
        'remove':None,
        'add': None
             }

    app.run(**{conf.APP_KEY:d})

    validate_result(input_path=exp_input, output_path=exp_output)

@pytest.fixture
def init_default_parser_kwargs(request, mocker):
    request_param = {} if (
        not hasattr(request, 'param')) else request.param
    yield request_param


@pytest.fixture
def initparserFixture(mocker, init_default_parser_kwargs):
    default_parser_cls = init_app_conf.default_parser_cls
    default_parser_kwargs = init_app_conf.default_parser_kwargs

    init_app_conf.initConfig(default_parser_cls=_PythonPackageSyncToolConfParser, default_parser_kwargs=init_default_parser_kwargs)
    yield _PythonPackageSyncToolConfParser
    init_app_conf.initConfig(default_parser_cls=default_parser_cls, default_parser_kwargs=default_parser_kwargs)


@pytest.mark.parametrize(
     'exp_value, value, is_windows_path',

    [
        ('lxml==4.3.3', 'lxml:4.3.3', None),  #: is maksed as ==
        ('lxml==4.3.3', 'lxml==4.3.3', None), #== remains untouched
        (['lxml:4.3.3'], ['lxml:4.3.3'], None),  #will not happen in practice, so it's ok to be incorrect
                                           #it just shouldn't blow up
        (['lxml==4.3.3'], ['lxml==4.3.3'], None), #list
        ('C:\\', 'C:\\', True),    #Windows path, remain utntouched
        ('/etc/', '/etc/', False),   #Posix   path, remain utntouched
        ('config.yml', 'config.yml', None)

    ]
)

def test_mask_value(request, mocker, exp_value, value, is_windows_path,
                    init_default_parser_kwargs, initparserFixture):
    logger.info(f'{request._pyfuncitem.name}()')

    ret = init_app_conf.mask_value(value)

    if is_windows_path is None or not is_windows_path:
        pytest.assume(exp_value == ret)
    else:
        assert is_windows_path
        is_run_on_windows = os.name == 'nt'
        if is_run_on_windows:
            #exact comparasion
            pytest.assume(exp_value == ret)
        elif not is_run_on_windows:
            def is_path_exists(p):
                try:
                    pa=Path(p)
                    return pa.exists()
                except OSError:
                    return False

            #loose comparasion, it is enough that both paths doesn't exists
            is_exists = is_path_exists(ret)
            pytest.assume(not is_exists)
            is_exists = is_path_exists(value)
            pytest.assume(not is_exists)


@pytest.mark.parametrize('init_default_parser_kwargs', [{'implicit_convert':False},
                                                    ], indirect=True)

def test_mask_value_no_implicit_convert(request, mocker, init_default_parser_kwargs, initparserFixture):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_value = 'lxml:4.3.3'
    ret = init_app_conf.mask_value(exp_value)
    pytest.assume(exp_value == ret)


if __name__ == "__main__":
    pytest.main([__file__])
