from tkinter import *
from random import randint
import csv


class Counter:
    object = 0

    def __init__(self):
        Counter.object += 1

    def clean(self):
        Counter.object = 0


def centrefenetre(fen):
    fen.update_idletasks()

    geo = fen.geometry()

    x = geo.find('x', 0)
    tx = geo[0:x]       # taille horizontale

    y = geo.find('+', x+1)
    ty = geo[x+1:y]     # taille verticale

    xecran = fen.winfo_screenwidth()
    yecran = fen.winfo_screenheight()

    x0 = (xecran-int(tx))//2
    y0 = (yecran-int(ty))//2

    fen.geometry("+" + str(x0) + "+" + str(y0))


def csvcount(filename):
    with open(filename, 'r') as f:
        i = 0
        for ligne in f:
            i += 1
    return i


class mere(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.root = parent
        self.list = Listbox(self.root, width=70)
        self.list.pack(side='left', padx=5, pady=5)

        Counter.clean(self)

        self.high_score = 0

        try:
            with open('high_score.txt', 'r', newline='') as file:
                self.high_score = file.read()
        except:
            self.high_score = 0

        try:
            with open('question.csv', 'r', newline='') as file:
                lecteur = csv.reader(file, delimiter=';')
                for row in lecteur:

                    self.list_tuple = self.list.get(0, END)
                    self.list_str = " ".join(self.list_tuple)
                    self.list_list = self.list_str.split(" ")

                    deja_vu = 0
                    for i in self.list_list:
                        if i == row[0]:
                            deja_vu += 1

                    if deja_vu == 0:
                        self.list.insert(END, row[0])
        except FileNotFoundError:
            with open('question.csv', 'x') as file:
                pass

        self.label_high_score = Label(
            self.root, text="meilleur record = {}".format(self.high_score))
        self.label_high_score.config(font=("Arial", 32))
        self.label_high_score.pack(side=RIGHT, padx=5, pady=5)

        self.question = Button(
            self.root, text='créer une question', command=self.question_command)
        self.question.config(font=("Arial", 32), bd=5,
                             overrelief="sunken", activebackground="grey")
        self.question.pack(fill=X, padx=5, pady=5)

        self.jouer = Button(self.root, text='jouer',
                            command=self.jouer_command)
        self.jouer.config(font=("Arial", 32), bd=5,
                          overrelief="sunken", activebackground="grey")
        self.jouer.pack(fill=X, padx=5, pady=5)

        self.quitter = Button(self.root, text='quitter',
                              command=self.root.destroy)
        self.quitter.config(font=("Arial", 32), bg="red",
                            bd=5, overrelief="sunken", activebackground="grey")
        self.quitter.pack(side=BOTTOM, padx=5, pady=5)

    def question_command(self):

        self.root.destroy()

        fenetre2 = Tk()
        fenetre2.title("Programme JuMo")
        fenetre2.geometry("1250x750")

        bg = PhotoImage(file='bg.png')
        background_label = Label(image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        centrefenetre(fenetre2)

        filleQuestion(fenetre2).pack()
        fenetre2.mainloop()

    def jouer_command(self):

        self.matiere_selectionnee = self.list.get(ACTIVE)
        with open('matiere.txt', 'w+', newline='') as mon_fichier:
            mon_fichier.write(self.matiere_selectionnee)

        self.root.destroy()

        fenetre3 = Tk()
        fenetre3.title("Programme JuMo")
        fenetre3.geometry("750x750")

        bg = PhotoImage(file='bg.png')
        background_label = Label(image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        centrefenetre(fenetre3)

        filleJouer(fenetre3).pack()
        fenetre3.mainloop()


class filleQuestion(mere, Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.root = parent
        self.ma_question = StringVar()
        self.ma_reponse = StringVar()
        self.ma_matiere = StringVar()

        self.label_question = Label(
            self.root, text='choisissez votre matière', fg='black')
        self.label_question.config(font=("Arial", 32))
        self.label_question.pack(padx=5, pady=5)

        self.matiere = Entry(self.root, textvariable=self.ma_matiere)
        self.matiere.config(font=("Arial", 32))
        self.matiere.pack(padx=5, pady=5)

        self.label_question = Label(
            self.root, text='choisissez une question', fg='black')
        self.label_question.config(font=("Arial", 32))
        self.label_question.pack(padx=5, pady=5)

        self.aff_question = Entry(
            self.root, textvariable=self.ma_question, fg='red')
        self.aff_question.config(font=("Arial", 32))
        self.aff_question.pack(padx=5, pady=5)

        self.choix_reponse_txt = Label(
            self.root, text='indiquez en la réponse', fg='black')
        self.choix_reponse_txt.config(font=("Arial", 32))
        self.choix_reponse_txt.pack(padx=5, pady=5)

        self.aff_reponse = Entry(
            self.root, textvariable=self.ma_reponse, fg='red')
        self.aff_reponse.config(font=("Arial", 32))
        self.aff_reponse.pack(padx=5, pady=5)

        self.valider_question = Button(
            self.root, text='valider', activebackground='red', command=self.ecrire)
        self.valider_question.config(
            font=("Arial", 32), bd=5, overrelief="sunken", activebackground="grey")
        self.valider_question.pack(padx=5, pady=5)

        self.quitter = Button(self.root, text='quitter', command=self.quit)
        self.quitter.config(font=("Arial", 32), bg="red",
                            bd=5, overrelief="sunken", activebackground="grey")
        self.quitter.pack(padx=5, pady=5, side=BOTTOM)

    def ecrire(self):

        with open('question.csv', 'a+', newline='') as mon_fichier:
            ecrire = csv.writer(mon_fichier, delimiter=";",
                                quoting=csv.QUOTE_NONE)
            ecrire.writerow(
                [self.ma_matiere.get(), self.ma_question.get(), self.ma_reponse.get()])

        self.refaire()

    def refaire(self):
        self.root.destroy()

        fenetre2 = Tk()
        fenetre2.title("Programme JuMo")
        fenetre2.geometry("1250x750")

        bg = PhotoImage(file='bg.png')
        background_label = Label(image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        centrefenetre(fenetre2)

        filleQuestion(fenetre2).pack()
        fenetre2.mainloop()

    def quit(self):
        self.root.destroy()

        root = Tk()
        root.title("Programme JuMo")
        root.geometry("1250x750")

        bg = PhotoImage(file='bg.png')
        background_label = Label(image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        centrefenetre(root)

        mere(root).pack()
        root.mainloop()


class filleJouer(mere, Frame):

    def __init__(self, parent, *args, **kwargs):

        Frame.__init__(self, parent)

        self.root = parent

        self.calcul()

    def calcul(self):

        with open('matiere.txt', 'r', newline='') as file:
            self.matiere_selectionnee = file.read()

        with open('question.csv', 'r') as f:
            i = 0
            lecteur = csv.reader(f, delimiter=';')
            for ligne in lecteur:
                if ligne[0] == self.matiere_selectionnee:
                    i += 1

        self.n_question = randint(0, i-1)

        with open('question.csv', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            row_count = 0
            for row in reader:
                if row[0] == self.matiere_selectionnee:
                    if row_count == self.n_question:
                        self.matiere = row[0]
                        self.question = row[1]
                        self.reponse = row[2]
                        row_count += 1
                    else:
                        row_count += 1
        self.reponse.lower()

        self.affiche()

    def affiche(self):

        # Affichage de la question
        self.label_jeu = Label(self.root, text=self.question, fg='black')
        self.label_jeu.config(font=("Arial", 32))
        self.label_jeu.pack(side=TOP, pady=10, padx=5)

        # demander la réponse
        self.reponse_a_verif = StringVar()
        self.reponse_demande = Entry(
            self.root, textvariable=self.reponse_a_verif, fg='red')
        self.reponse_demande.config(font=("Arial", 32))
        self.reponse_demande.pack(side=TOP, padx=5, pady=5)

        # vérification
        self.valider_reponse = Button(
            self.root, text='valider', activebackground='red', command=self.verif)
        self.valider_reponse.config(
            font=("Arial", 32), bd=5, overrelief="sunken", activebackground="grey")
        self.valider_reponse.pack(side=TOP, padx=5, pady=5)

        # affichage du Counter
        self.label_Counter = Label(
            self.root, text="victoires:{}".format(Counter.objet), fg='black')
        self.label_Counter.config(font=("Arial", 32))
        self.label_Counter.pack(side=TOP, padx=5, pady=100)

        self.quitter = Button(self.root, text='quitter', command=self.quit)
        self.quitter.config(font=("Arial", 32), bg="red",
                            bd=5, overrelief="sunken", activebackground="grey")
        self.quitter.pack(padx=5, pady=5, side=BOTTOM)

    def verif(self):
        resultat = Toplevel()
        # resultat.geometry('500x200+400+400')

        def fini(): return self.quitter_le_popup(resultat)

        cadre_txt = Frame(resultat)
        cadre_txt.pack(fill=BOTH, padx=10, pady=5)

        cadre = Frame(resultat)
        cadre.pack(fill=BOTH, padx=10, pady=5)

        if self.reponse_a_verif.get() == self.reponse:
            resultat.title('Tu as réussi!!!')

            a = Counter()

            resultat_txt = Label(
                cadre_txt, text='Bravo champion!', bg='#c93d3d', fg='#ffffff', relief='groove')
            resultat_txt.config(font=("Arial", 32))
            resultat_txt.pack(fill=BOTH, padx=5, pady=5)

            def pas_fini(): return self.continu(resultat)
            suivant = Button(cadre, text='continuer', activebackground='red',
                             bg='#3cb5e7', fg='#ffffff', command=pas_fini)
            suivant.config(font=("Arial", 20), bd=5,
                           overrelief="sunken", activebackground="grey")
            suivant.pack(padx=5, pady=5)

            quitter = Button(cadre, text='quitter',
                             bg='#3cb5e7', fg='#ffffff', command=fini)
            quitter.config(font=("Arial", 20), bg="red", bd=5,
                           overrelief="sunken", activebackground="grey")
            quitter.pack(side=BOTTOM, padx=5, pady=5)

        else:
            resultat.title('Tu es nul!')

            resultat_txt = Label(
                cadre_txt, text='réessayes encore', bg='#3cb5e7', fg='#ffffff', relief='groove')
            resultat_txt.config(font=("Arial", 32))
            resultat_txt.pack(fill=BOTH, padx=5, pady=5)

            def refaire(): return self.retry(resultat)
            reessayer = Button(resultat, text='réessayer', activebackground='red',
                               bg='#c93d3d', fg='#ffffff', command=refaire)
            reessayer.config(font=("Arial", 20), bd=5,
                             overrelief="sunken", activebackground="grey")
            reessayer.pack(padx=5, pady=5)

            quitter = Button(resultat, text='quitter',
                             bg='#c93d3d', fg='#ffffff', command=fini)
            quitter.config(font=("Arial", 20), bg="red", bd=5,
                           overrelief="sunken", activebackground="grey")
            quitter.pack(side=BOTTOM, padx=5, pady=5)

        resultat.mainloop()

    def continu(self, resultat):
        resultat.destroy()

        self.root.destroy()

        fenetre3 = Tk()
        fenetre3.title("Programme JuMo")
        fenetre3.geometry("750x750")

        bg = PhotoImage(file='bg.png')
        background_label = Label(image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        centrefenetre(fenetre3)

        filleJouer(fenetre3).pack()
        fenetre3.mainloop()

    def retry(self, resultat):
        resultat.destroy()

    def quitter_le_popup(self, resultat):

        try:
            with open('high_score.txt', 'r') as mon_fichier:
                ancien_record = mon_fichier.read()

            if Counter.objet >= int(ancien_record):
                with open('high_score.txt', 'w') as mon_fichier:
                    mon_fichier.write(str(Counter.objet))

        except FileNotFoundError:
            with open('high_score.txt', 'x') as mon_fichier:
                mon_fichier.write(str(Counter.objet))

        resultat.destroy()
        self.root.destroy()

        root = Tk()
        root.title("Programme JuMo")
        root.geometry("1250x750")

        bg = PhotoImage(file='bg.png')
        background_label = Label(image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        centrefenetre(root)

        mere(root).pack()
        root.mainloop()

    def quit(self):
        self.root.destroy()

        root = Tk()
        root.title("Programme JuMo")
        root.geometry("1250x750")

        bg = PhotoImage(file='bg.png')
        background_label = Label(image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        centrefenetre(root)

        mere(root).pack()
        root.mainloop()
