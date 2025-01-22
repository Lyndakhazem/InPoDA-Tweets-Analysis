#chargement des modules
import gradio as gr  # importer gradio pour implementer l'interface graphique
import pandas as pd
import analyse # importationb de notre module analyse , et toute ses fonctions 
import matplotlib.pyplot as plt
# importation de ses deux modules qui nous sert pour visualiser les plot
import io
import base64
# chargement du fichier atterissage dans un data frame python 
df = pd.read_json("zone_atterrissage.json", lines=True)
# Définir la fonction actuelle en fonction de l'option sélectionnée par l'utilisateur
def choisir_function(option, parametre):
    ''' nous sert a chosiir la fonction d'analyse de donnees a a partir du choix d'utilisateur'''
    if option is None or not isinstance(option, str):
        return "Veuillez sélectionner une option ."
    if option.startswith("Top K"):
        if parametre is None or not str(parametre).strip():
            return "Veuillez fournir un paramètre entier valide pour les options Top K."

        try:
            parametre = int(str(parametre))
        except ValueError:
            return "Veuillez fournir un paramètre entier valide pour les options Top K."

    if option == "Top K Hashtags":
        resultat = analyse.top_k_hashtags(parametre, df)
    elif option == "Top K Utilisateurs":
        resultat = analyse.top_k_utilisateurs(parametre, df)
    elif option == "Top K Topics":
        resultat = analyse.top_k_topics(parametre, df)
    elif option=="Top K Utilisateurs mentionne":
        resultat=analyse.top_k_utilisateurs_mentionnes(parametre,df)
    elif option == "Nombre de Publications par Utilisateur":
        resultat = analyse.nombre_de_publications_par_utilisateur(df)
        resultat = "<br>".join([f"{utilisateur}: {nombre}" for utilisateur, nombre in resultat.items()])
    elif option == "Nombre de Publications par hashtags":
        resultat = analyse.nombre_de_publications_par_hashtags(df)
        resultat = "<br>".join([f"{hashtags}: {nombre}" for hashtags, nombre in resultat.items()])

    elif option == "ensemble de tweets d'un utilisateur specifique":
        resultat = analyse.ensemble_de_tweets_d_un_utilisateur_specifique(df,str(parametre))
        resultat = "<br>".join([f"{i+1}: {text}" for i,text in enumerate(resultat)])
    elif option == "ensemble de tweets mentionnant un utilisateur specifique":
        resultat = analyse.ensemble_de_tweets_mentionnant_un_utilisateur_specifique(df,str(parametre))
        resultat = "<br>".join([f"{i+1}: {text}" for i,text in enumerate(resultat)])
    elif option == "Les utilisateurs mentionnant un hashtag specifique":
        resultat = analyse.Les_utilisateurs_mentionnant_un_hashtag_specifique(df,str(parametre))
        resultat = "<br>".join([f"{i+1}: {utilisateur}" for i,utilisateur in enumerate(resultat)])
    elif option == "Les utilisateurs mentionnes par un utilisateur specifique":
        resultat = analyse.Les_utilisateurs_mentionnes_par_un_utilisateur_specifique(df,str(parametre))
        resultat = "<br>".join([f"{i+1}: {mention}" for i,mention in enumerate(resultat)])

    elif option == "Nombre de Publications par Topic":
        plt.figure(figsize=(10, 14))
        analyse.nombre_de_publications_par_topic(df).plot.bar(
            title="nombre de publications par topic", rot=45, figsize=(10,14))

        # Convertir le graphique en image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.read()).decode()
        plt.close()
        
        # Renvoyer l'image dans une balise HTML
        # cela nous permmette d'afficher le resultat de plot sur gradio
        resultat = f"<img src='data:image/png;base64,{img_base64}' width='500' height='250'>"
    elif option == "Sentiments des Tweets":
        plt.figure(figsize=(8, 4))
        df["sentiment"].value_counts().plot.pie(title="Les sentiments des tweets", autopct="%1.1f%%")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.read()).decode()
        plt.close()
        resultat = f"<img src='data:image/png;base64,{img_base64}' width='600' height='600'>"

    # Si c'est un top, on format les resultats de l'affichage,
    # pour afficher les top ligne par ligne

    
    if option.startswith("Top"):
        resultat = "<br>".join([f"Top {i + 1} : {item}" for i, item in enumerate(resultat)])
    
    #parametre = None
    return resultat

# on cree l'interface graphique avec Gradio
# on va la mettre dans une fonction pour que on peut l'appeleer dans le module principale "main"

def lancement_InPoDA():
# Lancement de l'interface graphique 
    interface = gr.Interface(
        fn=choisir_function,
        inputs=[
        gr.Radio(choices=["Top K Hashtags", "Top K Utilisateurs", "Top K Topics","Top K Utilisateurs mentionne",
                          "Nombre de Publications par Utilisateur","Nombre de Publications par hashtags", "Nombre de Publications par Topic","ensemble de tweets d'un utilisateur specifique"
                          ,"ensemble de tweets mentionnant un utilisateur specifique",
                          "Les utilisateurs mentionnant un hashtag specifique",
                          "Les utilisateurs mentionnes par un utilisateur specifique","Sentiments des Tweets"]),
        gr.Textbox(placeholder="Entrez le paramètre", label="Paramètre (pour les options nécessitant un paramètre), on indique @ que pour les utilisateurs mentionné", type="text")
        ],
        outputs=gr.HTML(),
        live=True,
        title="InPoDa - Analyse de données des Tweets",
        description="Choisissez une option, entrez le paramètre (si nécessaire), et découvrez les résultats.",
    )
    interface.launch(inbrowser=True)
