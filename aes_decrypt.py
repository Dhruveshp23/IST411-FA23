from Crypto.Cipher import AES
import json

# Replace 'YourLastName' with your actual last name
input_filename = 'encryptedPayloadPatelD.aes'
output_filename = 'decryptedPayloadPatelD.json'
key_size = 32  # 256-bit key

# Read the encrypted payload and IV
try:
    with open(input_filename, 'rb') as file:
        data = file.read()
        iv = data[:AES.block_size]
        ciphertext = data[AES.block_size:]

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the payload
    decrypted_payload = json.loads(cipher.decrypt(ciphertext).decode())

    # Save the decrypted payload
    with open(output_filename, 'w') as file:
        json.dump(decrypted_payload, file, indent=2)

    print(f"Decryption successful. Decrypted payload saved in {output_filename}")
except Exception as e:
    print(f"Error decrypting payload: {e}")
