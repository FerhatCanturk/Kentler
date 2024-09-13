from   cryptography.hazmat.primitives         import padding
from   cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from   cryptography.hazmat.backends           import default_backend
import base64
##########################################################################################################################  
BinaryKEY = b'\xabd\xce\xb7\x05p\x8ePo2\xbe\x04t@\x05f\x19\xb9\xd7NHu\xba\xd9(\x06\xc4\xd1\xd4+T(\xdc'  # 32 bayt uzunluğunda (256-bit) anahtar
BinaryIV  = b'\x00' * 16  # 16 bayt uzunluğunda IV
BinaryKEY = BinaryKEY[:32]
##########################################################################################################################  
def Sifrele(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(BinaryKEY), modes.CBC(BinaryIV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_data)
##########################################################################################################################  
def SifreyiCoz(encrypted_data_base64):
    encrypted_data = base64.b64decode(encrypted_data_base64)
    cipher = Cipher(algorithms.AES(BinaryKEY), modes.CBC(BinaryIV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode('utf-8')
##########################################################################################################################  

