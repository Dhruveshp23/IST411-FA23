from Crypto.Cipher import AES
import json
import pytest

def encrypt(payload, key, output_file):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(payload).encode('utf-8'))

    # Write the encrypted data to the specified file
    with open(output_file, 'wb') as file:
        file.write(ciphertext)

@pytest.mark.benchmark(group='encrypt')
def test_encrypt_short(benchmark):
    key = bytes.fromhex('e6e7122f0bd7860b3f1be91ce003644c')
    output_file = 'encryptedPayloadShort.aes'
    with open('plaintextPayloadShort.json', 'r') as file:
        payload_short = json.load(file)
    benchmark(encrypt, payload_short, key, output_file)

@pytest.mark.benchmark(group='encrypt')
def test_encrypt_medium(benchmark):
    key = bytes.fromhex('e6e7122f0bd7860b3f1be91ce003644c')
    output_file = 'encryptedPayloadMedium.aes'
    with open('plaintextPayloadMedium.json', 'r') as file:
        payload_medium = json.load(file)
    benchmark(encrypt, payload_medium, key, output_file)

@pytest.mark.benchmark(group='encrypt')
def test_encrypt_long(benchmark):
    key = bytes.fromhex('e6e7122f0bd7860b3f1be91ce003644c')
    output_file = 'encryptedPayloadLong.aes'
    with open('plaintextPayloadLong.json', 'r') as file:
        payload_long = json.load(file)
    benchmark(encrypt, payload_long, key, output_file)

if __name__ == "__main__":
    pytest.main()
