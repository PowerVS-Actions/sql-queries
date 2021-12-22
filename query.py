#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2021 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Rafael Sene <rpsene@br.ibm.com>
"""

import os
import sys
import psycopg2
from datetime import datetime
from configparser import ConfigParser


def get_db_config(filename='postgres.ini', section='postgresql'):
    '''Reads and parses the postgres.ini file.'''
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


def connect_db():
    '''Returns a new database connection'''
    conn = None
    try:
        # read database configuration
        params = get_db_config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def execute_sql_command(sql):
    '''Runs any SQL command'''
    conn = connect_db()
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the powervs_id back
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def calculate_daily_avg_resources():
    sql="select * from avg_resources_day()"
    execute_sql_command(sql)


def calculate_montly_avg_resources():
    sql="select * from avg_resources_month()"
    execute_sql_command(sql)

if __name__ == '__main__':
    calculate_daily_avg_resources()
    calculate_montly_avg_resources()