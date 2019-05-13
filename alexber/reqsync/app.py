import logging.config


from pathlib import Path
import alexber.reqsync.app_conf as conf

from collections import deque

_READ_BUFFER_SIZE = 2 ** 16
_WRITE_BUFFER_SIZE = 2 ** 16

def _getSourceGen(filename):

    buffersize = _READ_BUFFER_SIZE
    with open(filename, 'rt') as f:
        while True:
            lines_buffer = f.readlines(buffersize)
            if not lines_buffer:
                break
            for line in lines_buffer:
                pck = line.rstrip()  # remove '\r'
                if pck:
                    yield pck


def _process_line(prev_line, cur_line, **kwargs):
    if (prev_line is not None) and (prev_line == cur_line):
        return None #duplicate line, ignore

    if (prev_line is not None) and (prev_line > cur_line):
        raise ValueError("Source file expected to be sorted. Use sort utilities, for example.")

    add_pckgs = kwargs.get(conf.ADD_KEY, None)
    rm_pckgs = kwargs.get(conf.RM_KEY, None)
    cur_pck, _ = cur_line.split('==')
    prev_pck, _ = '' if prev_line is None else prev_line.split('==')

    ret = []

    #remove packages first
    while rm_pckgs:
        rm_pck = rm_pckgs[0]
        if cur_pck < rm_pck:
            ret.append(cur_line)
            #we shoudn't remove rm_pck
            break
        if cur_pck == rm_pck:
            rm_pckgs.popleft()
        else:
            ret.append(cur_line)
            rm_pckgs.popleft()

    # add packages
    while add_pckgs:
        add_line = add_pckgs[0]
        add_pck, _ = add_line.split('==')
        if prev_pck<add_pck<cur_pck:
            ret.append(add_line)
            add_pckgs.popleft()


    return ret


def run(**kwargs):
    """
    This method recieved all conf params in kwargs.
    All unexpected values will be ignored.
    It is expected that value type is correct.
    No conversion on the value of the dict kwargs will be applied.
    This method will built playerA, playerB, engine,
    and run engine with these players.

    Please, consult alexber.rpsgame.app_conf in order to construct kwargs.
    Command-line argument and ini-file are suppored out of the box.
    JSON/YML, etc. can be easiliy handled also.
    """

    #filter out unrelated params
    kwargs = conf.parse_dict(kwargs)

    src_f = kwargs.get(conf.SOURCE_KEY, None)
    if src_f is None:
        raise ValueError(f'{conf.SOURCE_KEY} key should be defined')

    dest_f = kwargs.get(conf.DEST_KEY, None)
    if dest_f is None:
        raise ValueError(f'{conf.DEST_KEY} key should be defined')

    add_pck = kwargs.pop(conf.ADD_KEY, None)
    add_pck = None if add_pck is None else deque(sorted(add_pck))   #Limitation: in-memory sorted

    rm_pckgs = kwargs.pop(conf.RM_KEY, None)
    rm_pckgs = None if rm_pckgs is None else deque(sorted(rm_pckgs))  # Limitation: in-memory sorted

    kwargs[conf.ADD_KEY] = add_pckgs
    kwargs[conf.RM_KEY] = rm_pckgs


    full_src_path = Path(src_f).resolve()  # relative to cwd
    full_dest_path = Path(dest_f).resolve()  # relative to cwd
    sourceGen = _getSourceGen(full_src_path)

    buffersize = _WRITE_BUFFER_SIZE
    lines_buffer = deque(maxlen=buffersize)
    prev_line = None

    with open(full_dest_path, 'wt') as f:
        for cur_line in sourceGen:
            lines = _process_line(prev_line, cur_line,
                                  **kwargs)
            if lines is not None:
                lines_buffer.extend(lines)

            length = len(lines_buffer)
            if length ==  buffersize:
                f.writelines(lines_buffer)
                lines_buffer.clear()
            prev_line = cur_line
        f.writelines(lines_buffer)
        lines_buffer.clear()






def main(args=None):
    """
    main method
    :param args: if not None, suppresses sys.args
    """
    dd = conf.parse_config(args)
    run(**dd)


#see https://terryoy.github.io/2016/05/short-ref-python-logging.html
_config = {
        "log_config": {
            "version": 1,
            "formatters": {
                "brief": {
                    "format": "%(message)s",
                },
                "detail": {
                    "format": "%(asctime)-15s %(levelname)s [%(name)s.%(funcName)s] %(message)s",
                    "datefmt": '%Y-%m-%d %H:%M:%S',
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "brief",
                },
                # "file": {
                #     "class": "logging.handlers.RotatingFileHandler",
                #     "filename": "dev.log",
                #     "level": "DEBUG",
                #     "formatter": "detail",
                # },
            },
            "root": {
                # "handlers": ["console", "file"],
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "loggers": {
                "requests": {
                    # "handlers": ["file"],
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": False,
                }
            },
        },
    }

if __name__ == '__main__':
    logging.config.dictConfig(_config["log_config"])
    del _config
    logger = logging.getLogger(__name__)
    main()


