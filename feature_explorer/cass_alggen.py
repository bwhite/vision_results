import pycassa
import time


def get_column_family(column_fam):
    pool = pycassa.ConnectionPool('alggen')
    return pycassa.ColumnFamily(pool, column_fam)


def get_run_id():
    return 'run-%f' % time.time()


def get_score_id():
    return 'score-%f' % time.time()
