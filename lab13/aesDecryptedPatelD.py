from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

# Load encrypted data from a file
def load_encrypted_data(filename):
    with open(filename, 'rb') as file:
        return file.read()

# Decrypt data using the provided key
def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = cipher.decrypt(encrypted_data[AES.block_size:])
    return json.loads(unpad(decrypted, AES.block_size).decode('utf-8'))

# Main function to decrypt and display the message
def main():
    filename = 'encryptedPayloadPatelD.aes'

    key_input = input("Enter the key in hexadecimal format: ").strip()
    try:
        key = bytes.fromhex(key_input)
    except ValueError:
        print("Invalid key format. Key must be in hexadecimal format.")
        return

    encrypted_data = load_encrypted_data(filename)
    try:
        decrypted_data = decrypt_data(encrypted_data, key)
        if 'message' in decrypted_data:
            message = decrypted_data['message']  # Extracting the 'message' value
            print("Decrypted Message:")
            print(message)
        else:
            print("No 'message' found in decrypted data.")
    except (ValueError, KeyError):
        print("Decryption failed. Incorrect key or data format.")

if __name__ == "__main__":
    main()
