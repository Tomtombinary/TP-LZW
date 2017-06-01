#!/usr/bin/python3
#-*- coding:utf-8 -*-

from math import *
from copy import *

class BitStreamException(Exception):
    def __init__(self,message):
        super(BitStreamException,self).__init__(message)

class BitStream:
    def __init__(self,nbits):
        self._nbits = nbits
        self._stream = list()

    def write_codes(self,code_list):
        for code in code_list:
            self.write_code(code)

    def write_code(self,code):
        if code >= 2 ** self._nbits:
            raise BitStreamException("Error, code %d can't be encoded on %d bits" % (code, self._nbits))

        for i in range(0, self._nbits):
            self._stream.append(bool((code >> i) & 1))

    def read_code(self):
        if len(self._stream) == 0:
            raise BitStreamException("Error, stream end")

        code = 0
        code_bits = self._stream[0:self._nbits]
        for k in range(0,self._nbits):
            code = (code << 1) | int(code_bits[(self._nbits - 1) - k])

        del self._stream[0:self._nbits]
        return code

    def read_codes(self):
        code_list = list()
        for i in range(0,len(self._stream),self._nbits):
            code = self.read_code()
            code_list.append(code)
        return code_list

    def size_in_code(self):
        return floor(len(self._stream) / self._nbits)

    def flush(self):
        self._stream = list()

    def to_bytes(self):
        buffer = bytearray()

        streamcopy = copy(self._stream)

        if len(streamcopy) % 8 != 0:
            padding = 8 - len(streamcopy) % 8
            for i in range(0,padding):
                streamcopy.append(False)

        for i in range(0, len(streamcopy), 8):
            bits = streamcopy[i:i+8]
            car = 0
            for k in range(0,8):
                car = (car << 1) | int(bits[7 - k])
            buffer.append(car)
        return bytes(buffer)


    def from_bytes(self,buffer):
        self.flush()
        for code in buffer:
            for i in range(0,8):
                self._stream.append(bool((code >> i) & 1))
        # Suppression des bits inutiles
        size = floor(len(self._stream)/self._nbits) * self._nbits
        self._stream = self._stream[0:size]

