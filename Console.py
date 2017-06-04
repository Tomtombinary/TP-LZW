#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
Outil en ligne de commande pour compresser/decompresser un fichier
en utilisant l'algorithme LZW.
@author: Thomas Dubier
@author: Pol Kramarenko
@version: 1.0.0
"""
from LZW import *
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Compresse ou décompresse un fichier')
    parser.add_argument('filename', help='Fichier à compresser', type=str)
    parser.add_argument('-o', '--output', help="Fichier de sortie", type=str)
    parser.add_argument('-d', '--decompress', help="Décompresse le fichier", action='store_true')
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print("Le fichier n'existe pas")

    output_filename = args.output
    if output_filename is None:
        if not args.decompress:
            output_filename = args.filename + ".lzm"
        else:
            output_filename = args.filename + ".ulzm"

    if not args.decompress:
        with open(args.filename, 'rb') as source:
            data = source.read()
            cdata = compress(data)
            print("Fichier compressé à %d %%" % (100 * (1 - len(cdata) / len(data))))
            with open(output_filename, 'wb') as dest:
                dest.write(cdata)
    else:
        with open(args.filename, 'rb') as source:
            data = source.read()
            try:
                udata = uncompress(data)
                with open(output_filename, 'wb') as dest:
                    dest.write(udata)
            except BufferError:
                print("Le fichier compressé est corrompu")


if __name__ == '__main__':
    main()
