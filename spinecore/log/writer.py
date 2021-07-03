"""
Created 18th June 2019
"""
import logging

from spinecore.log.constants import LoggingConstants as lc
from spinecore.log.formatting import create_log_line


FILE_DATE_FORMAT = '%Y%m%d%H'


def _get_logging_function(log_type):
    """ Get the logging function to use """
    if log_type == lc.LFR_AUDIT:
        return logging.getLogger(lc.SPINE_LOGGER).audit
    if log_type == lc.LFR_NMS:
        return logging.getLogger(lc.SPINE_LOGGER).monitor
    if log_type == lc.LFR_OPERATIONS:
        return logging.getLogger(lc.SPINE_LOGGER).info
    if log_type == lc.LFR_CRASHDUMP:
        return logging.getLogger(lc.SPINE_LOGGER).crash

    return None


def write_to_file(
        log_preamble,
        log_text,
        substitution_dict,
        log_type,
        error_list=None
):
    """
    Append the log line to the appropriate file
    Add traceback information if required
    """
    log_line = create_log_line(log_preamble, log_text, substitution_dict)
    if error_list:
        log_line = '{} - {}'.format(log_line, error_list[0:])

    logging_func = _get_logging_function(log_type)
    if logging_func:
        # pylint: disable=deprecated-method
        logging_func(log_line)