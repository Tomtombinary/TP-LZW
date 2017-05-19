#!/usr/bin/python3
# -*- coding:utf-8 -*-

import struct

def compresser(buffer):
    """
    Compress un fichier en utilisant l'algorithme LZW
    :param buffer: donnée à compresser de type bytes
    :return: un buffer de type bytes qui contient la représentation binaire des données compressées
    """
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
            output += struct.pack("<H",convert_table[w]) # On ajoute le code du mot dans la sortie (sur 32 bits)
            w = chr(c)  # On reinitialise le mot avec le caractère courrant
    output+=struct.pack("<H",convert_table[w])
    return output

def decompresser(buffer):
    """
    Decompresse un fichier en utilisant l'algorithme LZW
    :param buffer: un buffer en bytes qui contient la représentation binaire des données compressées
    :return: un buffer de type bytes qui contient  les données décompressés.
    """
    convert_table = {}
    count = 256
    bytes_list = []
    c = struct.unpack("<H",buffer[0:2])[0]          # Premier caractère
    w = chr(c)                                      # Décode le premier caractère
    bytes_list.append(c)                            # On sort le premier caractère
    for i in range(2, len(buffer), 2):              # Pour chaque caractère
        c = struct.unpack("<H",buffer[i:i+2])[0]    # Recupère le code
        if c > 255 and c in convert_table:          # Si le code n'est pas imprimable mais défini dans le convert_table
            entree = convert_table[c]               # On récupère la valeur correspondante dans le dico
        elif c > 255 and c not in convert_table:    # Si le code n'est pas imprimable et non défini dans le convert_table
            entree = w + w[0]                       # On défini la valeur
        else:  # Si le code est imprimable
            entree = chr(c)                         # Alors la valeur est la conversion ASCII du code
        for carac in entree:
            bytes_list.append(ord(carac))              # On ajoute à la bytes_list la valeur decodé
        # On reconstruit le dictionaire
        convert_table[count] = w + entree[0]
        count += 1
        w = entree
    return bytearray(bytes_list)





