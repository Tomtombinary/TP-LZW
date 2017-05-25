#!/usr/bin/python3
# -*- coding:utf-8 -*-

import struct


def compresser(buffer):
    """
    Compresse un fichier en utilisant l'algorithme LZW. L'algorithme utilise des codes sur 16 bits,
    et donc peut encoder 65536 codes différents, si les données nécessitent plus de 65536 codes pour être
    compressé la fonction lève une exception du type BufferError.
    Les données compressées peuvent être plus lourd que les données originales, s'il y a peu d'octets qui se répètent.
    :param buffer: donnée à compresser de type bytes
    :raise: TypeError : si l'argument n'a pas le bon type
    :raise: BufferError : si le buffer ne peut pas être compressé
    :return: un buffer de type bytes qui contient la représentation binaire des données compressées
    """
    # Verification des arguments
    if not isinstance(buffer, bytes):
        raise TypeError("a bytes object is required, not '%s'" % type(buffer))

    output = b''
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
            if count >= 65536:
                raise BufferError("buffer can't be compressed, it need more than 65536 different code")
            output += struct.pack("<H", convert_table[w])  # On ajoute le code du mot dans la sortie (sur 16 bits)
            w = chr(c)  # On reinitialise le mot avec le caractère courrant
    output += struct.pack("<H", convert_table[w])
    return output


def decompresser(buffer):
    """
    Décompresse un fichier en utilisant l'algorithme LZW avec des codes sur 16 bits.
    :param buffer: un buffer en bytes qui contient la représentation binaire des données compressées
    :raise: TypeError : si l'argument n'est pas un objet de type bytes
    :raise: BufferError : si les données sont malformées, c'est-à-dire :
                - s'il y'a un nombre impair d'octets
                - si le premier code n'est pas un caractère
    :return: un buffer de type bytes qui contient  les données décompressés.
    """
    # Verification des arguments
    if not isinstance(buffer, bytes):
        raise TypeError("a bytes object is required, not '%s'" % type(buffer))
    # Verifie si le buffer a une taille pair (16 bits par code)
    if len(buffer) % 2 != 0:
        raise BufferError("a bytes object of pair length is required, actual length is %d" % len(buffer))

    convert_table = {}
    count = 256
    bytes_list = []
    c = struct.unpack("<H", buffer[0:2])[0]  # Premier caractère
    # Le premier code est forcement un caractère sinon le buffer ne peut pas être décompresser
    if c >= 256:
        raise BufferError("malformed bytes object")

    w = chr(c)  # Décode le premier caractère
    bytes_list.append(c)  # On sort le premier caractère
    for i in range(2, len(buffer), 2):  # Pour chaque caractère
        c = struct.unpack("<H", buffer[i:i + 2])[0]  # Recupère le code
        if c > 255 and c in convert_table:  # Si le code n'est pas imprimable mais défini dans le convert_table
            entree = convert_table[c]  # On récupère la valeur correspondante dans le dico
        # Si le code n'est pas imprimable et non défini dans le convert_table
        elif c > 255 and c not in convert_table:
            entree = w + w[0]  # On défini la valeur
        else:  # Si le code est imprimable
            entree = chr(c)  # Alors la valeur est la conversion ASCII du code
        for carac in entree:
            bytes_list.append(ord(carac))  # On ajoute à la bytes_list la valeur decodé
        # On reconstruit le dictionaire
        convert_table[count] = w + entree[0]
        count += 1
        w = entree

    return bytes(bytes_list)
