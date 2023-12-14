import zlib
import lzma
import bz2
import time
import os

class Compress:
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder

    def compress(self, algorithm, compression_func, extension):
        try:
            with open(self.input_file, 'rb') as f:
                payload = f.read()

            start_time = time.time()
            compressed_data = compression_func(payload)
            end_time = time.time()

            compressed_file = os.path.join(self.output_folder, f'compressed_{algorithm}.{extension}')
            with open(compressed_file, 'wb') as f:
                f.write(compressed_data)

            original_size = len(payload)
            compressed_size = len(compressed_data)

            print(f'{algorithm.capitalize()} Compression - Original Size: {original_size} bytes, Compressed Size: {compressed_size} bytes')
            print(f'Compression Time: {end_time - start_time:.4f} seconds')
            return compressed_file
        except Exception as e:
            print(f'{algorithm.capitalize()} Compression failed: {e}')
            return None

    @staticmethod
    def calculate_crc32(file_path):
        try:
            with open(file_path, 'rb') as f:
                payload = f.read()
                checksum = zlib.crc32(payload) & 0xFFFFFFFF
            return checksum
        except Exception as e:
            print(f'Failed to calculate CRC32 checksum for file {file_path}: {e}')
            return None

class Decompress:
    def __init__(self, input_folder):
        self.input_folder = input_folder

    def decompress(self, compressed_file, decompression_func, algorithm, extension):
        try:
            with open(compressed_file, 'rb') as f:
                compressed_data = f.read()

            start_time = time.time()
            payload = decompression_func(compressed_data)
            end_time = time.time()

            decompressed_file = os.path.join(self.input_folder, f'decompressed_{algorithm}.{extension}')
            with open(decompressed_file, 'wb') as f:
                f.write(payload)

            decompressed_size = len(payload)
            print(f'{algorithm.capitalize()} Decompression - Decompressed Size: {decompressed_size} bytes')
            print(f'Decompression Time: {end_time - start_time:.4f} seconds')
            return decompressed_file
        except Exception as e:
            print(f'{algorithm.capitalize()} Decompression failed: {e}')
            return None

if __name__ == "__main__":
    input_file = "payloadPatelD.json"
    output_folder = "Lab11"
    input_folder = "Lab11"

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    compress_obj = Compress(input_file, output_folder)
    decompress_obj = Decompress(input_folder)

    compression_results = {}
    decompression_results = {}

    compression_algorithms = {
        'zlib': (zlib.compress, 'json'),
        'lzma': (lzma.compress, 'json'),
        'bz2': (bz2.compress, 'json')
    }

    decompression_algorithms = {
        'zlib': (zlib.decompress, 'json'),
        'lzma': (lzma.decompress, 'json'),
        'bz2': (bz2.decompress, 'json')
    }

    for algorithm, (compress_func, extension) in compression_algorithms.items():
        compressed_file = compress_obj.compress(algorithm, compress_func, extension)
        if compressed_file:
            compression_results[algorithm] = compressed_file

    for algorithm, (decompress_func, extension) in decompression_algorithms.items():
        if algorithm in compression_results:
            decompressed_file = decompress_obj.decompress(compression_results[algorithm], decompress_func, algorithm, extension)
            if decompressed_file:
                decompression_results[algorithm] = decompressed_file

    print("CRC32 Checksums:")
    original_crc32 = Compress.calculate_crc32(input_file)
    print(f'Original Checksum (CRC32): {original_crc32}')

    for algorithm, decompressed_file in decompression_results.items():
        checksum = Compress.calculate_crc32(decompressed_file)
        print(f'{algorithm.capitalize()} Decompressed Checksum (CRC32): {checksum}')

    print("Operations completed successfully.")
