from file import File
import tree
from folder import Folder
import secrets
import json
from base64 import decode, urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()

class Vault(File):

    def __init__(self, name, path, params = {}):

        self.params = {}
        for key, value in params.items():
            setattr(self, key, value)
        
        self.name = name
        self.path = path

    # Decrypt and unlock the vault
    def decrypt(self, password):
        encrypted = self.read(limit=False)
        decrypted = passwordDecrypt(encrypted, password).decode()
        structured = json.loads(decrypted)
        data = { structured.get('name'): structured }
        contents = tree._loadExplore(self.getParentPath() + "/", data)[0]

        return contents
        

def encrypt(object, password):

    # Ignore if object cannot be modified
    #if hasattr(object, 'invulnerable') and object.invulnerable: return None

    # Unload the object
    data = tree._unloadExplore(object)

    # Serialize the object
    serialized = json.dumps(data)

    # Encrypt the serialized data
    encrypted = passwordEncrypt(serialized.encode(), password)

    # Create the vault
    vault = Vault(object.getName(), object.getParentPath())
    vault.write(encrypted)
    return vault
    

# Derive a key from a password and salt
def _derive_key(password, salt, iterations):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend
    )

    return b64e(kdf.derive(password))

# Encrypt a message using the password
def passwordEncrypt(message, password, iterations = 100000):
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message))
        )
    )
    
# Decrypt a message using the password
def passwordDecrypt(token, password):
    decoded = b64d(token)
    salt, iterations, token = decoded[:16], int.from_bytes(decoded[16:20], 'big'), b64e(decoded[20:])
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)
