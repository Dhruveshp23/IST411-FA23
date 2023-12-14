# Project: Lab 8 SFTP
# Purpose Details: Learning to use secure file transfer protocol
# Course: IST 411
# Author: Dhruvesh
# Date Developed: 10/13/2023
# Last Date Changed: 10/15/2023
# Rev: 1


import pysftp
import getpass
import sys

def main():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Create an instance of CnOpts and set hostkeys to None (disable host key verification)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    # Define the connection information
    cinfo = {
        'cnopts': cnopts,
        'host': '172.29.135.40',
        'username': username,
        'password': password,
        'port': 1855
    }

    try:
        # Establish an SFTP connection
        with pysftp.Connection(**cinfo) as sftp:
            print("Connected to SFTP server")
            sftp.chdir("lab8/ftpsend")

            # List the contents of lab8/ftpsend
            print("Contents of lab8/ftpsend:")
            files = sftp.listdir()
            for file in files:
                print(file)

            # Change directory to lab8/ftprecieive
            try:
                sftp.chdir("/home/" + username + "/lab8/ftpreceive")
            except Exception as cd_error:
                print("Error changing directory:", str(cd_error))
                sys.exit(1)

            # Specify the full local path and remote path for the file transfer
            local_path = "/home/vrp5109/lab8/ftpsend/JSONPayload.json"
            remote_path = "/home/" + username + "/lab8/ftpreceive/JSONPayload.json"

            try:
                sftp.put(local_path, remote_path)
                print("File JSONPayload.json transferred to lab8/ftpreceive/")
            except Exception as put_error:
                print("Error transferring file:", str(put_error))
                sys.exit(1)

            # List the contents of lab8/ftpreceive:
            print("Contents of lab8/ftpreceive:")
            files = sftp.listdir()
            for file in files:
                print(file)

            # Remove the JSONPayload.json from lab8/ftpsend
            try:
                sftp.remove("JSONPayload.json")
                print("Removed JSONPayload.json from lab8/ftpsend/")
            except Exception as remove_error:
                print("Error removing file:", str(remove_error))
                sys.exit(1)

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        print("Closing SFTP connection")

if __name__ == "__main__":
    main()
