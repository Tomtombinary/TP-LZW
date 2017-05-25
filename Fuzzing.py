#!/usr/bin/python3

"""
@author: Thomas DUBIER
Script python pour Fuzzer les fonctions de compression/décompression
Si le script crash alors il y a des erreurs à corriger.
Les exceptions attrapées sont celles spécifiées dans la documentation des fonctions
compresser/decompresser
"""
from LZW import *

# Pour installer hypothesis
# pip3 install hypothesis
from hypothesis import given, strategies as st


@given(st.binary(min_size=None,max_size=1000))
def test_compress_decompress(buffer):
    """
    Fuzz les fonctions de compression decompression avec des données aléatoire de type
    bytes. La seule exception qui est traitée est de type BufferError comme spécifié dans la doc.
    :param buffer: données aléatoire
    :raise: AssertionError : si la compression/décompression ne retourne pas la valeur initiale
    :return: rien
    """
    try:
        data = compresser(buffer)
        assert isinstance(data, bytes)
        uncompress = decompresser(data)
        assert isinstance(uncompress,bytes)
        assert buffer == uncompress
    except BufferError:
        pass

@given(st.binary(min_size=None,max_size=1000))
def test_decompress_only(buffer):
    """
    Fuzz la fonction de décompression avec des données aléatoire de type bytes.
    La seule exception qui est traitée est de type BufferError comme spécifié dans la doc
    de la fonction de décompression
    :param buffer: données aléatoire de type bytes.
    :return: rien
    """
    try:
        uncompress = decompresser(buffer)
        assert isinstance(uncompress,bytes)
    except BufferError:
        pass

test_compress_decompress()
test_decompress_only()