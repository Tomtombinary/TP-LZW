#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
from LZW import *
import os


class MyTestCase(unittest.TestCase):
    def test_compress_decompress(self):
        """
        Test tout les fichiers dont le nom commence par test dans le répertoire test
        """
        for filename in os.listdir("tests/"):
            if filename.startswith("test"):
                data, udata = self.TesterFichier(filename,"lzm_"+filename,"res_"+filename)
                self.assertEqual(data, udata)

    def TesterFichier(self, tfname, cfname, rfname):
        test_filename = os.path.join("tests",tfname) # Chemin sous Windows/Linux
        compress_filename = os.path.join("tests",cfname)
        result_filename = os.path.join("tests",rfname)

        clair = open(test_filename, "rb")
        data = clair.read()
        clair.close()

        archive = open(compress_filename, "wb")
        archive.write(compress(data))
        archive.close()

        archive = open(compress_filename, "rb")
        compressed_data = archive.read()
        archive.close()

        result = open(result_filename, "wb")
        decompressed_data = uncompress(compressed_data)
        result.write(decompressed_data)
        result.close()

        return data, decompressed_data


if __name__ == '__main__':
    unittest.main()
