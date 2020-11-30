# -*- coding: utf-8 -*-
import tkinter as tk
import os.path
from tkinter import messagebox
from tkinter import filedialog

liste_artistes = ""
liste_musees = ""
FILETYPES = [ ("text files", "*.txt") ]
listpath="liste_association.txt"

fenetre = tk.Tk()

class Partenaire: # Classe mère 
    def __init__(self):
        self.ID = "ID00"
        self.preference = []

    def extrairePref(self):
        self.preferences =(self.preferences).strip().split(" ")
        
    @staticmethod
    def autoExtractFromCSV(chemin_fichier): #méthode statique permettant de lire les fichiers CSV
        file = open(chemin_fichier)
        lines = file.readlines()
        return lines

class Artiste(Partenaire): # Classe fille de Partenaire
    
    __listeArtiste = [] # variable statique privée pour plus de sécurité
    # le seul moyen d'accéder à listeArtiste est de passer par les méthodes définies (getListeArtiste et autoExtractFromCSV)
    
    def __init__(self):
        Partenaire.__init__(self)
        self.ID = "ART00"
        self.nom = "nomartiste"
        self.prenom = "prenomartiste"
        
    @staticmethod    
    def getListeArtiste(): # accesseur
        return Artiste.__listeArtiste
        
    @staticmethod
    def autoExtractFromCSV(chemin_fichier): #méthode statique redéfinie pour Artiste
        lines = Partenaire.autoExtractFromCSV(chemin_fichier)
        donnees=[]
        compteur=0
        for line in lines:
            donnees=[line.strip().split(",")]
            Artiste.__listeArtiste.append(Artiste())
            Artiste.__listeArtiste[compteur].ID = donnees[0][0]
            Artiste.__listeArtiste[compteur].nom = donnees[0][1]
            Artiste.__listeArtiste[compteur].prenom = donnees[0][2]
            Artiste.__listeArtiste[compteur].preferences = donnees[0][3]
            Artiste.__listeArtiste[compteur].extrairePref()
            compteur+=1
        del Artiste.__listeArtiste[0]        

class Musee(Partenaire): # Classe fille de partenaire, soeur d'Artiste
    
    __listeMusee = [] # accès privé
    
    def __init__(self):
        Partenaire.__init__(self)
        self.ID = "MUS00"
        self.nom = "musee"
        self.ville = "ville"
               
    @staticmethod    
    def getListeMusee(): # accesseur
        return Musee.__listeMusee
    
    @staticmethod
    def autoExtractFromCSV(chemin_fichier): # méthode statique redéfinie pour Musee
        lines = Partenaire.autoExtractFromCSV(chemin_fichier)    
        donnees=[]
        compteur=0
        for line in lines:
            donnees=[line.strip().split(",")]
            Musee.__listeMusee.append(Musee())
            Musee.__listeMusee[compteur].ID = donnees[0][0]
            Musee.__listeMusee[compteur].nom = donnees[0][1]
            Musee.__listeMusee[compteur].ville = donnees[0][2]
            Musee.__listeMusee[compteur].preferences = donnees[0][3]
            Musee.__listeMusee[compteur].extrairePref()
            compteur+=1
        del Musee.__listeMusee[0]



