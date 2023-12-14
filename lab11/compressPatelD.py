import zlib
import lzma
import bz2
import time
import os

class Compress:
    def __init__(self, input_file, output_folder):
        """
        Constructor for the Compress class.

        Args:
            input_file (str): Path to the input JSON file to be compressed.
            output_folder (str): Path to the folder where compressed files will be stored.
        """
        self.input_file = input_file
        self.output_folder = output_folder

    def compress_zlib(self):
        """
        Compress the input JSON file using zlib.

        Returns:
            str: Path to the compressed file.
        """
        try:
            with open(self.input_file, 'rb') as f:
                payload = f.read()
            
            start_time = time.time()
            compressed_data = zlib.compress(payload, level=zlib.Z_BEST_COMPRESSION)
            end_time = time.time()

            compressed_file = os.path.join(self.output_folder, 'compressed_zlib.json')
            with open(compressed_file, 'wb') as f:
                f.write(compressed_data)

            print(f'Zlib Compression - Original Size: {len(payload)} bytes, Compressed Size: {len(compressed_data)} bytes')
            print(f'Compression Time: {end_time - start_time:.4f} seconds')
            return compressed_file
        except Exception as e:
            print(f'Zlib Compression failed: {e}')
            return None

    def compress_lzma(self):
        """
        Compress the input JSON file using LZMA.

        Returns:
            str: Path to the compressed file.
        """
        try:
            with open(self.input_file, 'rb') as f:
                payload = f.read()
            
            start_time = time.time()
            compressed_data = lzma.compress(payload, format=lzma.FORMAT_ALONE)
            end_time = time.time()

            compressed_file = os.path.join(self.output_folder, 'compressed_lzma.json')
            with open(compressed_file, 'wb') as f:
                f.write(compressed_data)

            print(f'LZMA Compression - Original Size: {len(payload)} bytes, Compressed Size: {len(compressed_data)} bytes')
            print(f'Compression Time: {end_time - start_time:.4f} seconds')
            return compressed_file
        except Exception as e:
            print(f'LZMA Compression failed: {e}')
            return None

    def compress_bz2(self):
        """
        Compress the input JSON file using BZ2.

        Returns:
            str: Path to the compressed file.
        """
        try:
            with open(self.input_file, 'rb') as f:
                payload = f.read()
            
            start_time = time.time()
            compressed_data = bz2.compress(payload)
            end_time = time.time()

            compressed_file = os.path.join(self.output_folder, 'compressed_bz2.json')
            with open(compressed_file, 'wb') as f:
                f.write(compressed_data)

            print(f'BZ2 Compression - Original Size: {len(payload)} bytes, Compressed Size: {len(compressed_data)} bytes')
            print(f'Compression Time: {end_time - start_time:.4f} seconds')
            return compressed_file
        except Exception as e:
            print(f'BZ2 Compression failed: {e}')
            return None

    def calculate_crc32(self, file_path):
        """
        Calculate the CRC32 checksum of a file.

        Args:
            file_path (str): Path to the file for which you want to calculate the checksum.

        Returns:
            int: CRC32 checksum.
        """
        try:
            with open(file_path, 'rb') as f:
                payload = f.read()
                checksum = zlib.crc32(payload) & 0xFFFFFFFF  # Ensure a positive integer result
            return checksum
        except Exception as e:
            print(f'Failed to calculate CRC32 checksum: {e}')
            return None

class Decompress:
    def __init__(self, input_folder):
        """
        Constructor for the Decompress class.

        Args:
            input_folder (str): Path to the folder containing compressed files.
        """
        self.input_folder = input_folder

    def decompress_zlib(self, compressed_file):
        """
        Decompress a zlib-compressed file.

        Args:
            compressed_file (str): Path to the zlib-compressed file.

        Returns:
            str: Path to the decompressed file.
        """
        try:
            with open(compressed_file, 'rb') as f:
                compressed_data = f.read()

            start_time = time.time()
            payload = zlib.decompress(compressed_data)
            end_time = time.time()

            decompressed_file = os.path.join(self.input_folder, 'decompressed_zlib.json')
            with open(decompressed_file, 'wb') as f:
                f.write(payload)

            print(f'Zlib Decompression - Decompressed Size: {len(payload)} bytes')
            print(f'Decompression Time: {end_time - start_time:.4f} seconds')
            return decompressed_file
        except Exception as e:
            print(f'Zlib Decompression failed: {e}')
            return None

    def decompress_lzma(self, compressed_file):
        """
        Decompress an LZMA-compressed file.

        Args:
            compressed_file (str): Path to the LZMA-compressed file.

        Returns:
            str: Path to the decompressed file.
        """
        try:
            with open(compressed_file, 'rb') as f:
                compressed_data = f.read()

            start_time = time.time()
            payload = lzma.decompress(compressed_data, format=lzma.FORMAT_ALONE)
            end_time = time.time()

            decompressed_file = os.path.join(self.input_folder, 'decompressed_lzma.json')
            with open(decompressed_file, 'wb') as f:
                f.write(payload)

            print(f'LZMA Decompression - Decompressed Size: {len(payload)} bytes')
            print(f'Decompression Time: {end_time - start_time:.4f} seconds')
            return decompressed_file
        except Exception as e:
            print(f'LZMA Decompression failed: {e}')
            return None

    def decompress_bz2(self, compressed_file):
        """
        Decompress a BZ2-compressed file.

        Args:
            compressed_file (str): Path to the BZ2-compressed file.

        Returns:
            str: Path to the decompressed file.
        """
        try:
            with open(compressed_file, 'rb') as f:
                compressed_data = f.read()

            start_time = time.time()
            payload = bz2.decompress(compressed_data)
            end_time = time.time()

            decompressed_file = os.path.join(self.input_folder, 'decompressed_bz2.json')
            with open(decompressed_file, 'wb') as f:
                f.write(payload)

            print(f'BZ2 Decompression - Decompressed Size: {len(payload)} bytes')
            print(f'Decompression Time: {end_time - start_time:.4f} seconds')
            return decompressed_file
        except Exception as e:
            print(f'BZ2 Decompression failed: {e}')
            return None

if __name__ == "__main__":
    input_file = "payloadPatelD.json"
    output_folder = "Lab11"
    input_folder = "Lab11"

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    compress_obj = Compress(input_file, output_folder)
    decompress_obj = Decompress(input_folder)

    # Compression
    compressed_zlib = compress_obj.compress_zlib()
    compressed_lzma = compress_obj.compress_lzma()
    compressed_bz2 = compress_obj.compress_bz2()

    # Decompression
    decompressed_zlib = decompress_obj.decompress_zlib(compressed_zlib)
    decompressed_lzma = decompress_obj.decompress_lzma(compressed_lzma)
    decompressed_bz2 = decompress_obj.decompress_bz2(compressed_bz2)

    # Calculate CRC32 checksums
    print("CRC32 Checksums:")
    original_crc32 = compress_obj.calculate_crc32(input_file)
    print(f'Original Checksum (CRC32): {original_crc32}')

    zlib_crc32 = compress_obj.calculate_crc32(decompressed_zlib)
    print(f'Zlib Decompressed Checksum (CRC32): {zlib_crc32}')

    lzma_crc32 = compress_obj.calculate_crc32(decompressed_lzma)
    print(f'LZMA Decompressed Checksum (CRC32): {lzma_crc32}')

    bz2_crc32 = compress_obj.calculate_crc32(decompressed_bz2)
    print(f'BZ2 Decompressed Checksum (CRC32): {bz2_crc32}')

    # Print full details of all operations with timestamps to the console
    print("Operations completed successfully.")
