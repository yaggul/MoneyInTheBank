import hashlib
from random import getrandbits


class PassHasher:
    def __init__(self):
        pass

    def make_spice(self):
        spice = getrandbits(256)
        m = hashlib.sha256()
        m.update(str(spice).encode('utf-8'))

        return m.hexdigest()

    def make_pass(self, password, salt=None):
        if salt is None:
            salt = self.make_spice()
        m = hashlib.sha256()
        concated_password = password + salt
        m.update(concated_password.encode('utf-8'))
        passkey = m.hexdigest()
        return (passkey, salt)
