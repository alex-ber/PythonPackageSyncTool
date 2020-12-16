import logging
logger = logging.getLogger(__name__)

import pytest
import alexber.reqsync.app as app
from alexber.reqsync.app import conf


@pytest.mark.parametrize(
        'arg,exp_key,exp_value',

        [
            ('--source=requirements-src.txt','source', 'requirements-src.txt'),
            ('--destination=requirements-dest.txt','destination', 'requirements-dest.txt'),
            ('--remove=datashape,menuinst','remove', 'datashape,menuinst'),
            ('--add=numpy','add', 'numpy'),
            ('--treeroot.remove=datashape,menuinst','treeroot.remove', 'datashape,menuinst'),

             (None, None, None),
            ('add=numpy',None, 'add=numpy'),    #see below (1)
            ('--add','--add', ''),              #see below (2)

        ]
    )

def test_adapt_arg_split(request, mocker, arg, exp_key, exp_value):
    logger.info(f'{request._pyfuncitem.name}()')

    ret_key, ret_value = app._adapt_arg_split(arg)
    pytest.assume(exp_key == ret_key)
    pytest.assume(exp_value == ret_value)


@pytest.mark.parametrize(
        'arg,exp_value',

        [
            ('--source=requirements-src.txt','--treeroot.source=requirements-src.txt'),
            ('--destination=requirements-dest.txt','--treeroot.destination=requirements-dest.txt'),
            ('--remove=datashape,menuinst', '--treeroot.remove=datashape,menuinst'),
            ('--add=numpy', '--treeroot.add=numpy'),
            ('--treeroot.remove=datashape,menuinst','--treeroot.remove=datashape,menuinst'),
            ('--port=19572','--port=19572'),    #unknown paramater

            (None, None),
            ('add=numpy','add=numpy'),    #(1)
            ('--add','--add'),            #(2)

        ]
    )
def test_adapt_arg_split(request, mocker, arg, exp_value):
    logger.info(f'{request._pyfuncitem.name}()')

    ret = app._adapt_arg(arg)
    pytest.assume(exp_value == ret)




@pytest.mark.parametrize(
        'args,exp_value',

        [
            (['--source=requirements-src.txt',
              '--destination=requirements-dest.txt',
              '--remove=datashape,menuinst'],
            None),

            (['--treeroot.source=requirements-src.txt',
              '--treeroot.destination=requirements-dest.txt',
              '--treeroot.remove=datashape,menuinst'],
            '--general.listEnsure=treeroot.remove'),

            (['--treeroot.source=requirements-src.txt',
              '--treeroot.destination=requirements-dest.txt',
              '--treeroot.remove=datashape,menuinst'],
            '--general.listEnsure=treeroot.remove'),

            (['--treeroot.source=requirements-src.txt',
              '--treeroot.destination=requirements-dest.txt',
              '--treeroot.add=numpy',
              '--treeroot.remove=datashape,menuinst'],
            '--general.listEnsure=treeroot.add,treeroot.remove'),

            ([
              '--treeroot.remove=datashape,menuinst'],
            '--general.listEnsure=treeroot.remove'),

            ([
              '--treeroot.add=numpy',   #treeroot.add will  not be treated as list
              '--treeroot.remove=datashape,menuinst',
              '--port=19572',        ##unknown paramater
              '--general.listEnsure=treeroot.remove'   #explicit param
             ],
            '--general.listEnsure=treeroot.remove'),


        ]
    )
def test_adapt_list_ensure(request, mocker, args, exp_value):
    logger.info(f'{request._pyfuncitem.name}()')

    ret = app._adapt_list_ensure(args)
    assert ret is not None
    list_ensure_key = f'--{conf.GENERAL_KEY}.{conf.LIST_ENSURE_KEY}'
    is_found = False

    for keyvalue in ret:
        if keyvalue.startswith(list_ensure_key):
            is_found = True
            if exp_value is not None:
                pytest.assume(exp_value == keyvalue)

    if exp_value is not None:
        pytest.assume(is_found)
    else:
        pytest.assume(not is_found)

if __name__ == "__main__":
    pytest.main([__file__])
