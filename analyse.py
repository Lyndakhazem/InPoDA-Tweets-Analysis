import pandas as pd 
def top_k_hashtags(k,data):
    '''extraire les top k hastaghs dans nos tweets '''
    serie = data['hashtags'].apply(pd.Series,dtype='object').stack()#transforme la colonne hashtags en une serie pandas
    hashtags = serie.value_counts() # calcule le nombre d'ocuurence de chaque hashtags 
    top_k_hashtags=hashtags.head(k) # on selectionne que les k top premiers hashtags 
    # on return la liste des top k hashtags trier par ordre decroissant
    return (top_k_hashtags.index).to_list()# rendre le resultat comme une liste python

def top_k_utilisateurs(k,data):
    top_k_aut=data["auteur"].value_counts().head(k)# calcule le nombre d'ocuurence de chaque auteur 
    # on prend que les 5 premiere de la serie par ordre decroissant
    return (top_k_aut.index).to_list()# rendre le resultat comme une liste python

def top_k_utilisateurs_mentionnes(k, data):
    serie = data['mentions'].apply(pd.Series, dtype='object').stack()  # Transforme la colonne mentions en une serie pandas
    utilisateurs_mentionnes = serie.value_counts()# Calcule le nombre d'occurrences de chaque utilisateur mentionne
    top_k_utilisateurs_mentionnes=utilisateurs_mentionnes.head(k)  
    # On retourne la nouvelle série avec les K top utilisateurs mentionnes trier par ordre decroissant
    return (top_k_utilisateurs_mentionnes.index).to_list()# rendre le resultat comme une liste python

def top_k_topics(k,data):
    serie = data['topics'].apply(pd.Series, dtype='object').stack()  # Transforme la colonne topics en une serie pandas
    topics = serie.value_counts()# Calcule le nombre d'occurrences de chaque topics 
    top_k_topics=topics.head(k)  # on prend que les k 
    # On retourne la nouvelle série avec les K top utilisateurs mentionnes trier par ordre decroissant
    return (top_k_topics.index).to_list()# rendre le resultat comme une liste python


def nombre_de_publications_par_utilisateur(data):
    publications_par_utilisateur = data["auteur"].value_counts()# Calcule le nombre d'occurrence de chaque auteur , cad le nombre de publication de chaque utilisateur
    # On retourne la nouvelle série avec les nombre de publication par utilisateur  trier par ordre decroissant
    return publications_par_utilisateur

def nombre_de_publications_par_hashtags(data):
    serie = data['hashtags'].apply(pd.Series, dtype='object').stack()  # Transforme la colonne "hashtag" en une serie pandas
    hashtags_par_publication = serie.value_counts()# Calcule le nombre de publications par chaque auteur , 
    #...cad le nombre de publication de chaque hashtags 
    # On retourne la nouvelle série avec les nombre de publication par hashtags  trier par ordre decroissant
    return hashtags_par_publication


def  nombre_de_publications_par_topic(data):
    serie = data['topics'].apply(pd.Series, dtype='object').stack()  # Transforme la colonne "topic" en une serie pandas
    topic_par_publication = serie.value_counts()# Calcule le nombre de publications par chaque topic , 
    #...cad le nombre de publication pour chaque topic
    # On retourne la nouvelle série avec les nombre de publication par topic  trier par ordre decroissant
    return topic_par_publication

def ensemble_de_tweets_d_un_utilisateur_specifique(data,utilisateur):
    # on retourne la liste de tous les textes publier par l'utilisateur en paramatre 
    # on selection que les texte ou la colonne "auteur" est egale a l'utilisateur 
    return data[data["auteur"]==utilisateur]["text_brut"].to_list()

def ensemble_de_tweets_mentionnant_un_utilisateur_specifique(data,utilisateur):
    l=[]# initialisation d'une liste vide 
    for i,ment in enumerate(data["mentions"]):# i prend l'index de la ligne , ment la liste des mentions de chaque tweet
        if utilisateur in ment and not(data.iloc[i]["text_brut"] in l):# si l'utilisateur est dans la liste des mentions 
            l.append(data.iloc[i]["text_brut"])# alors on rajoute le text de tweet a notre liste
    # on retourne la liste de tous les textes ou l'utilisateur passee en paramatre est mentionee
    return l 
def Les_utilisateurs_mentionnant_un_hashtag_specifique(data,h):
    l=[]# initialisation d'une liste vide 
    # i prend l'index de la ligne , hasht la liste des hashtags de chaque tweets
    for i,hasht in enumerate(data["hashtags"]):
        if h in hasht:# si le hashtags est dans la liste des hashtags 
            # alors on rajoute l'auteur de tweet a notre liste
            #si l'auteur il existe pas deja dans notre liste(pour eviter la repitions des auteurs pour un meme hashtags)
            if not (data.iloc[i]["auteur"]) in l :
                l.append(data.iloc[i]["auteur"])
    # on retourne la liste de tous lesauteur qui mentionee un hashtags specifique
    return l 
def  Les_utilisateurs_mentionnes_par_un_utilisateur_specifique(data,utilisateur):
    # on retourne la liste des utilisateurs mentionnee par un utilisateur specifique
    l=[]
    for i,aut in enumerate(data["auteur"]):
        if (aut==utilisateur) and not(data.iloc[i]["mentions"]==[]) and not(data.iloc[i]["mentions"] in l):
            l.append(data.iloc[i]["mentions"])#copier la liste des mentions dans notre liste 
    return sum(l,[])#pour rendre la liste unique 

