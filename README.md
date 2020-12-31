# SIO_Python_HLAMY

#### Requirements : ####
# python : python 3.7

# flask library, 1.1.2 :
installation via $ pip install flask

# pillow library, 8.0.1:
installation via $ pip install pillow

# celery library, 5.0.5:
installation via $ pip install celery




#### Les API : ####
/ + requete GET : racine, indique si le serveur tourne
/images/<pictureID> + requete GET : donne les métadata de l'image considérée
/images/ + requete POST : permet d'envoyer une image sur le serveur. Les formats TIFF, BMP, PNG, JPG, JPEG et TGA sont supportés.
/thumbnails/<pictureID> + requete GET : permet de récupérer le thumbnail d'une image
/delete/<pictureID> + requete DELETE : permet de supprimer les données issues du traitement d'une image (metadonnées, thumbnail, etc.)


#### Les requêtes CURL utilisables pour utiliser l'application via ses API : ####

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