def algo_affectation(liste_art, liste_mus):
    
    # au début de l'algorithme, tous les artistes et musées sont non assignés    
    liste_artiste_free = list(liste_art) # on initialise la liste d'artistes non assigné 
    liste_mus_free = list(liste_mus) # on initialise la liste de musées non assignés
    liste_s = [] # on initialise à vide la liste des fiancailles
        
    i=0
    
    # ----------- Vérifications -----------
    
     #si un artiste est dans la base de données mais n'est référencé par aucun musée
    liste_artiste_cleaned = list(liste_artiste_free)  
    for m in range(0, len(liste_artiste_free)):
        flag=0
        for n in range(0, len(liste_mus_free)):
            if (liste_artiste_free[m].ID not in liste_mus_free[n].preferences):
                flag=flag+1
        if (flag == len(liste_mus_free)):
            liste_artiste_cleaned.remove(liste_artiste_free[m])       
    
    liste_artiste_free = liste_artiste_cleaned
    
    #si un musée est dans la base de données mais n'est référencé par aucun artiste
    liste_mus_cleaned = list(liste_mus_free)  
    for m in range(0, len(liste_mus_free)):
        flag=0
        for n in range(0, len(liste_artiste_free)):
            if (liste_mus_free[m].ID not in liste_artiste_free[n].preferences):
                flag=flag+1
        if (flag == len(liste_artiste_free)):
            liste_mus_cleaned.remove(liste_mus_free[m])       
    
    liste_mus_free = liste_mus_cleaned
    
    
    
    
    #vérifie que toutes les préférences sont entrées
    liste_id_a = []
    for n in range(0, len(liste_artiste_free)):
        liste_id_a.append(liste_artiste_free[n].ID)
        
    liste_id_m = []
    for n in range(0, len(liste_mus_free)):
        liste_id_m.append(liste_mus_free[n].ID)
            
    #  les sets permettent de comparer de manière plus aisée
    set_id_a=set(liste_id_a)
    set_id_m=set(liste_id_m) 
        
    flag = 0
    for n in range(0, len(liste_mus_free)):
        if ((len(set_id_a - set(liste_mus_free[n].preferences)) != 0) or (len(liste_mus_free[n].preferences) != len(set_id_a))):
                flag = 1
                if (flag == 1):
                    message="Le musée " + liste_mus_free[n].ID + " n'a pas bien rempli ses préférences."
                    retry(message)
                    GetMusees()
                    
    flag = 0
    for n in range(0, len(liste_artiste_free)):
        if ((len(set_id_m - set(liste_artiste_free[n].preferences)) != 0) or (len(liste_artiste_free[n].preferences) != len(set_id_m))):
                flag = 1
                if (flag == 1):
                    message="L'artiste "+ liste_artiste_free[n].ID + " n'a pas bien rempli ses préférences."
                    retry(message)
                    GetArtistes()
            
        
    while (len(liste_artiste_free) > 0): # tant qu'il reste un artiste non assigné, on fait une boucle
        
        if(len(liste_artiste_free[i].preferences) == 0):
            break #si l'artiste a demandé à tous ses choix (0 préférence restante), on sort de la boucle (possibilité d'avoir un artiste sans musée)
        
        
              
        musee_pref = liste_artiste_free[i].preferences[0] #id de la première préference
        musee_object = next((x for x in liste_mus if x.ID == musee_pref), None) #permet de récupérer l'objet à partir de l'id
        
        if (musee_object in liste_mus_free): #si le musée est libre
            # on crée le couple (artiste, musee) dans la liste_s et on met à jour les autres listes
            liste_s.append([liste_artiste_free[i], musee_object]) 
            liste_mus_free.remove(musee_object)
            liste_artiste_free[i].preferences.remove(liste_artiste_free[i].preferences[0]) # la préférence a été examinée, on peut l'enlever
            liste_artiste_free.remove(liste_artiste_free[i])
            if(i >= len(liste_artiste_free)):
                i = 0

            
        else: # si musée déjà pris
            for j in range(0, len(liste_s)):
            #on parcourt la liste_s pour trouver le conjoint actuel de musee_object
                if (liste_s[j][1] == musee_object): #on a trouvé le couple  
                    temp = liste_s[j][0] #conjoint actuel de musee_object
                    
                    flag = 0
                    
                    try:
                        var_index_temp = musee_object.preferences.index(temp.ID)
                    except ValueError:
                        #print("List does not contain value")
                        flag = 1
                        
                    
                    try:
                        var_index_current = musee_object.preferences.index(liste_artiste_free[i].ID) #index de l'artiste[i] dans les préférences du musée
                    except ValueError:
                        #print("List does not contain value")
                        flag = 1
                        
                    if(flag == 0):    
                        liste_artiste_free[i].preferences.remove(liste_artiste_free[i].preferences[0])
                        #quoiqu'il en soit le musée a été examiné, on peut actualiser la liste de préférences.
                        
                        if (var_index_temp > var_index_current): 
                            #si l'index de temp est supérieur, cela signifie qu'il était moins bien classé et du coup on échange 
                            #artiste[i] devient le nouveau conjoint de musée et temp redevient free
                            liste_s[j][0] = liste_artiste_free[i]
                            liste_artiste_free.append(temp)
                            liste_artiste_free.remove(liste_artiste_free[i])
                            
                            if(i >= len(liste_artiste_free)):
                                i = 0
                            
                        else:
                            if (i < len(liste_artiste_free)-1):
                                i = i+1
                            else:
                                i = 0
                            

                
    return liste_s # on retourne notre liste de mariages stables 



