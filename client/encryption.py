"""
Telegraf Encryption Module
End-to-end encryption using RSA + AES
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class EncryptionManager:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.peer_public_keys = {}

    def generate_keys(self):
        """Generate RSA key pair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def get_public_key_pem(self):
        """Export public key as PEM string"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return base64.b64encode(pem).decode('utf-8')

    def load_peer_public_key(self, user_id, pem_string):
        """Load peer's public key"""
        try:
            pem_bytes = base64.b64decode(pem_string)
            public_key = serialization.load_pem_public_key(
                pem_bytes,
                backend=default_backend()
            )
            self.peer_public_keys[user_id] = public_key
            return True
        except Exception as e:
            print(f"Error loading public key: {e}")
            return False

    def encrypt_message(self, message, recipient_id):
        """Encrypt message using AES + RSA hybrid encryption"""
        if recipient_id not in self.peer_public_keys:
            return None

        try:
            # Generate random AES key
            aes_key = os.urandom(32)  # 256-bit key
            iv = os.urandom(16)

            # Encrypt message with AES
            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()

            # Pad message to AES block size
            message_bytes = message.encode('utf-8')
            padding_length = 16 - (len(message_bytes) % 16)
            padded_message = message_bytes + bytes([padding_length] * padding_length)

            encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

            # Encrypt AES key with recipient's RSA public key
            peer_public_key = self.peer_public_keys[recipient_id]
            encrypted_key = peer_public_key.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Return encrypted data
            return {
                'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
                'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8'),
                'iv': base64.b64encode(iv).decode('utf-8')
            }

        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    def decrypt_message(self, encrypted_data):
        """Decrypt message using RSA + AES"""
        try:
            # Decrypt AES key with private RSA key
            encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
            aes_key = self.private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Decrypt message with AES
            iv = base64.b64decode(encrypted_data['iv'])
            encrypted_message = base64.b64decode(encrypted_data['encrypted_message'])

            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()

            padded_message = decryptor.update(encrypted_message) + decryptor.finalize()

            # Remove padding
            padding_length = padded_message[-1]
            message = padded_message[:-padding_length]

            return message.decode('utf-8')

        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def encrypt_file(self, file_data, recipient_id):
        """Encrypt file data"""
        if recipient_id not in self.peer_public_keys:
            return None

        try:
            # Generate random AES key
            aes_key = os.urandom(32)
            iv = os.urandom(16)

            # Encrypt file with AES
            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()

            # Pad file data
            padding_length = 16 - (len(file_data) % 16)
            padded_data = file_data + bytes([padding_length] * padding_length)

            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            # Encrypt AES key with RSA
            peer_public_key = self.peer_public_keys[recipient_id]
            encrypted_key = peer_public_key.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return {
                'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
                'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8'),
                'iv': base64.b64encode(iv).decode('utf-8')
            }

        except Exception as e:
            print(f"File encryption error: {e}")
            return None

    def decrypt_file(self, encrypted_data):
        """Decrypt file data"""
        try:
            # Decrypt AES key
            encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
            aes_key = self.private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Decrypt file
            iv = base64.b64decode(encrypted_data['iv'])
            encrypted_file = base64.b64decode(encrypted_data['encrypted_data'])

            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()

            padded_data = decryptor.update(encrypted_file) + decryptor.finalize()

            # Remove padding
            padding_length = padded_data[-1]
            file_data = padded_data[:-padding_length]

            return file_data

        except Exception as e:
            print(f"File decryption error: {e}")
            return None
