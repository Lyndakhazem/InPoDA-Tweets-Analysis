import json # pour ecrire dans le fichier atterissage
import re # pour les expression regulieres 
from textblob import TextBlob #pour analyser les sentiments 

# une constante qui va nous servire pour faire l'identification du topic 
# il s'agit d'un dictionnaire python 
topics_dict ={"Intelligence Artificielle": ["intelligence", "artificial", "machine", "learning", "AI"],
    "Science et Recherche": ["science", "research", "discovery", "technology", "innovation"],
    "Politique et Gouvernement": ["politics", "government", "election", "policy", "democracy"],
    "Musique": ["music", "song", "artist", "concert", "album"],
    "Voyages et Aventures": ["travel", "destination", "adventure", "explore", "vacation"],
    "Santé et Bien-être": ["health", "wellness", "fitness", "nutrition", "medicine"],
    "Affaires et Finance": ["business", "finance", "economy", "entrepreneurship", "startup"],
    "Sports et Compétition": ["sports", "game", "athlete", "competition", "fitness"]
}
# la classe tweet

class Tweet:

    def __init__(self,tw):
        ''' le constructeur de la classe Tweet'''
        self.__text=tw["TweetText"]
        self.__text_net=self.nettoie_text()

    #les methodes :
    def nettoie_text(self):
        # supprimer tous les caracteres speciaux de text en utulisant une expression
        #.. reguliere 
        return re.sub(r'[^A-Za-z0-9\s]', '', self.__text) 
    
    def hashtags(self):
        # extraire du text tous les mots qui commence par # , 
        #.. cad extraire tous les hashtags du tweet avec une expression reguliere 
        # et retourne la liste des hashtags 
        return re.findall(r'#\w+', self.__text)
    
    def auteur(self):
        # Si le tweet commence par "RT @"
        if self.__text.startswith("RT @"): 
            aut = re.search(r'RT @([^\s:]+)', self.__text)# chercher le nom d'auteur a l'aide d'une expression reguliere
        else:
            #sinon si il s'agit pas d'un retweet 
            # alors on extrait la premiere mention qui commence avec @
            aut = re.search(r'@([^\s:]+)', self.__text)
        # retourner l'auteur si il existe sinon on retourne None
        if aut :
            return aut.group(1)
        else :
            return None
    
    def mentions(self):
        #extraire les mentions dans le texte de tweet avec une expression reguliere
        # returne la liste des mentions 
        l=re.findall(r'@\w+', self.__text)
        if len(l)>=1:
            return l[1:]
        else:
            return []

    
    def sentiment(self):
        # analyse de sentiment de tweet avec textBlob 
        
        sent=TextBlob(self.__text_net).sentiment
         # <0 si il negative , ==0 il est neutre , >0 il est positif 
        if sent [0]> 0:
            sentiment = "positif"
        elif sent [0]< 0:
            sentiment = "negatif"
        else:
            sentiment = "neutre"

        # retourne le sentiment de tweet , soit il est positif ou negatif
        return sentiment
    
    def topics(self):
        topics = []# Initialiser une liste vide pour stocker les topics détectés
        # Parcourir le dictionnaire de topics
        for key, topic in topics_dict.items():
            # si le topic est contenue dans le tweet et ses hashtags 
            # alors on le rajoute a la liste des topics detectes 
            if (key in self.__text_net.lower()):
                topics.append(key)
            else:
                for m in topic:
                    if m in self.__text_net.lower():
                        topics.append(key)
                        break
        # on retourne la liste des topics 
        return topics
    
    def sauvegarder_dans_la_zone_atterissage(self, fich):
        # Sauvegarder le tweet nettoyé dans le fichier JSON de la zone d'atterrissage
        # on ouvre la zone d'atterissage on mode "a" pour rajouter cela a la fin de fichier ..
        #.. sans ecraser son contenue 
        #with open(fich,'a') as landing_file:
            # on cree un dictionnaire tweet
        tweet = {
                "text_brut":self.__text,
                "text_net":self.nettoie_text(),
                "auteur":self.auteur(),
                "hashtags": self.hashtags(),
                "mentions": self.mentions(),
                "sentiment": self.sentiment(),
                "topics": self.topics() 
            }
            # on ecrit a la fin du fichier d'atterissage en format json 
        en_format_json = json.dumps(tweet, ensure_ascii=False)
        fich.write(en_format_json + '\n')
    