def ecrire_fichier(liste_couple):
    asso = open(listpath,'w')
    quitter()
    for i in range(0, len(liste_couple)):
        asso.write(liste_couple[i][0].prenom + " " + liste_couple[i][0].nom + " - " + liste_couple[i][1].nom + "\n")
    asso.close()

def affectation(path_artiste,path_musee):
    Artiste.autoExtractFromCSV(path_artiste)
    Musee.autoExtractFromCSV(path_musee)
    liste_couple = algo_affectation(Artiste.getListeArtiste(),Musee.getListeMusee())
    ecrire_fichier(liste_couple)

def quitter():
    messagebox.showwarning("Terminé !", "La procédure est terminée, cliquez sur ok pour fermer le programme.")
    fenetre.quit()

def retry(message):
    messagebox.askretrycancel("Erreur", "La liste fournie n'est pas correcte\nMessage d'erreur :"+message+"\nChoisissez Retry pour rentrer une nouvelle liste")

def GetDir():
    global listpath
    listpath = filedialog.asksaveasfilename(filetypes=FILETYPES,defaultextension=".txt")

def GetArtistes():
    global liste_artistes
    liste_artistes = filedialog.askopenfilename(filetypes=FILETYPES)
    
def GetMusees():
    global liste_musees
    liste_musees = filedialog.askopenfilename(filetypes=FILETYPES)
    
def Launcher():
    if os.path.exists(liste_artistes) == True and os.path.exists(liste_musees) == True:
        affectation(liste_artistes,liste_musees)
    elif os.path.exists(liste_artistes) == False and os.path.exists(liste_musees) == False:
        messagebox.showerror("Erreur", "RENTRE DES LISTES CRETIN")
    elif os.path.exists(liste_artistes) == False:
        messagebox.showerror("Erreur artiste", "Il n'y a pas de liste d'artistes")
    elif os.path.exists(liste_musees) == False:
        messagebox.showerror("Erreur artiste", "Il n'y a pas de liste de musées")

welcome_label = tk.Label(fenetre, text="    Bienvenue dans le programme d'association artistes-musées    ")
bouton_getart = tk.Button(fenetre, text="Récupérer la liste d'artistes", command=GetArtistes)
bouton_getmus = tk.Button(fenetre, text="Récupérer la liste de musées", command=GetMusees)
bouton_getdir = tk.Button(fenetre, text="Sauver la liste comme...", command=GetDir)
bouton_lauchprog = tk.Button(fenetre, text="Lancer la procédure", command=Launcher)

def fenetreaffichee():
    fenetre.title("Programme d'association artistes-musées")
    welcome_label.pack() 
    bouton_getart.pack()
    bouton_getmus.pack()
    bouton_getdir.pack()
    bouton_lauchprog.pack()
    fenetre.mainloop()
    fenetre.destroy()

def main():
    fenetreaffichee()

main()