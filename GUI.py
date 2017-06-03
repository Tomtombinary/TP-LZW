#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
from LZW import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class MainWindow(Frame):
    """
    Fenetre principale hérite de la classe Frame
    """

    def __init__(self, fenetre, **kwargs):
        """
        Constructeur de la fenêtre, créer les boutons pour choisir, compresser,
        décompresser un fichier

        @param fenetre: la fenêtre parent
        @param kwargs: les arguments a passé en plus au constructeur de la classe Frame
        """
        Frame.__init__(self, fenetre, width=800, height=600, **kwargs)
        self.pack(fill=BOTH)

        self._button_source = Button(self, text="Choisir un fichier", command=self.select_source)
        self._button_source.pack(fill=X)

        self._label_source = Label(self, text="Chemin source")
        self._label_source.pack(fill=X)

        self._button_compresser = Button(self, text="Compresser", command=self.action_compresser)
        self._button_compresser.pack(fill=X)

        self._button_decompresser = Button(self, text="Decompresser", command=self.action_decompresser)
        self._button_decompresser.pack(fill=X)

    def select_source(self):
        """
        Action effectuée lorsque l'utilisateur clique sur le bouton "Choisir un fichier"
        Une fenêtre permet de choisir le fichier à compresser/décompresser
        Le label se met à jour en fonction du choix de l'utilisateur
        """
        self._filename_src = filedialog.askopenfilename()
        if os.path.isfile(self._filename_src):
            self._label_source['text'] = self._filename_src
        else:
            self._label_source['text'] = "Chemin source"

    def action_compresser(self):
        """
        Action effectuée lorsque l'utilisateur clique sur le bouton "Compresser"
        Une fenêtre permet de nommer le fichier à sauvegarder.
        Ensuite le fichier choisi devient le fichier compressé, le label se met à jour en conséquence
        """
        self._filename_dest = filedialog.asksaveasfilename(defaultextension=".lzm",
                                                           filetypes=(('Archive LZW', '.lzw'),))
        if os.path.isfile(self._filename_src):
            if self._filename_dest != "":
                try:
                    with open(self._filename_src, 'rb') as source:
                        data = source.read()
                        compressed_data = compress(data)
                        with open(self._filename_dest, 'wb') as dest:
                            dest.write(compressed_data)
                        self._filename_src = self._filename_dest
                        self._label_source['text'] = self._filename_src
                        messagebox.showinfo("Info", "Compression réussie")
                except BufferError:
                    messagebox.showerror("Erreur", "Impossible de compresser le fichier")
                except:
                    messagebox.showerror("Erreur", "Cela n'aurait pas du se produire")
        else:
            messagebox.showerror("Erreur", "Merci de choisir le fichier à compresser/decompresser")

    def action_decompresser(self):
        """
        Action effectuée lorsque l'utilisateur clique sur le bouton "Décompresser"
        Une fenêtre permet de nommer le fichier à sauvergarder
        Ensuite le fichier choisi devient le fichier décompressé, le label se met à jour en conséquence
        """
        self._filename_dest = filedialog.asksaveasfilename()
        if os.path.isfile(self._filename_src):
            if self._filename_dest != "":
                try:
                    with open(self._filename_src, 'rb') as source:
                        data = source.read()
                        uncompressed_data = uncompress(data)
                        with open(self._filename_dest, 'wb') as dest:
                            dest.write(uncompressed_data)
                        self._filename_src = self._filename_dest
                        self._label_source['text'] = self._filename_src
                        messagebox.showinfo("Info", "Décompression réussie")
                except BufferError:
                    messagebox.showerror("Erreur", "Impossible de décompresser le fichier")
                except:
                    messagebox.showerror("Erreur", "Cela n'aurait pas du se produire")
        else:
            messagebox.showerror("Erreur", "Merci de choisir le fichier à compresser/decompresser")


if __name__ == '__main__':
    window = Tk()
    interface = MainWindow(window)
    interface.mainloop()
