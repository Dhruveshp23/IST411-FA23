import hmac
import hashlib
import base64
import json

def generate_signature(msg, key):
    try:
        print("Encoding message and key...")
        
        # Convert the message and key to bytes for HMAC processing
        message = msg.encode('utf-8')
        key = key.encode('utf-8')

        # Create HMAC digesters for SHA1 and MD5
        print("Creating MD5 Signature... Creating SHA1 Signature...")
        digester_sha1 = hmac.new(key, message, hashlib.sha1)
        digester_md5 = hmac.new(key, message, hashlib.md5)

        # Generate the HMAC signatures
        signature_sha1 = digester_sha1.digest()
        signature_md5 = digester_md5.digest()

        # Encode the HMAC signatures in base64
        print("Creating Base64 Signature...")
        signature_sha1_base64 = base64.urlsafe_b64encode(signature_sha1)
        signature_md5_base64 = base64.urlsafe_b64encode(signature_md5)

        return signature_md5, signature_sha1, signature_md5_base64, signature_sha1_base64
    except Exception as e:
        print(f"Error generating signature: {e}")
        return None, None, None, None

def compare_signature(sig1, sig2):
    try:
        # Compare two HMAC signatures to see if they match
        return hmac.compare_digest(sig1, sig2)
    except Exception as e:
        print(f"Error comparing signatures: {e}")
        return False

def print_signatures(msg, key, sig_md5, sig_sha1, sig_sha1_base64):
    print(f"Message: {msg}")
    print(f"Key: {key}")
    print(f"MD5 Signature: {sig_md5.hex()}")
    print(f"SHA1 Signature: {sig_sha1.hex()}")
    print(f"Base64 Signature: {sig_sha1_base64.decode('utf-8')}\n")

if __name__ == "__main__":
    # Define JSON messages and keys for testing
    msg1 = '{"Name": "Joe"}'
    key1 = "This is the key"

    msg2 = '{"Name": "Bob"}'
    key2 = "This is the other key"

    msg3 = '{"Name": "Joe"}'
    key3 = "This is the key"

    # Generate HMAC signatures for each message
    sig1_md5, sig1_sha1, sig1_md5_base64, sig1_sha1_base64 = generate_signature(msg1, key1)
    sig2_md5, sig2_sha1, sig2_md5_base64, sig2_sha1_base64 = generate_signature(msg2, key2)
    sig3_md5, sig3_sha1, sig3_md5_base64, sig3_sha1_base64 = generate_signature(msg3, key3)

    # Print the HMAC and Base64 signatures for each message
    print_signatures(msg1, key1, sig1_md5, sig1_sha1, sig1_sha1_base64)
    print_signatures(msg2, key2, sig2_md5, sig2_sha1, sig2_sha1_base64)
    print_signatures(msg3, key3, sig3_md5, sig3_sha1, sig3_sha1_base64)


    # Compare and print the result of the HMAC signature comparison
    print("Comparing signatures...")
    if compare_signature(sig1_sha1, sig2_sha1):
        print(f"Authentication successful \nHMAC-SHA1 Signatures 1 and 2 match. \n.")
    else:
        print(f"Authentication failed.\nHMAC-SHA1 Signatures 1 and 2 do not match.\n")
    
    if compare_signature(sig1_sha1, sig3_sha1):
        print(f"Authentication successful \nHMAC-SHA1 Signatures 1 and 3 match. \n")
    else:
        print(f"Authentication failed \nHMAC-SHA1 Signatures 1 and 3 do not match. \n")
