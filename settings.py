import os

BLOCK_ATTEMPTS = 5
BLOCK_TIME = 20
DB_NAME = 'bank.db'
BASE_DIR = os.path.dirname(__file__)
SQL_STRUCTURE_FILE =os.path.join(BASE_DIR, 'structure.sql')
