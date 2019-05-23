import logging
logger = logging.getLogger(__name__)

import pytest
from alexber.reqsync import app
from contextlib import ExitStack
from importlib.resources import path
from pathlib import Path
import yaml

from .app_test import validate_result


def _calc_removed_lines_lines(config_file):
    full_path = Path(config_file).resolve()

    with open(full_path) as f:
        d = yaml.safe_load(f)
    d = d['treeroot']
    ret = d['remove']
    return ret


@pytest.mark.it
def test_it_full_single_package(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck,  "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output= file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_package = 'lxml'
    exp_version = '4.3.3'
    exp_line = f'{exp_package}=={exp_version}'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version} ' \
        .split()
    app.main(argsv)

    validate_result(
        input_path=exp_input,
        output_path=exp_output,
        new_lines=[exp_line],
        removed_lines=_calc_removed_lines_lines(exp_config_yml))



@pytest.mark.it
def test_it_full_single_package_exist(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_package = 'numpy'
    exp_version = '1.16.2'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version} ' \
        .split()

    with pytest.raises(ValueError, match='Mutual_Exclusion'):
        app.main(argsv)





@pytest.mark.it
def test_it_full_single_package_as_list(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_package = 'lxml'
    exp_version = '4.3.3'
    exp_line = f'{exp_package}=={exp_version}'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version}, ' \
        .split()
    app.main(argsv)

    validate_result(
        input_path=exp_input,
        output_path=exp_output,
        new_lines=[exp_line],
        removed_lines=_calc_removed_lines_lines(exp_config_yml))


@pytest.mark.it
def test_it_full_single_package_exist_as_list(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()
    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_package = 'numpy'
    exp_version = '1.16.2'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version}, ' \
        .split()

    with pytest.raises(ValueError, match='Mutual_Exclusion'):
        app.main(argsv)


@pytest.mark.it
def test_it_full_single_package_last(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_package = 'zope.interface'
    exp_version = '4.6.0'
    exp_line = f'{exp_package}=={exp_version}'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version}, ' \
        .split()

    app.main(argsv)

    validate_result(
        input_path=exp_input,
        output_path=exp_output,
        new_lines=[exp_line],
        removed_lines=_calc_removed_lines_lines(exp_config_yml))


@pytest.mark.it
def test_it_full_single_package_first(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck, "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))
    exp_package = 'aaa'
    exp_version = '1.0.0'
    exp_line = f'{exp_package}=={exp_version}'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version}, ' \
        .split()

    app.main(argsv)

    validate_result(
        input_path=exp_input,
        output_path=exp_output,
        new_lines=[exp_line],
        removed_lines=_calc_removed_lines_lines(exp_config_yml))


@pytest.mark.it
def test_it_remove_single_package(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck,  "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output= file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))

    remove_package = 'numpy'


    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--remove={remove_package} ' \
        .split()
    app.main(argsv)

    validate_result(
        input_path=exp_input,
        output_path=exp_output,
        removed_lines=[remove_package])


@pytest.mark.it
def test_it_remove_single_package_first(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck,  "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output= file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))

    remove_package = 'appdirs'


    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--remove={remove_package} ' \
        .split()
    app.main(argsv)

    validate_result(
        input_path=exp_input,
        output_path=exp_output,
        removed_lines=[remove_package])

@pytest.mark.it
def test_it_remove_single_package_last(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    file_manager = ExitStack()

    pck = '.'.join(['tests_data', __package__, 'it'])

    exp_config_yml = file_manager.enter_context(
        path(pck,  "config.yml"))
    exp_input = file_manager.enter_context(
        path(pck, 'requirements-src.txt'))
    exp_output= file_manager.enter_context(
        path(pck, 'requirements-dest.txt'))

    remove_package = 'wstools'


    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--remove={remove_package} ' \
        .split()
    app.main(argsv)

    validate_result(
        input_path=exp_input,
        output_path=exp_output,
        removed_lines=[remove_package])


if __name__ == "__main__":
    pytest.main([__file__])
