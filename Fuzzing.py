#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Script python pour Fuzzer les fonctions de compression/décompression
Si le script crash alors il y a des erreurs à corriger.
Les exceptions attrapées sont celles spécifiées dans la documentation des fonctions
compresser/decompresser.
@author: Thomas Dubier
@author: Pol Kramarenko
@version: 1.0.0
"""

from LZW import *

# Pour installer hypothesis
# pip3 install hypothesis
from hypothesis import given, strategies as st


@given(st.binary(min_size=None, max_size=300))
def test_compress_decompress(buffer):
    """
    Fuzz les fonctions de compression decompression avec des données aléatoire de type
    bytes. La seule exception qui est traitée est de type BufferError comme spécifié dans la doc.
    @param buffer: données aléatoire
    @exception: AssertionError : si la compression/décompression ne retourne pas la valeur initiale
    """
    try:
        data = compress(buffer)
        assert isinstance(data, bytes)
        uncompressed_data = uncompress(data)
        assert isinstance(uncompressed_data, bytes)
        assert buffer == uncompressed_data
    except BufferError:
        pass
    except BitStreamErrorEncode:
        pass


@given(st.binary(min_size=None, max_size=300))
def test_uncompress_only(buffer):
    """
    Fuzz la fonction de décompression avec des données aléatoire de type bytes.
    La seule exception qui est traitée est de type BufferError comme spécifié dans la doc
    de la fonction de décompression
    @param buffer: données aléatoire de type bytes.
    """
    try:
        uncompress_data = uncompress(buffer)
        assert isinstance(uncompress_data, bytes)
    except BufferError:
        pass
    except BitStreamErrorEOF:
        pass


if __name__ == '__main__':
    try:
        test_compress_decompress()
        test_uncompress_only()
    except AssertionError:
        print("[-] test failed")
    print("[+] test pass")