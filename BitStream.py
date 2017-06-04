#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
Module pour gèrer un flux de données encodé sur n bits
@author: Thomas Dubier
@author: Pol Kramarenko
@version: 1.0.0
"""

from math import *
from copy import *


class BitStreamError(Exception):
    """
    Classe abstraite représentant une exception générale pour un BitStream
    """

    def __init__(self, message):
        super(BitStreamError, self).__init__(message)


class BitStreamErrorEOF(BitStreamError):
    """
    Exception levée lorsqu'on essaye de lire dans le flux de bit alors
    que celui-ci est vide.
    """

    def __init__(self):
        super(BitStreamErrorEOF, self).__init__("Error, stream end")


class BitStreamErrorEncode(BitStreamError):
    """
    Exception levée lorsque l'encodage d'un code échoue
    """

    def __init__(self, message):
        super(BitStreamErrorEncode, self).__init__(message)


class BitStreamUnsupportedParameter(BitStreamError):
    """
    Exception levée lorsqu'un paramètre de configuration du flux, n'est
    pas valide.
    """

    def __init__(self, message):
        super(BitStreamUnsupportedParameter, self).__init__(message)


class BitStream:
    """
    Classe pour représenter un flux de bits
    """
    def __init__(self, nbits):
        """
        Initialise un flux de bit
        @param nbits: nombre de bits sur lequel sont encodé les codes. Il doit être supérieur ou égal à 8
        @exception BitStreamUnsupportedParameter: si le paramètre nbits est inférieur à 8
        @exception TypeError : si le paramètre nbits n'est pas un entier
        """
        if not isinstance(nbits, int):
            raise TypeError("nbits must be a integer")

        if nbits < 8:
            raise BitStreamUnsupportedParameter("nbits must be greater than or equal to 8")

        self._nbits = nbits
        self._stream = list()

    def write_codes(self, code_list):
        """
        Nourri le flux avec une liste de codes entier
        @param code_list : la liste de codes à encoder sur nbits
        @exception BitStreamErrorEncode : le code nécessite plus que nbits pour être encodé en binaire
        @exception TypeError : si la liste de code n'est pas une liste d'entier
        """
        if not isinstance(code_list, list):
            raise TypeError("parameters must be a list of integers")

        for code in code_list:
            self.write_code(code)

    def write_code(self, code):
        """
        Nourri le flux avec un code entier
        @param code: le code à encoder sur nbits
        @exception BitStreamErrorEncode : le code nécessite plus que nbits pour être encodé en binaire
        @exception TypeError : si le code n'est pas un entier
        """
        # Un code est un nombre entier
        if not isinstance(code, int):
            raise TypeError("code must be integer")

        # Un code est forcement positif
        if code < 0:
            raise BitStreamErrorEncode("Error, code can't be negative")

        # Le code ne doit pas dépasser la limite
        if code >= 2 ** self._nbits:
            raise BitStreamErrorEncode("Error, code %d can't be encoded on %d bits" % (code, self._nbits))

        # Les bits de poids faible sont ajouté en premier little-endian
        for i in range(0, self._nbits):
            self._stream.append(bool((code >> i) & 1))

    def read_code(self):
        """
        Lit un code dans le flux et passe au suivant
        @return : un entier représentant le code encodé sur nbits
        """
        if len(self._stream) == 0:
            raise BitStreamErrorEOF()

        code = 0
        code_bits = self._stream[0:self._nbits]
        for k in range(0, self._nbits):
            code = (code << 1) | int(code_bits[(self._nbits - 1) - k])

        del self._stream[0:self._nbits]  # Supprime le code qui vient d'être lu
        return code

    def read_codes(self):
        """
        Lit le flux en entier et retourne la liste des codes.
        @exception BitStreamErrorEOF : le flux est vide
        @return : une liste d'entier représentant des codes encodés sur nbits
        """

        if len(self._stream) == 0:
            raise BitStreamErrorEOF()

        code_list = list()
        for i in range(0, len(self._stream), self._nbits):
            code = self.read_code()
            code_list.append(code)
        return code_list

    def size_in_code(self):
        """
        Calcule le nombre de codes contenus dans le flux
        @return: le nombre de codes
        """
        # Arrondi à l'inférieur du nombre de bits total, sur le nombre bit qui était encodé
        return floor(len(self._stream) / self._nbits)

    def flush(self):
        """
        Vide le flux
        """
        self._stream = list()

    def to_bytes(self):
        """
        Convertis le flux en un tampon d'octets (bytes) sans vider le flux.
        On rajoute un padding (assez de bits à 0) pour créer le dernier octet du tampon.
        @exception BitStreamErrorEOF : le flux est vide
        @return : un tampon de bytes (octets)
        """

        if len(self._stream) == 0:
            raise BitStreamErrorEOF()

        buffer = bytearray()

        streamcopy = copy(self._stream)

        if len(streamcopy) % 8 != 0:
            padding = 8 - len(streamcopy) % 8
            for i in range(0, padding):
                streamcopy.append(False)

        for i in range(0, len(streamcopy), 8):
            bits = streamcopy[i:i + 8]
            car = 0
            for k in range(0, 8):
                car = (car << 1) | int(bits[7 - k])
            buffer.append(car)
        return bytes(buffer)

    def from_bytes(self, buffer):
        """
        Rempli le flux de bits grâce au tampon passé en paramètre.
        Le flux de bits est vidé avant l'opération.
        Les derniers bits qui servent de padding sont supprimés
        @param buffer : le tampon à convertir en flux de bits
        """
        self.flush()  # Vide le buffer
        for code in buffer:
            for i in range(0, 8):
                self._stream.append(bool((code >> i) & 1))
        # On prend la taille totale, on regarde combien de code (complet) on peut encoder
        # On multiplie ce nombre de code par le nombre de bits utilisé pour encoder un code
        size = floor(len(self._stream) / self._nbits) * self._nbits
        # Suppression des bits inutiles
        self._stream = self._stream[0:size]
