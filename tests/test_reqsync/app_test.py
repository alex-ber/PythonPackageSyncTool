import logging
logger = logging.getLogger(__name__)

import pytest

import alexber.reqsync.app as app
from alexber.reqsync.app import conf as app_conf

_real_parse_config = app_conf.parse_config





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
    exp_destination = '--destination=requirements-dest.txt'
    exp_remove = '--remove=datashape,menuinst'

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

    d = {'source': 'requirements-src.txt',
             'destination': 'requirements-dest.txt',
             'remove':['datashape','menuinst'],
             'add': None
             }

    app.run(**d)

#
# @pytest.mark.it
# def test_play_it(request, mocker):
#     logger.info(f'{request._pyfuncitem.name}()')
#
#     mocker.patch('alexber.rpsgame.engine', new=engine_1_0)
#     mock_logging = mocker.patch(f'alexber.rpsgame.engine_1_0.logging', autospec=True, spec_set=True)
#     reset_event_listeners()
#     mocker.patch('alexber.rpsgame.engine_1_0.uuid1mc', new=lambda: '1')
#
#     args = '--playera.cls=alexber.rpsgame.players.ConstantPlayer --playerb.cls=alexber.rpsgame.players.ConstantPlayer'\
#         .split()
#     rpsgame_app_main(args)
#
#     mock_result = mock_logging.info
#
#     result = _parse_result(mock_result, app_conf.DEFAULT_NAME_PLAYER_A, app_conf.DEFAULT_NAME_PLAYER_B)
#     pytest.assume(ResultEnum.DRAW == result)


if __name__ == "__main__":
    pytest.main([__file__])
