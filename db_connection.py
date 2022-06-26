import psycopg2
from decorator import contextmanager
from psycopg2 import connect, extras
from configparser import ConfigParser

parser = ConfigParser()
section = "db_connection"
parser.read('config.ini')
if parser.has_section(section):
    params = dict(parser.items(section))
else:
    raise Exception("section not found")


@contextmanager
def get_cursor():
    """create database cursor"""
    conn = connect(**params)
    try:
        yield conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def insert_dict_into_db(table_name, data_dict, ignore_conflict=False):
    value_list = [tuple(data_dict.values())]
    headers= list(map(lambda x: x.lower(), list(data_dict.keys())))
    conflict_line = ''
    if ignore_conflict:
        conflict_line = 'ON CONFLICT DO NOTHING'

    try:
        with get_cursor() as cur:
            extras.execute_values(cur,
                                  f"""insert into {table_name} ("{'","'.join(headers)}") values %s {conflict_line};""", value_list)
        return cur.rowcount
    except Exception as e:
        pass

def insert_dataframe_into_db(table_name, data_frame):
    pass


def get_result_as_dict(table_name, conditions = None):
    """conditons shuld be list of tuples [(column, value), (column, value)]"""
    if conditions:
        conditions_str = ''
        for i in conditions:
            conditions_str += i[0]+'='+i[1]
        query = f"""select * from {table_name} where {conditions[0]}"""
    else:
        query = f"""select * from {table_name}"""
    try:
        with get_cursor() as cur:
            cur.execute(query)
            result_set = cur.fetchall()
        data = {}
        data = {i[0]: i[1] for i in result_set}
        return data
    except Exception as e:
        return e
