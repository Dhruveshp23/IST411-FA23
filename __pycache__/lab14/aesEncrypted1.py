from Crypto.Cipher import AES
import json
import pytest

def encrypt(payload, key, output_file):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(payload).encode('utf-8'))

    # Write the encrypted data to the specified file
    with open(output_file, 'wb') as file:
        file.write(ciphertext)

def get_key_from_input():
    # Prompt the user for the key
    key_input = input("Enter the encryption key (16 characters hex string): ").strip()
    try:
        key = bytes.fromhex(key_input)
        if len(key) != 16:  # Check if the key length is appropriate for AES-128
            raise ValueError("Invalid key length. Must be a 16-character hex string.")
        return key
    except ValueError as e:
        print("Error:", e)
        return get_key_from_input()  # Ask for input again if an error occurs

key = get_key_from_input()

@pytest.mark.benchmark(group='encrypt')
def test_encrypt_short(benchmark):
    output_file = 'encryptedPayloadShort.aes'
    with open('plaintextPayloadShort.json', 'r') as file:
        payload_short = json.load(file)
    benchmark(encrypt, payload_short, key, output_file)

@pytest.mark.benchmark(group='encrypt')
def test_encrypt_medium(benchmark):
    output_file = 'encryptedPayloadMedium.aes'
    with open('plaintextPayloadMedium.json', 'r') as file:
        payload_medium = json.load(file)
    benchmark(encrypt, payload_medium, key, output_file)

@pytest.mark.benchmark(group='encrypt')
def test_encrypt_long(benchmark):
    output_file = 'encryptedPayloadLong.aes'
    with open('plaintextPayloadLong.json', 'r') as file:
        payload_long = json.load(file)
    benchmark(encrypt, payload_long, key, output_file)
