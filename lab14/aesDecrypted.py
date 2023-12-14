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

@pytest.mark.benchmark(group='decrypt')
def test_decrypt_short(benchmark):
    key = bytes.fromhex('e6e7122f0bd7860b3f1be91ce003644c')
    try:
        with open('encryptedPayloadShort.aes', 'rb') as file:
            encrypted_short = file.read()
        benchmark(decrypt, encrypted_short, key)
    except FileNotFoundError:
        pytest.skip("File not found: encryptedPayloadShort.aes")

@pytest.mark.benchmark(group='decrypt')
def test_decrypt_medium(benchmark):
    key = bytes.fromhex('e6e7122f0bd7860b3f1be91ce003644c')
    try:
        with open('encryptedPayloadMedium.aes', 'rb') as file:
            encrypted_medium = file.read()
        benchmark(decrypt, encrypted_medium, key)
    except FileNotFoundError:
        pytest.skip("File not found: encryptedPayloadMedium.aes")

@pytest.mark.benchmark(group='decrypt')
def test_decrypt_long(benchmark):
    key = bytes.fromhex('e6e7122f0bd7860b3f1be91ce003644c')
    try:
        with open('encryptedPayloadLong.aes', 'rb') as file:
            encrypted_long = file.read()
        benchmark(decrypt, encrypted_long, key)
    except FileNotFoundError:
        pytest.skip("File not found: encryptedPayloadLong.aes")

if __name__ == "__main__":
    pytest.main()
