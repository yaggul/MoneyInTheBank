import sys
import unittest
import os

sys.path.append("..")
from password_validator import PasswordValidator
from pass_hasher import PassHasher
from sql_manager import SqlManager
from settings import BLOCK_ATTEMPTS, BLOCK_TIME, DB_NAME, SQL_STRUCTURE_FILE

# '''
# setUP tearDown tearDownClass при всяко пускане на unittest. Сетъп се пуска
# преди всеки метод на unittest, а tearDown i tearDownClass се пускат след пускане
# на всички тестове.
# '''


class SqlManagerTests(unittest.TestCase):
    def setUp(self):
        self.sql_manager = SqlManager()
        self.sql_manager.create_structure()
        self.sql_manager.register('Tester', '123lalal!M')

    def tearDown(self):
        self.sql_manager.cursor.execute('DROP TABLE clients')

    @classmethod
    def tearDownClass(cls):
        os.remove("bank.db")

    def test_register(self):
        self.sql_manager.register('Dinko', 'aA1234!b')

        self.sql_manager.cursor.execute('''SELECT Count(*)
            FROM clients
            WHERE username = (?)''', ('Dinko',))
        users_count = self.sql_manager.cursor.fetchone()

        self.assertEqual(users_count[0], 1)

    def test_register_with_not_valid_password(self):
        self.sql_manager.register('Dinko', '123123')

        self.sql_manager.cursor.execute('''SELECT Count(*)
            FROM clients
            WHERE username = (?)''', ('Dinko',))
        users_count = self.sql_manager.cursor.fetchone()

        self.assertFalse(users_count[0], 1)

    def test_login(self):
        logged_user = self.sql_manager.login('Tester', '123lalal!M')
        self.assertEqual(logged_user.get_username(), 'Tester')

    def test_login_sql_injection_with_username(self):
        logged_user = self.sql_manager.login("' OR 1=1 --", 'lalalalala')
        with self.assertRaises(AttributeError):
            logged_user.get_username("' OR 1=1 --", 'lalalalala')

    def test_login_sql_injection_with_password(self):
        logged_user = self.sql_manager.login(" ' OR 1=1 --", 'lalalalala')
        with self.assertRaises(AttributeError):
            logged_user.get_username(' " OR 1=1 --', 'lalalalala')

#    def test_login_sql_injection_with_username_False(self):
#        logged_user = self.sql_manager.login("' OR 1=1 --", 'lalalalala')
#        self.assertFalse(logged_user.get_username(), '" OR 1=1 --')
#
#     def test_login_sql_injection_with_password_False(self):
#         logged_user = self.sql_manager.login("Tester", "' OR 1=1 --")
#         self.assertFalse(logged_user.get_username(), 'Tester')

    def test_login_wrong_password(self):
        logged_user = self.sql_manager.login('Tester', '123567')
        self.assertFalse(logged_user)

    def test_change_message(self):
        logged_user = self.sql_manager.login('Tester', '123lalal!M')
        new_message = "podaivinototam"
        self.sql_manager.change_message(new_message, logged_user)
        self.assertEqual(logged_user.get_message(), new_message)

    def test_change_password(self):
        logged_user = self.sql_manager.login('Tester', '123lalal!M')
        new_password = "dDamam!!1111"
        self.sql_manager.change_pass(new_password, logged_user)

        logged_user_new_password = self.sql_manager.login('Tester', new_password)
        self.assertEqual(logged_user_new_password.get_username(), 'Tester')

    def test_change_password_with_sql_injection(self):
        self.sql_manager.register('Dinko', 'aA1234!b')
        self.sql_manager.register('Vladko', 'bB1234@a')
        logged_user = self.sql_manager.login('Dinko', 'aA1234!b')
        new_password = "1234' WHERE id = 3 --"
        self.sql_manager.change_pass(new_password, logged_user)

        self.assertFalse(self.sql_manager.login('Vladko', '1234'))


if __name__ == '__main__':
    unittest.main()
