#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Fichier de tests unitaire
@author: Thomas Dubier
@author: Pol Kramarenko
@version: 1.0.0
"""

import unittest
from LZW import *
from BitStream import *
import os


class MyTestCase(unittest.TestCase):
    def test_compress_decompress(self):
        """
        Test tout les fichiers dont le nom commence par test dans le répertoire test
        @exception AssertionError : si le test échoue
        """
        for filename in os.listdir("tests/"):
            if filename.startswith("test"):
                data, udata = MyTestCase.TesterFichier(filename, "lzm_" + filename, "res_" + filename)
                self.assertEqual(data, udata)

    def test_bitstream_init_invalid(self):
        """
        Test la construction d'un bitstream avec de mauvais paramètre en entrée
        @exception AssertionError : si le test échoue
        """
        exception = None
        try:
            bitstream = BitStream(2)
        except Exception as e:
            exception = e

        self.assertEqual(isinstance(exception, BitStreamUnsupportedParameter), True)

        exception = None
        try:
            bitstream = BitStream(-8)
        except Exception as e:
            exception = e

        self.assertEqual(isinstance(exception, BitStreamUnsupportedParameter), True)

        exception = None
        try:
            bitstream = BitStream("18")
        except Exception as e:
            exception = e

        self.assertEqual(isinstance(exception, TypeError), True)

    def test_bitstream_init(self):
        """
        Test la construction d'un bitstream valide
        @exception AssertionError : si le test échoue
        """
        exception = None
        try:
            bitstream = BitStream(15)
        except Exception as e:
            exception = e

        self.assertEqual(exception, None)

    def test_bitstream_write(self):
        """
        Test l'écriture de données valide dans un bitstream
        @exception AssertionError : si le test échoue
        """
        bitstream = BitStream(9)
        bitstream.write_code(10)
        bitstream.write_code(259)

        self.assertEqual(bitstream.read_code(), 10)
        self.assertEqual(bitstream.read_code(), 259)

        bitstream = BitStream(12)
        bitstream.write_code(2 ** 12 - 1)
        bitstream.write_code(259)

        self.assertEqual(bitstream.read_code(), 2 ** 12 - 1)
        self.assertEqual(bitstream.read_code(), 259)

    def test_bitstream_write_negative(self):
        """
        Test l'écriture de données invalide dans un bitstream
        @exception AssertionError : si le test échoue
        """
        bitstream = BitStream(9)

        exc = None
        try:
            bitstream.write_code(-1)
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, BitStreamErrorEncode), True)

        bitstream = BitStream(12)
        exc = None
        try:
            bitstream.write_code("12")
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, TypeError), True)

        exc = None
        try:
            bitstream.write_code(b'\x04')
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, TypeError), True)

        bitstream = BitStream(9)
        exc = None
        try:
            bitstream.write_code(2 ** 9)
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, BitStreamErrorEncode), True)

        try:
            bitstream.write_code(21356)
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, BitStreamErrorEncode), True)

    def test_bitstream_read_EOF(self):
        """
        Test la lecture alors que le flux est vide
        @exception AssertionError : si le test échoue
        """
        bitstream = BitStream(10)
        bitstream.write_code(10)

        bitstream.read_code()

        exc = None
        try:
            bitstream.read_code()
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, BitStreamErrorEOF), True)

        exc = None
        try:
            bitstream.read_codes()
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, BitStreamErrorEOF), True)

    def test_bitstream_write_codes(self):
        """
        Test l'écriture d'une liste de codes
        @exception AssertionError : si le test échoue
        """
        bitstream = BitStream(9)
        bitstream.write_codes([123, 259, 0])

        self.assertEqual(bitstream.read_code(), 123)
        self.assertEqual(bitstream.read_code(), 259)
        self.assertEqual(bitstream.read_code(), 0)

    def test_bitstream_read_codes(self):
        """
        Test la lecture complete du flux de bit
        @exception AssertionError : si le test échoue
        """
        bitstream = BitStream(12)
        bitstream.write_code(10)
        bitstream.write_code(29)
        bitstream.write_code(2 ** 12 - 1)

        self.assertEqual(bitstream.read_codes(), [10, 29, 2 ** 12 - 1])

    def test_bitstream_write_codes_exception(self):
        """
        Test l'écriture d'une liste de codes invalid
        @exception AssertionError : si le test échoue
        """
        bitstream = BitStream(9)

        exc = None
        try:
            bitstream.write_codes([12, 0, 1, -1])
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, BitStreamErrorEncode), True)

        exc = None
        try:
            bitstream.write_codes(b'\x01\x02')
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, TypeError), True)

        exc = None
        try:
            bitstream.write_codes([12, 1567, 5])
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, BitStreamErrorEncode), True)

        exc = None
        try:
            bitstream.write_codes([12, 5.2, 5])
        except Exception as e:
            exc = e

        self.assertEqual(isinstance(exc, TypeError), True)

    @staticmethod
    def TesterFichier(tfname, cfname, rfname):
        """
        Effectue la compression/décompression d'un fichier de test.
        Tout les fichiers de test, et les résultats se trouve dans un dossier
        tests.
        @param tfname: nom du fichier de test
        @param cfname: nom du fichier de test après compression
        @param rfname: nom du fichier de test après décompression
        @return: les données originales, les données décompressée
        """
        test_filename = os.path.join("tests", tfname)  # Chemin sous Windows/Linux
        compress_filename = os.path.join("tests", cfname)
        result_filename = os.path.join("tests", rfname)

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
