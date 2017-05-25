#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
from LZW import *


class MyTestCase(unittest.TestCase):
    def test_compress_decompress(self):
        data, decompressed_data = self.TesterFichier("test1.bin", "compress1.lzm", "result1.bin")
        self.assertEqual(data, decompressed_data)

    def test_compress_decompress_loremipsum(self):
        data, decompressed_data = self.TesterFichier("test2.txt", "compress2.lzm", "result2.txt")
        self.assertEqual(data, decompressed_data)

    def test_compress_decompress_image(self):
        data, decompressed_data = self.TesterFichier("test3.jpeg", "compress3.lzm", "result3.jpeg")
        self.assertEqual(data, decompressed_data)

    def test_compress_decompress_bmp(self):
        data, decompressed_data = self.TesterFichier("test4.bmp", "compress4.lzm", "result4.bmp")
        self.assertEqual(data, decompressed_data)

    def test_compress_decompress_random(self):
        data, decompressed_data = self.TesterFichier("test5.random", "compress5.lzm", "result5.random")
        self.assertEqual(data, decompressed_data)

    def TesterFichier(self, tfname, cfname, rfname):
        test_filename = "tests/" + tfname
        compress_filename = "tests/" + cfname
        result_filename = "tests/" + rfname

        clair = open(test_filename, "rb")
        data = clair.read()
        clair.close()

        archive = open(compress_filename, "wb")
        archive.write(compresser(data))
        archive.close()

        archive = open(compress_filename, "rb")
        compressed_data = archive.read()
        archive.close()

        result = open(result_filename, "wb")
        decompressed_data = decompresser(compressed_data)
        result.write(decompressed_data)
        result.close()

        return data, decompressed_data


if __name__ == '__main__':
    unittest.main()
