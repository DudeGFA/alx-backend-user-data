#!/usr/bin/env python3
"""
    Contains:
        Function filter_datum
        Class RedactingFormatter
        Function get_logger
        Function get_db
        List PII_FIELDS
"""
import re
import logging
from typing import List
import mysql.connector
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List,
        redaction: str,
        message: str,
        separator: str) -> str:
    """
        returns the log message obfuscated
    """
    for field in fields:
        pattern = re.escape(field + "=") + r".*?" + re.escape(separator)
        replacement = field + "=" + redaction + separator
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
            Intialise new instance
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            returns a formatted log from a log record
        """
        log_message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            log_message,
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
        returns a logging.Logger object.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        returns a connector to a mysql database
    """
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    db_host = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    connector = mysql.connector.connect(user=db_username,
                                        password=db_password,
                                        host=db_host,
                                        database=db_name)
    return connector


def main():
    """
        obtain a database connection using get_db and
        retrieve all rows in the users table and display
        each row
    """
    new_connector = get_db
    new_logger = get_logger
    cursor = new_connector.cursor()
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        new_logger.info(message.strip())
    cursor.close()
    new_connector.close()


if __name__ == "__main__":
    main()
