#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
from LZW import *
import os


class MyTestCase(unittest.TestCase):
    def test_compress_decompress(self):
        """
        Test tout les fichiers dont le nom commence par test dans le
        :return:
        """
        for filename in os.listdir("tests/"):
            if filename.startswith("test"):
                data, decompressed_data = self.TesterFichier(filename,"lzm_"+filename,"res_"+filename)
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
