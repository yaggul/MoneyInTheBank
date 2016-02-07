import sqlite3
from client import Client
from password_validator import PasswordValidator, StrongPasswordError
from pass_hasher import PassHasher
from settings import BLOCK_ATTEMPTS, BLOCK_TIME, DB_NAME, SQL_STRUCTURE_FILE
import datetime

conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row


class SqlManager:
    def __init__(self):
        self.conn = conn
        self.cursor = conn.cursor()
        self.pass_validator = PasswordValidator()
        self.pass_hash = PassHasher()

    def create_structure(self):
        with open(SQL_STRUCTURE_FILE) as f:
            sql_file = f.read()
        self.cursor.executescript(sql_file)

    def change_message(self, new_message, logged_user):
        update_sql = '''UPDATE clients
                                SET message = ?
                                WHERE id = ?'''
        self.cursor.execute(update_sql, (new_message, logged_user.get_id()))
        self.conn.commit()
        logged_user.set_message(new_message)

    def change_pass(self, new_pass, logged_user):
        if self.pass_validator.validate(logged_user.get_username(), new_pass):
            user_pass, user_salt = self.pass_hash.make_pass(new_pass)
        else:
            raise StrongPasswordError
        update_sql = '''UPDATE clients
                                SET password =?,
                                salt =?
                                WHERE id =?'''
        self.cursor.execute(update_sql, (user_pass, user_salt, logged_user.get_id()))
        self.conn.commit()

    def register(self, username, password):
        if self.pass_validator.validate(username, password):
            user_pass, user_salt = self.pass_hash.make_pass(password)
        else:
            return False
        insert_sql = '''INSERT INTO clients (username, password, salt)
                              VALUES (?, ?, ?)'''
        self.cursor.execute(insert_sql, (username, user_pass, user_salt))
        self.conn.commit()

    def __get_salt(self, username):
        sql = '''SELECT username, password, salt
        FROM clients
        WHERE username =?'''
        self.cursor.execute(sql, (username, ))
        data = self.cursor.fetchone()
        if data is None:
            return None
        else:
            return data['salt']

    def _login(self, username):
        if not self._is_blocked(username):


    def _is_blocked(self, username):
        client_id = self.get_client_id_by_username(username)
        now = datetime.datetime.now()
        sql = '''SELECT id, block_end
                   FROM blocked_users
                   WHERE client_id=?
                   ORDER BY id
                   DESC
                   LIMIT 1'''
        self.cursor.execute(sql, (client_id, ))
        result = self.cursor.fetchone()
        if result is None:
            return False
        return (now, result['blocked_end'])

    def block_user(self, username):
        start = datetime.datetime.now()
        end = start + BLOCK_TIME
        client_id = self.get_client_id_by_username(username)
        sql = '''INSERT INTO blocked_users
                   (client_id, blocked_start, blocked_end)
                   VALUES (?, ?, ?)'''

    def create_login_attempt(self, username, password, status='FAIL'):
        login_attempts = BLOCK_ATTEMPTS
        if self.pass_validator.validate(username, password):
            status = 'SUCCEED'
        else:
            if login_attempts > 0:
                login_attempts -= 1
            else:
                status = 'BLOCKED'
        client_id = self.get_client_id_by_username(username)
        now = datetime.datetime.now()
        sql = '''INSERT INTO login_attemps
                   (client_id, attempt_status, time_stamp)
                   values (?, ?, ?)'''
        self.cursor.execute(sql, (client_id, status, now))

    def login(self, username, password):
        self._login(username)
        data = self.__get_salt(username)
        if data is None:
            return False
        select_query = '''SELECT id, username, balance, message
                                   FROM clients
                                   WHERE username =?
                                   AND password =?
                                   LIMIT 1'''
        passkey = self.pass_hash.make_pass(password, data)
        self.cursor.execute(select_query, (username, passkey[0]))
        user = self.cursor.fetchone()

        if(user):
            return Client(user[0], user[1], user[2], user[3])
        else:
            return False

    def get_client_id_by_username(self, username):
        sql = '''SELECT id from clients where username=? '''
        self.cursor.execute(sql, (username, ))
        result = self.cursor.fetchone()
        return result['id']
