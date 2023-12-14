from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import json

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_encrypted(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def encrypt_data(data, key):
    data_bytes = json.dumps(data).encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data_bytes, AES.block_size))
    return cipher.iv + ct_bytes

def generate_key(key_length):
    return get_random_bytes(16)

def save_key_to_file(key, filename):
    with open(filename, 'wb') as file:
        file.write(key)

def main():
    data = load_json('payloadPatelD.json')
    
    key = generate_key(32)
    key_hex = key.hex()
    encrypted_data = encrypt_data(data, key)

    save_encrypted(encrypted_data, 'encryptedPayloadPatelD.aes')
    save_key_to_file(key, 'encryptionKey.key')
    print("Encryption Key:", key.hex())

if __name__ == "__main__":
    main()
