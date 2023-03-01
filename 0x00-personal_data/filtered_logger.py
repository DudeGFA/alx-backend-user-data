#!/usr/bin/env python3
"""
    Contains function filtered_datum
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
        returns the log message obfuscated
    """
    for field in fields:
        pattern = re.escape(field + "=") + r".*?" + re.escape(separator)
        replacement = field + "=" + redaction + separator
        message = re.sub(pattern, replacement, message)
    return message
