from Crypto.Cipher import AES
import json
import pytest

def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_EAX)
    try:
        decrypted_payload = json.loads(cipher.decrypt(ciphertext).decode('utf-8'))
        return decrypted_payload
    except UnicodeDecodeError:
        # If decoding as UTF-8 fails, return the raw bytes
        return cipher.decrypt(ciphertext)

def get_key_from_input():
    # Prompt the user for the key
    key_input = input("Enter the decryption key (16 characters hex string): ").strip()
    try:
        key = bytes.fromhex(key_input)
        if len(key) != 16:  # Check if the key length is appropriate for AES-128
            raise ValueError("Invalid key length. Must be a 16-character hex string.")
        return key
    except ValueError as e:
        print("Error:", e)
        return get_key_from_input()  # Ask for input again if an error occurs

key = get_key_from_input()

@pytest.mark.benchmark(group='decrypt')
def test_decrypt_short(benchmark):
    try:
        with open('encryptedPayloadShort.aes', 'rb') as file:
            encrypted_short = file.read()
        benchmark(decrypt, encrypted_short, key)
    except FileNotFoundError:
        pytest.skip("File not found: encryptedPayloadShort.aes")

@pytest.mark.benchmark(group='decrypt')
def test_decrypt_medium(benchmark):
    try:
        with open('encryptedPayloadMedium.aes', 'rb') as file:
            encrypted_medium = file.read()
        benchmark(decrypt, encrypted_medium, key)
    except FileNotFoundError:
        pytest.skip("File not found: encryptedPayloadMedium.aes")

@pytest.mark.benchmark(group='decrypt')
def test_decrypt_long(benchmark):
    try:
        with open('encryptedPayloadLong.aes', 'rb') as file:
            encrypted_long = file.read()
        benchmark(decrypt, encrypted_long, key)
    except FileNotFoundError:
        pytest.skip("File not found: encryptedPayloadLong.aes")

if __name__ == "__main__":
    pytest.main()
