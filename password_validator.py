from string import punctuation


class StrongPasswordError(Exception):
    pass


class PasswordValidator:
    def __init__(self):
        pass

    def __check_punctuation(self, char):
        return char in punctuation

    def _is_digit(self, password):
        return any([char.isdigit() for char in password])

    def _is_lower(self, password):
        return any([char.islower() for char in password])

    def _is_upper(self, password):
        return any([char.isupper() for char in password])

    def _is_punctuations(self, password):
        return any([self.__check_punctuation(char) for char in password])

    def _is_long_enogh(self, password):
        return len(password) >= 8

    def _is_username_included(self, username, password):
        return username not in password

    def validate(self, username, password):
        return all([self._is_digit(password), self._is_lower(
            password), self._is_punctuations(password), self._is_upper(
            password), self._is_long_enogh(password), self._is_username_included(
            username.lower(), password.lower())])

validator = PasswordValidator()
# passval = PasswordValidator()
print(validator.validate('titko', 'Mitko e sup3r!'))
