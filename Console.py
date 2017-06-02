#!/usr/bin/python3
# -*- coding:utf-8 -*-

from LZW import *
import argparse
import os

def main():

    parser = argparse.ArgumentParser(description='Compresse ou décompresse un fichier')
    parser.add_argument('filename',help='Fichier à compresser',type=str)
    parser.add_argument('-e','--encode',help="Nombre de bits pour encoder les codes (12 bits par défaut)",default=12,type=int)
    parser.add_argument('-o','--output',help="Fichier de sortie",type=str)
    parser.add_argument('-d','--decompress',help="Décompresse le fichier",action='store_true')
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print("Le fichier n'existe pas")

    output_filename = args.output
    if output_filename == None:
        if not args.decompress:
            output_filename = args.filename + ".lzm"
        else:
            output_filename = args.filename + ".ulzm"

    stream = BitStream(args.encode)

    if not args.decompress:
        with open(args.filename,'rb') as source:
            data = source.read()
            cdata = compress(data,encoder=stream)
            print("Fichier compressé à %d %%" % (100 * (1 - len(cdata) / len(data))))
            with open(output_filename,'wb') as dest:
                dest.write(cdata)
    else:
        with open(args.filename,'rb') as source:
            data = source.read()
            try:
                udata = uncompress(data,decoder=stream)
                with open(output_filename,'wb') as dest:
                    dest.write(udata)
            except BufferError:
                print("Le fichier compressé est corrompu")


if __name__ == '__main__':
    main()