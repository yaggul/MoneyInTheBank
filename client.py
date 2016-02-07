class Client():
    def __init__(self, _id, username, balance, message):
        self.__id = _id
        self.__username = username
        self.__balance = balance
        self.__message = message

    def get_username(self):
        return self.__username

    def get_balance(self):
        return self.__balance

    def get_id(self):
        return self.__id

    def get_message(self):
        return self.__message

    def set_message(self, new_message):
        self.__message = new_message
