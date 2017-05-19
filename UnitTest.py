import unittest

from LZW import *

class MyTestCase(unittest.TestCase):
    def test_compress_decompress(self):
        clair = open("test1.txt", "rb")
        data = clair.read()
        clair.close()

        archive = open("compress1.lzm", "wb")
        archive.write(compresser(data))
        archive.close()

        archive = open("compress1.lzm", "rb")
        compressed_data = archive.read()
        archive.close()

        resultat = open("result1.txt", "wb")
        resultat.write(decompresser(compressed_data))
        resultat.close()

        self.assertEqual(data,compressed_data)


if __name__ == '__main__':
    unittest.main()
