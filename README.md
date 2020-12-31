# SIO_Python_HLAMY

#### Description ####

Ceci est une application écrite dans le cadre du mastère SIO 2021 de CentraleSupélec, par l'élève Hugues LAMY.
Elle permet de générer un thumbnail et d'extraire des métadonnées à partir d'une image fourni par l'utilisateur, via des API de type REST.

#### Installation ####




#### Requirements : ####
# python : python 3.8

# flask library, 1.1.2 :
installation via $ pip install flask

# pillow library, 8.0.1:
installation via $ pip install pillow

# celery library, 5.0.5:
installation via $ pip install celery

# pathlib library, 1.0.1
installation via $ pip install pathlib

#### Les contrats API : ####

/images/ + requete POST : permet d'envoyer une image sur le serveur. Les formats TIFF, BMP, PNG, JPG, JPEG et TGA sont supportés.

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
- Les fichiers '.gif' ne sont pas compatible ;