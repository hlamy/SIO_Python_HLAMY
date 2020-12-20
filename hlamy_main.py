import pprint
from random import randint
from flask import Flask, send_from_directory, request, abort, send_file
# utilisation de la librairie os pour gérer les chemins d'accès
import os
import json
# utilisation de la librairie PIL pour gérer les images
from PIL import Image as img
# utilisation de la librairie 'Path' pour assurer une bonne gestion des chemins de fichiers
from pathlib import Path
# importation des fonctions du service de gestion des images
import pichandler

app = Flask(__name__)
texte = pprint.pformat(__name__) + '\n'

# lignes de configuration des dossiers de stockage des images, thumbnails et fichiers temporaires
app.config['UPLOAD_FOLDER'] = 'f:/GitHub/SIO_Python_HLAMY/Temp'
temporary_files_folder = 'f:/GitHub/SIO_Python_HLAMY/Temp'
pictures_folder = Path('f:/GitHub/SIO_Python_HLAMY/pictures')
thumbnails_folder = Path('F:/GitHub/SIO_Python_HLAMY/thumbnails')
app.config["CLIENT_IMAGES"] = pictures_folder
metadata_folder = Path('F:/GitHub/SIO_Python_HLAMY/metadata')

#page racine de l'API
@app.route('/')
def mainpage():
    picturename = 'pictures/test.jpg'

    return pichandler.extractMetadata(picturename)

# méthode de dépot de l'image sur le serveur (via POST)
@app.route('/images', methods = ['POST'])
def uploadpic():
    
    # obtention d'un identifiant d'image
    try :
        pictureID = pichandler.definePictureID(pictures_folder)
    except:
        return 'Error : could not provide proper ID'
    # try to load the provided file. If not OK, return error
    
    try:
        picture = request.files['file']
    except:
        return 'Error : upload problem'
    
    # sauvegarde l'image dans un dossier temporaire et extraction des metadata
    try:
        picture.save(temporary_files_folder / Path(pictureID))
        #pichandler.saveMetadataAsJSON(temporary_files_folder / Path(pictureID), metadata_folder)
    except:
        return 'Error : metadata extraction problem'

    # try to open provided file as a picture. If OK, save it, if not, return error
    try:
        with img.open(picture) as new_pic:
            new_pic.save(str(pictures_folder / Path(pictureID + '.' + new_pic.format)))
    except:
        return 'Error : file is not a picture'

    # extraction de thumbnail (action synchrone pour le moment)
    try:
        pichandler.extractThumbnail(pictureID, new_pic.format)
    except:
        return 'Error : could not extract thumbnail'

    # extraction de metadata et sauvegarde en JSON (action synchrone pour le moment)
    try:
        if pichandler.saveMetadataAsJSON(pictureID, pichandler.extractMetadata(str(temporary_files_folder / Path(pictureID))), metadata_folder):
        
            return pictureID
        else:
            return 'no metadata'
    except:
        abort(500)


# méthode d'envoi vers le client des métadata de l'image demandée
@app.route('/images/metadata/<pictureID>', methods = ['GET'])
def pictureInfoAccess(pictureID):
    try:
        return send_file(str(metadata_folder / Path(pictureID + '.json')), as_attachment=True), 'OK'
    # si fichier non trouvé : erreur 404, car cas similaire à une page non trouvée
    except FileNotFoundError:
        abort(404)

# méthode d'envoi vers le client des informations et métadata de l'image demandée
@app.route('/images/<pictureID>', methods = ['GET'])
def metadataaccess(pictureID):
    
    try:
        
        with open(str(metadata_folder / Path(pictureID + '.json')), 'r') as metadata:
            donnees = str({'"status" : "OK"}\n' + str(metadata.readlines()) + '\n' + 'http://127.0.0.1:5000/thumbnails/' + pictureID + '.jpg\n')
        return donnees

    # si problème : erreur 404, car cas similaire à une page non trouvée
    except:
        abort(404)


# méthode d'envoi de l'image demandée vers le client de l'API (via GET) - façon téléchargement
@app.route('/download/<picturename>', methods = ['GET'])
def pictureaccess(picturename):
    try:
        return send_file(str(pictures_folder / Path(picturename)), as_attachment=True)
    # si fichier non trouvé : erreur 404, car cas similaire à une page non trouvée
    except FileNotFoundError:
        abort(404)

# méthode d'accès au thumbnail de l'image vers le client de l'API (via GET) - façon téléchargement
@app.route('/thumbnails/<picturename>', methods = ['GET'])
def thumbnailaccess(picturename):
    try:
        return send_file(str(thumbnails_folder / Path(picturename)), as_attachment=True)
    # si fichier thumbnail non trouvé : erreur 404, car cas similaire à une page non trouvée
    except FileNotFoundError:
        abort(404)