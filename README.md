# SIO_Python_HLAMY


#### Description ####

Ceci est une application écrite dans le cadre du mastère SIO 2021 de CentraleSupélec, par l'élève Hugues LAMY.
Elle permet de générer un thumbnail et d'extraire des métadonnées à partir d'une image fourni par l'utilisateur, via des API de type REST.

Le développement a été effectué avec VS Code - l'environnement virtuel crée par celui-ci est dans le dossier /venv.

#### Installation ####

Cet outil de génération de thumbnail a été developpé sous windows et testé avec la distribution "DEBIAN" de GNU/LINUX (système recommandé).

Python 3.8, puis les librairies flask, pillow, celery et pathlib doivent être installées.

# python : python 3.8

# flask library, 1.1.2 :
installation via $ pip install flask

# pillow library, 8.0.1:
installation via $ pip install pillow

# celery library, 5.0.5:
installation via $ pip install celery

# pathlib library, 1.0.1
installation via $ pip install pathlib

Ensuite, le contenu du fichier zippé doit être dézippé dans le répertoire choisi par l'utilisateur pour faire fonctionner l'application. En pratique, seulement les fichiers "launcher.py", "hlamy_main.py", et "pichandler.py" sont nécessaires à minima pour faire fonctionner l'application. 

Le lancement de celle-ci verra la création, s'il n'existent pas déjà, des dossiers /metadata, /pictures, /temp et /thumbnail. Ceux-ci contiendront les fichiers nécessaires à l'application.

L'environnement virtuel est présent dans le dossier /venv au besoin.

### Tests ####

Les fichiers restants sont eux indispensables pour réaliser les tests de fonctionnement : test_pichandler.py réalise les tests sur les fonctions de pichandler.py alors que test_hlamy_main teste lui l'application web. Le dossier tests et ses sous-dossiers contiennent des données controlées destinées à vérifier le bon retour de l'application lors de l'envoi de ces documents.


### Mise en route de l'application ###

L'application peut être lancée via l'execution du script "laucher.py". Aucune autre action n'est nécessaire, mais l'utilisateur doit avoir les droits suffisants pour que le script puisse executer/lire et écrire dans son dossier courant.

Ce script lancera un serveur flask accessible sur le port 5000, c'est à dire par exemple sur http://localhost:5000/ (ou l'adresse IP de la machine serveur suivi de :5000). 

Le bon accès a la page racine http://localhost:5000/ confirme le bon fonctionnement de l'application et donne les informations sur l'API.


#### Les contrats API : ####

/images/ + requete POST : permet d'envoyer une image sur le serveur. Les formats TIFF, BMP, PNG, JPG, JPEG et TGA sont supportés. un pictureID à 7 chiffres (compris entre 1000000 et 9999999) est renvoyé par l'application.

/ + requête GET : racine, indique si le serveur tourne. Fourni aussi des indications concernant les contrats API.

/images/<pictureID> + requête GET : donne les métadata de l'image considérée dans un fichier au format JSON. Si des données EXIF existent, elles y sont ajoutées. Sinon, seules des métadonnées basiques sont fournies (incluant un identifiant unique d'image généré par l'application ainsi que le chemin pour atteindre le thumbnail).

/thumbnails/<pictureID>.jpg + requête GET : permet de récupérer le thumbnail de l'image demandée. 

/delete/<pictureID> + requête DELETE : permet de supprimer les données issues du traitement d'une image (metadonnées, thumbnail, etc.).


#### Requêtes CURL ####

# Voici quelques requêtes CURL utilisables pour atteindre l'application via ses API :

# possible requete CURL pour envoyer une image:
curl -F file="@nom_image.format" -X POST http://127.0.0.1:5000/images

# possible requete CURL pour récupérer les métadonnées de l'image :
curl http://127.0.0.1:5000/images/<pictureID>

# possible requete CURL pour récupérer le thumbnail de l'image, sauvegardé dans le dossier courant :
curl --output <pictureID>.jpg http://127.0.0.1:5000/thumbnails/<pictureID>.jpg


#### limitations : ####

- Les fichiers "texture" ne sont pas pris en compte, ce ne sont pas des formats d'image ;
- Les fichiers "logiciel de retouche" ne sont pas pris en compte, ce ne sont pas des formats d'image ;
- Les fichiers '.gif' ne sont pas compatible avec l'application ;
- un maximum de 9 millions de fichiers sont envoyables sur l'application (ceci pour rester raisonnable : il est possible d'augmenter cette taille dans le programme si cela est désiré, mais hors des enjeux d'une application scolaire).