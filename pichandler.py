# importation de fonctions de la librairie "pillow" pour assurer la manipulation des images
from PIL import Image as img
from PIL.ExifTags import TAGS
# utilisation de la librairie 'Path' pour assurer une bonne gestion des chemins de fichiers
from pathlib import Path
# importation de fonction de la librairie "os" pour gérer la recherche dans les fichiers
from os import walk
from os.path import isfile, join
# importation de json pour générer les fichiers de métadonnées
import json
from random import randint
# importation de celery pour paralleliser le travail sur les images
from celery import Celery


appcelery = Celery('tasks', broker='redis://localhost', backend='redis://localhost')

# fonction de vérification du pictureID, pour vérifier que celui-ci est utilisé ou non:
@appcelery.task
def verifyifIDtaken(pictureID,picture_folder):
    result = False
    # liste l'ensemble des fichiers dans le dossier d'images
    for files in walk(picture_folder):
        # liste les documents dans chaque dossier trouvé
        for docs in files:
            # vérifie la présence ou non de l'image recherchée
            if pictureID in docs:
              result = True

    return result

# fonction de définition d'un identifiant d'image unique
@appcelery.task
def definePictureID(picture_folder):
    pictureID = str(randint(1000000, 9999999))
    i=0
    while verifyifIDtaken(pictureID,picture_folder) and i<100:
        pictureID = str(randint(1000000, 9999999))
        i+=1
    if i<100:
        return pictureID

# fonction d'ouverture et d'extraction des métadonnées d'une image:
@appcelery.task
def extractMetadata(picturename):
    try:
        # Création d'un dictionnaire pour conserver les métadonnées
        metadata = {}

        with img.open(picturename) as pic:
            
            # On récupere certaines données spécifique de l'image grâce aux méthodes de la librairie 'pillow':
            metadata['PictureId'] = picturename
            metadata['Format'] = pic.format
            metadata['Size'] = pic.size
            metadata['Mode'] = pic.mode
            
            # Avec la librairie ExifTags de pillow, on peut récurérer les métadonnées de type EXIF (métadonnées de photographie) :
            try:
                metadata['EXIF'] = True
                for tag, valeur in pic._getexif().items():
                    metadata[str(tag)] = convertvalue(valeur)

            except AttributeError:
                #Une métadonnée pour signifier que les métadonnées de type photographique EXIF n'ont pu être récupérées
                metadata['EXIF'] = False
        
    # En cas d'erreur en entrée/sortie (impossible d'ouvrir l'image), le système retourne une erreur dans le dictionnaire de métadonnée :
    except IOError:
        metadata['Error'] = 'Erreur Ouverture Image'
    
    return metadata

# fonction de sauvegarde des metadata vers un fichier json, dans un dossier donné:
@appcelery.task
def saveMetadataAsJSON(pictureID, metadata, folder):
    # la fonction retournera un bouléen en cas de succès (True) ou d'échec (False)
    status = False

    try:
        # ouverture du fichier JSON et écriture des métadata à l'intérieur
        with open(str(folder / Path(pictureID)) + '.json', 'w') as metadatafile:
            json.dump(metadata, metadatafile)
            status = True
    except:
        pass

    return status

#fonction d'extraction d'un thumbnail depuis l'image originale vers le dossier thumbnails
@appcelery.task
def extractThumbnail(picturename, pictureformat, picture_folder = Path('pictures'), thumbnail_folder = Path('thumbnails'), size = (75, 75)):
    #ouverture de l'image "picturename", depuis le dossier picture_folder
    with img.open(picture_folder / Path(picturename + '.' + pictureformat)) as picture:
        # passage de l'image en taille thumbnail
        picture.thumbnail(size)
        # sauvegarde de l'image réduite dans le dossier prévu à cette effet
        picture.save(str(thumbnail_folder / Path(picturename)) + '.jpg', "JPEG")
    return None


# fonction de contrôle, pour vérifier si le fichier est une image ou un autre format
@appcelery.task
def picture_check(picture):

    try:
        pic = img.open(picture)
        pic.close()
        return True
    except:
        return False
    

# fonction de convertion, dans le format qui semble le plus approprié (pour réinjection dans le json contenant les métadonnées) :
@appcelery.task
def convertvalue(value):
    # entiers, décimaux et chaînes de caractères sont possibles. 
    # Retourne None s'il n'est pas possible de convertir en "string" :
    possibleFormats = [int, float, str]
    for f in possibleFormats :
        try:
            return f(value)
        except:
            pass
    return None
