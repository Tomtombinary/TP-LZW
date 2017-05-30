#!/usr/bin/python3
# -*- coding:utf-8 -*-

from LZW import *
import argparse
import os

def main():

    parser = argparse.ArgumentParser(description='Compresse ou décompresse un fichier')
    parser.add_argument('filename',help='Fichier à compresser',type=str)
    parser.add_argument('-e','--encode',help="Nombre d'octets pour encoder les codes (2 minimum)",default=2,type=int)
    parser.add_argument('-o','--output',help="Fichier de sortie",type=str)
    parser.add_argument('-d','--decompress',help="Décompresse le fichier",action='store_true')
    args = parser.parse_args()

    if args.encode < 2:
        print("2 octets minimum pour encoder")
        exit(0)

    if not os.path.exists(args.filename):
        print("Le fichier n'existe pas")

    output_filename = args.output
    if output_filename == None:
        if not args.decompress:
            output_filename = args.filename + ".lzm"
        else:
            output_filename = args.filename + ".ulzm"

    if not args.decompress:
        with open(args.filename,'rb') as source:
            data = source.read()
            cdata = compresser(data,coding_size=args.encode)
            print("Fichier compressé à %d %%" % (100 * (1 - len(cdata) / len(data))))
            with open(output_filename,'wb') as dest:
                dest.write(cdata)
    else:
        with open(args.filename,'rb') as source:
            data = source.read()
            try:
                udata = decompresser(data,coding_size=args.encode)
                with open(output_filename,'wb') as dest:
                    dest.write(udata)
            except BufferError:
                print("Le fichier compressé est corrompu")


if __name__ == '__main__':
    main()