import time
from chatgptModule1 import *
from wordpressModule1 import *
        
def creation_page_contenu(sujet, ville, type):
    texte = preparation_creation_article(sujet,ville)
    titre = launch_gpt("En tant qu'expert en référencement, créer un titre accrocheur donnant envie aux utilisateurs de cliquer pour l'article suivant portant sur le sujet "+ sujet +" et sur le ville de "+ ville +" . Tu ne dois pas spécifier la localisation de l'agence ni son nom dans le titre. Tu ne dois retourner que le contenu du titre et pas les symboles autour de celui-ci  : "+ texte +"")
    titre_verifie = launch_gpt("Tu peux retirer les guillemets et ces caractères « » dans ce texte : "+ titre +"")
    
    slug = launch_gpt("Créer un slug court et retourne uniquement le slug pour un article ayant ce titre : "+ titre_verifie +" "+ville)

    idPage = new_page(titre_verifie,texte,'publish',slug,type)
    
    response_json = idPage

    response_data = json.loads(response_json)

    return response_data['id']

def mise_a_jour_contenu(idPage : str, sujet, ville, type):
    texte = preparation_creation_article(sujet,ville)
    titre = launch_gpt("En tant qu'expert en référencement pour tu travaille pour une agence immobilière qui s'appelle 'La Galerie Immobiliere' mais tu ne dois pas spécifier la localisation de l'agence ni son nom dans le titre et l'article, tu dois créer un titre accrocheur donnant envie aux utilisateurs de cliquer sur l'article suivant portant sur le sujet "+ sujet +" et en lien avec la ville de "+ville+" . Tu ne dois retourner que le contenu du titre et pas les symboles autour de celui-ci : "+ texte +"")
    titre_verifie = launch_gpt("Tu peux retirer les guillemets et ces caractères « » dans ce texte : "+ titre +"")

    update_page(idPage,titre_verifie,texte, type)

def preparation_creation_article(sujet, ville):
    print("LESSUJETS")
    print(sujet)
    print(ville)
    sommaire = launch_gpt("En tant qu'expert en référencement, tu travaille pour une agence immobilière qui s'appelle 'La Galerie Immobiliere', qui souhaite améliorer son référencement sur les moteurs de recherche en rédigeant des articles compris entre 600 et 1000 mots. A la manière de Neil Pateil, tu dois rédiger le plan détaillé avec une introduction, le corps de l'article et une conclusion pour un article sur le sujet suivant "+sujet+" et sur le ville de "+ville+" en n'y mettant les points importants et sans mettre de sous partie. Tu ne dois pas spécifier en titre des sections, les parties concernant l'appel à l'action ou le corps de l'article")
    time.sleep(5)
    mots_cles = launch_gpt("En tant qu'expert en référencement, tu travaille pour une agence immobilière qui s'appelle 'La Galerie Immobiliere', qui souhaite améliorer son référencement sur les moteurs de recherche en rédigeant des articles compris entre 600 et 1000 mots. A la manière de Neil Pateil, tu dois trouver 15 mots clés à cibler dans l'article en lien avec le sujet "+sujet+" et sur le ville de "+ville+" pour le corps de l'article afin d'améliorer le référencement du site.")
    time.sleep(5)
    article = launch_gpt("En tant qu'expert en référencement, tu travaille pour une agence immobilière qui s'appelle 'La Galerie Immobiliere' mais tu ne dois pas spécifier la localisation de l'agence dans l'article et tu ne dois pas mettre le nom de l'agence dans l'article. Tu dois rédiger un article compris entre 600 et 1000 mots et en utilisant les mots clés suivants "+ mots_cles +". Tu dois utiliser le plan détaillé suivant : "+sommaire+" . L'article doit être en lien avec la ville de "+ville+" . Tu devras organiser, en HTML, le contenu en titre avec quelques titres mais il ne doit pas y avoir de sous partie dans chaque grande partie et en mettant des balises HTML de gras pour les points importants. Tu ne dois pas spécifier en titre des sections, les parties concernant l'appel à l'action ou le corps de l'article.")
    
    print("------------------")
    print(article)
    print("------------------")

    return article +" "


def creation_page_contenu_service(sujet):
    texte = preparation_creation_article_service(sujet)
    titre = launch_gpt("En tant qu'expert en référencement, créer un titre accrocheur court commençant par 'La Galerie Immobilière - ' suivi du sujet. La page porte sur le sujet "+sujet+" qui correspond à l'un des services de l'agence immobilière. Le titre doit permettre de promouvoir les services de l'agence immobilière 'La Galerie Immobilière'. Tu ne dois retourner que le contenu du titre et pas les symboles autour de celui-ci. Voici le contenu de l'article : "+texte+"")
    titre_verifie = launch_gpt("Tu peux retirer les guillemets et ces caractères « » dans ce texte : "+ titre +"")
    
    slug = launch_gpt("Tu peux me générer un slug court de quelques mots pour un article ayant ce titre :"+titre_verifie+"")

    idPage = new_page(titre_verifie,texte,'publish',slug,'')
    
    response_json = idPage

    response_data = json.loads(response_json)

    return response_data['id']

def mise_a_jour_contenu_service(idPage : str, sujet):
    texte = preparation_creation_article_service(sujet)
    titre = launch_gpt("En tant qu'expert en référencement, créer un titre accrocheur court commençant par 'La Galerie Immobilière - ' suivi du sujet. La page porte sur le sujet "+sujet+" qui correspond à l'un des services de l'agence immobilière. Le titre doit permettre de promouvoir les services de l'agence immobilière 'La Galerie Immobilière'. Tu ne dois retourner que le contenu du titre et pas les symboles autour de celui-ci. Voici le contenu de l'article : "+texte+"")
    titre_verifie = launch_gpt("Tu peux retirer les guillemets et ces caractères « » dans ce texte : "+ titre +"")

    update_page(str(idPage),titre_verifie,texte,'')

def preparation_creation_article_service(sujet):
    time.sleep(5)
    article = launch_gpt("En tant qu'expert en référencement, tu travaille pour une agence immobilière qui s'appelle 'La Galerie Immobiliere' qui souhaite promouvoir ses services sur les moteurs de recherche en rédigeant des articles compris entre 400 et 800 mots. Tu dois rédiger un article sur le sujet suivant "+sujet+" pour promouvoir ce service en n'y mettant les points importants. Tu dois donc parler de ce sujet en faisant la promotion de ce service chez 'La Galerie Immobilière'. Le titre de l'article ne doit pas être créer ni retourner. Tu devras organiser le contenu en titre avec quelques titres mais il ne doit pas y avoir de sous partie dans chaque grande partie et en mettant des balises HTML de gras pour les points importants.")
    
    print("------------------")
    print(article)
    print("------------------")

    return article +" "



