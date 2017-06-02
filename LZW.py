#!/usr/bin/python3
# -*- coding:utf-8 -*-

from BitStream import *
from math import *


def compress(buffer):
    """
    Compresse un fichier en utilisant l'algorithme LZW. L'algorithme utilise des codes sur n bits selon l'encodeur,
    si les données nécessitent plus de 2**n codes différents pour être
    compressé la fonction lève une exception du type BitStreamError.
    Les données compressées peuvent être plus lourd que les données originales, s'il y a peu d'octets qui se répètent.
    @param buffer: donnée à compress de type bytes
    @param encoder: précise l'encodage à utiliser (par défaut 12 bits)
    @exception: TypeError : si l'argument n'a pas le bon type
    @exception: BufferError : si le buffer ne peut pas être compressé
                - Le buffer est vide
    @exception: BitStreamErrorEncode :
                - le buffer a besoin de plus de 2**12 codes différents
    @return: un buffer de type bytes qui contient la représentation binaire des données compressées
    """
    # Verification des arguments
    if not isinstance(buffer, bytes):
        raise TypeError("a bytes object is required, not '%s'" % type(buffer))

    if len(buffer) <= 0:
        raise BufferError("can't compress a empty buffer")

    code_list = []
    convert_table = {}
    count = 256
    # On initialise le convert_table avec les caractères présents
    for c in buffer:
        convert_table[chr(c)] = c
    # Compresse
    w = ''
    # On parcours chaque lettre de la bytes_list
    for c in buffer:
        # Si le mot existe déjà dans le dictionnaire
        if w + chr(c) in convert_table:
            w = w + chr(c)  # On met à jour le mot en ajoutant le caractère suivant
        # Sinon
        else:
            convert_table[w + chr(c)] = count  # On attribut au mot un code > 255
            count += 1  # On incrémente le code
            code_list.append(convert_table[w])
            w = chr(c)  # On reinitialise le mot avec le caractère courrant

    code_list.append(convert_table[w])

    code_max = max(code_list)
    if code_max >= 256:
        nbits = int(ceil(log2(code_max)))
    else:
        nbits = 8

    encoder = BitStream(nbits)
    encoder.write_codes(code_list)
    return nbits.to_bytes(4,'little') + encoder.to_bytes()

def uncompress(buffer):
    """
    Décompresse un fichier en utilisant l'algorithme LZW avec des codes sur n bits selon le décodeur.
    @param buffer: un buffer en bytes qui contient la représentation binaire des données compressées
    @param decoder: précise le decoder à utiliser (par défaut 12 bits)
    @exception TypeError : si l'argument n'est pas un objet de type bytes
    @exception BufferError : si les données sont malformées, c'est-à-dire :
                - si le premier code n'est pas un caractère
    @exception BitStreamErrorEOF :
                - si le buffer est vide
    @return: un buffer de type bytes qui contient  les données décompressés.
    """
    # Verification des arguments
    if not isinstance(buffer, bytes):
        raise TypeError("a bytes object is required, not '%s'" % type(buffer))

    if len(buffer) <= 4:
        raise BufferError("invalid header")

    nbits = int.from_bytes(buffer[0:4],'little')
    decoder = BitStream(nbits)
    decoder.from_bytes(buffer[4:])

    size = decoder.size_in_code()

    convert_table = {}
    count = 256

    bytes_list = []

    c = decoder.read_code()

    # Le premier code est forcement un caractère sinon le buffer ne peut pas être décompresser
    if c >= 256:
        raise BufferError("malformed bytes object")

    w = chr(c)  # Décode le premier caractère
    bytes_list.append(c)  # On sort le premier caractère
    for i in range(0,size - 1):
        c = decoder.read_code()
        if c > 255 and c in convert_table:  # Si le code n'est pas imprimable mais défini dans le convert_table
            entree = convert_table[c]  # On récupère la valeur correspondante dans le dico
        # Si le code n'est pas imprimable et non défini dans le convert_table
        elif c > 255 and c not in convert_table:
            entree = w + w[0]  # On défini la valeur
        else:  # Si le code est imprimable
            entree = chr(c)  # Alors la valeur est la conversion ASCII du code
        for carac in entree:
            bytes_list.append(ord(carac))  # On ajoute à la bytes_list la valeur decodé
        # On reconstruit le dictionnaire
        convert_table[count] = w + entree[0]
        count += 1
        w = entree

    return bytes(bytes_list)
