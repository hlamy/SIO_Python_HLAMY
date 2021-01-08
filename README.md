# SIO_Python_HLAMY

#### Description ####

Ceci est une application �crite dans le cadre du mast�re SIO 2021 de CentraleSup�lec, par l'�l�ve Hugues LAMY.
Elle permet de g�n�rer un thumbnail et d'extraire des m�tadonn�es � partir d'une image fourni par l'utilisateur, via des API de type REST.

#### Installation ####

Python 3.8, puis les librairies flask, pillow, celery et pathlib doivent en premier lieu �tre install�es.

# python : python 3.8

# flask library, 1.1.2 :
installation via $ pip install flask

# pillow library, 8.0.1:
installation via $ pip install pillow

# celery library, 5.0.5:
installation via $ pip install celery

# pathlib library, 1.0.1
installation via $ pip install pathlib

Ensuite, le contenu du fichier zipp� doit �tre d�zipp� dans le r�pertoire choisi par l'utilisateur pour faire fonctionner l'application. En pratique, les fichiers "launcher.py", "hlamy_main.py", et "pichandler.py" sont n�cessaires � minima pour faire fonctionner l'application. 

Le lancement de celle-ci verra la cr�ation, s'il n'existent pas d�j�, des dossiers /metadata, /pictures, /temp et /thumbnail. Ceux-ci contiendront les fichiers n�cessaires � l'application.

### Tests ####

Les fichiers restants sont eux indispensables pour r�aliser les tests de fonctionnement : test_pichandler.py r�alise les tests sur les fonctions de pichandler.py pendant que test_hlamy_main teste lui l'application web. Le dossier tests et ses sous-dossiers contiennent des

### Mise en route de l'application ###

L'application peut �tre lanc�e via l'execution du script "laucher.py". Aucune autre action n'est n�cessaire, mais l'utilisateur doit avoir les droits suffisants pour que le script puisse executer/lire et �crire dans son dossier courant.

Ce script lancera un serveur flask accessible en local sur le port 5000, c'est � dire sur http://localhost:5000/. 

Le bon acc�s a la page racine http://localhost:5000/ confirme 

#### Les contrats API : ####

/images/ + requete POST : permet d'envoyer une image sur le serveur. Les formats TIFF, BMP, PNG, JPG, JPEG et TGA sont support�s.

/ + requ�te GET : racine, indique si le serveur tourne. Fourni aussi des indications concernant les contrats API.

/images/<pictureID> + requ�te GET : donne les m�tadata de l'image consid�r�e dans un fichier au format JSON. Si des donn�es EXIF existent, elles y sont ajout�es. Sinon, seules des m�tadonn�es basiques sont fournies (incluant un identifiant unique d'image g�n�r� par l'application ainsi que le chemin pour atteindre le thumbnail).

/thumbnails/<pictureID>.jpg + requ�te GET : permet de r�cup�rer le thumbnail de l'image demand�e. 

/delete/<pictureID> + requ�te DELETE : permet de supprimer les donn�es issues du traitement d'une image (metadonn�es, thumbnail, etc.).


#### Requ�tes CURL ####

# Voici quelques requ�tes CURL utilisables pour atteindre l'application via ses API :

# possible requete CURL pour envoyer une image:
curl -F file="@nom_image.format" -X POST http://127.0.0.1:5000/images

# possible requete CURL pour r�cup�rer les m�tadonn�es de l'image :
curl http://127.0.0.1:5000/images/<pictureID>

# possible requete CURL pour r�cup�rer le thumbnail de l'image, sauvegard� dans le dossier courant :
curl --output <pictureID>.jpg http://127.0.0.1:5000/thumbnails/<pictureID>.jpg


#### limitations : ####
- Les fichiers "texture" ne sont pas pris en compte, ce ne sont pas des formats d'image ;
- Les fichiers "logiciel de retouche" ne sont pas pris en compte, ce ne sont pas des formats d'image ;
- Les fichiers '.gif' ne sont pas compatible ;