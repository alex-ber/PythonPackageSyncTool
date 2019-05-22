import logging
logger = logging.getLogger(__name__)
from pathlib import Path

import pytest
from alexber.reqsync import app
from contextlib import ExitStack
from importlib.resources import open_text, path

@pytest.mark.it
def test_it_full_single_package(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    file_manager = ExitStack()

    exp_config_yml = file_manager.enter_context(
        path('tests_data.' + __package__+'.it',  "config.yml"))
    exp_input = file_manager.enter_context(
        path('tests_data.' + __package__+'.it', 'requirements-src.txt'))
    exp_output= file_manager.enter_context(
        path('tests_data.' + __package__+'.it', 'requirements-dest.txt'))
    exp_package = 'lxml'
    exp_version = '4.3.3'
    exp_line = f'{exp_package}=={exp_version}'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version} ' \
        .split()
    app.main(argsv)

    with open(exp_output, 'rt') as f:
        out_requirements = [line.rstrip() for line in f.readlines()]

    sorted_requirements = sorted(out_requirements, key=lambda line: line.split('==')[0].casefold())
    pytest.assume(sorted_requirements==out_requirements)
    pytest.assume(exp_line in sorted_requirements)

@pytest.mark.it
def test_it_full_single_package_exist(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    exp_config_yml = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', "config.yml"))
    exp_input = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-dest.txt'))
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

    exp_config_yml = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', "config.yml"))
    exp_input = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-dest.txt'))
    exp_package = 'lxml'
    exp_version = '4.3.3'
    exp_line = f'{exp_package}=={exp_version}'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version}, ' \
        .split()
    app.main(argsv)

    with open(exp_output, 'rt') as f:
        out_requirements = [line.rstrip() for line in f.readlines()]

    sorted_requirements = sorted(out_requirements, key=lambda line: line.split('==')[0].casefold())
    pytest.assume(sorted_requirements==out_requirements)
    pytest.assume(exp_line in sorted_requirements)


@pytest.mark.it
def test_it_full_single_package_exist_as_list(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    file_manager = ExitStack()

    exp_config_yml = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', "config.yml"))
    exp_input = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-dest.txt'))
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

    exp_config_yml = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', "config.yml"))
    exp_input = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-src.txt'))
    exp_output = file_manager.enter_context(
        path('tests_data.' + __package__ + '.it', 'requirements-dest.txt'))
    exp_package = 'zope.interface'
    exp_version = '4.6.0'
    exp_line = f'{exp_package}=={exp_version}'

    argsv = f'--config_file={exp_config_yml} ' \
            f'--source={exp_input} ' \
            f'--destination={exp_output} ' \
            f'--add={exp_package}:{exp_version}, ' \
        .split()

    app.main(argsv)

    with open(exp_output, 'rt') as f:
        out_requirements = [line.rstrip() for line in f.readlines()]

    sorted_requirements = sorted(out_requirements, key=lambda line: line.split('==')[0].casefold())
    pytest.assume(sorted_requirements == out_requirements)
    pytest.assume(exp_line in sorted_requirements)


if __name__ == "__main__":
    pytest.main([__file__])
