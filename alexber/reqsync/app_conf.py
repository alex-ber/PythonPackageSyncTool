import logging

logger = logging.getLogger(__name__)

from alexber.reqsync.utils.parsers import ConfigParser, ArgumentParser
from pathlib import Path
from collections import OrderedDict
import yaml

SOURCE_KEY = 'source'
DEST_KEY  = 'destination'
RM_KEY = 'remove'
ADD_KEY = 'add'

_WHITELIST_FLAT_PREFIX = {SOURCE_KEY, DEST_KEY, RM_KEY, ADD_KEY}


def parse_dict(d):
    dd = OrderedDict()

    for key in _WHITELIST_FLAT_PREFIX:
        val = d.get(key, None)
        if val is not None and ','  in val:
            dd[key]= val.split(',')
        else:
            dd[key] = val
    return dd


def parse_sys_args(argumentParser=None, args=None):
    """
    This function can be in external use.
    This function parses command line arguments.

    :param argumentParser:
    :param args: if not None, suppresses sys.args
    :return:
    """
    if argumentParser is None:
        argumentParser = ArgumentParser()
    argumentParser.add_argument("--config_file", nargs='?', dest='config_file', default='config.yml',
                                const='config.yml')
    params, unknown_arg = argumentParser.parse_known_args(args=args)

    dd = argumentParser.as_dict(args=unknown_arg)
    dd = parse_dict(dd)
    return params, dd





def parse_yml(config_file='config.yml'):
    """
    This function can be in external use.
    This function parses ini file.

    :param config_file: path to the YAML file. Default value is config.yml. Can be str or os.PathLike.
    :return: dict ready to use
    """

    full_path = Path(config_file).resolve() #relative to cwd

    with open(full_path) as f:
        d = yaml.safe_load(f)
    d = d['treeroot']
    dd = parse_dict(d)
    return dd

def parse_config(args=None):
    """
    This function can be in external use, but it is not intended for.
    This function parses command line arguments.
    Than it parse ini file.
    Command line arguemnts overrides ini file arguments.

    In more detail, command line arguments of the form --key=value are parsed first.
    If exists --config_file it's value is used to search for ini file.
    if --config_file is absent, 'config.yml' is used for ini file.
    If ini file is not found, only command line arguments are used.
    If ini file is found, both arguments are used, while
    command line arguments overrides ini arguments.

    :param args: if not None, suppresses sys.args
    :return: dict ready to use
    """
    params, cli_dd = parse_sys_args(args=args)
    filtered_cli_dd = {k: v for k, v in cli_dd.items() if v is not None}   #filter out None

    config_dd = parse_yml(params.config_file)
    dd = OrderedDict()
    dd.update(config_dd)
    dd.update(filtered_cli_dd)
    return dd



