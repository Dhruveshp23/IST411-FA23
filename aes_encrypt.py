from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json

# Replace 'YourLastName' with your actual last name
input_filename = 'payloadPatelD.json'
output_filename = 'encryptedPayloadPatelD.aes'
key_size = 32  # 256-bit key

# Generate a random key
key = get_random_bytes(key_size)

# Create AES cipher object
cipher = AES.new(key, AES.MODE_CBC)

# Read JSON payload
try:
    with open(input_filename, 'r') as file:
        payload = json.load(file)

    # Encrypt JSON payload
    ciphertext = cipher.encrypt(json.dumps(payload).encode())

    # Save encrypted payload and key
    with open(output_filename, 'wb') as file:
        file.write(cipher.iv + ciphertext)

    print(f"Encryption successful. Encrypted payload saved in {output_filename}")
except Exception as e:
    print(f"Error encrypting JSON payload: {e}")
