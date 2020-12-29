import pprint
# importation de flask comme serveur web
from flask import Flask, send_from_directory, request, abort, send_file
# utilisation de la librairie os pour gérer les chemins d'accès et la navigation dans les fichiers
import os
# importation de json pour pouvoir lire les fichiers json contenant les métadonnées
import json
# utilisation de la librairie PIL pour gérer les images
from PIL import Image as img
# utilisation de la librairie 'Path' pour assurer une bonne gestion des chemins de fichiers
from pathlib import Path
# importation des fonctions du service de gestion des images
import pichandler

app = Flask(__name__)
texte = pprint.pformat(__name__) + '\n'

# lignes de configuration des dossiers de stockage des images, thumbnails et fichiers temporaires - ils sont tous à la racine du dossier du python
temporary_files_folder = Path('./temp')
app.config['UPLOAD_FOLDER'] = temporary_files_folder
pictures_folder = Path('./pictures')
thumbnails_folder = Path('./thumbnails')
app.config["CLIENT_IMAGES"] = pictures_folder
metadata_folder = Path('./metadata')

#page racine de l'API
@app.route('/')
def mainpage():
    greetingmessage = 'Server is up and running' + '\n'
    explanationLine1 = "/ + requete GET : racine, indique si le serveur tourne" + '\n'
    explanationLine2 = "/images/<pictureID> + requete GET : donne les métadata de l'image considérée" + '\n'
    explanationLine3 = "/images/ + requete POST : permet d'envoyer une image sur le serveur. Les formats TIFF, BMP, PNG, JPG, JPEG, TGA sont supportés." + '\n'
    explanationLine4 = "/thumbnails/<pictureID> + requete GET : permet de récupérer le thumbnail d'une image." + '\n'

    return greetingmessage + explanationLine1 + explanationLine2 + explanationLine3 + explanationLine4

# méthode de dépot de l'image sur le serveur (via POST)
@app.route('/images', methods = ['POST'])
def uploadpic():
    
    # obtention d'un identifiant d'image (le dossier des métadonnées est fourni pour définir le )

    try :
        pictureID = pichandler.definePictureID(metadata_folder)
    except:
        return 'Error : could not provide proper ID', 500
    # try to load the provided file. If not OK, return error
    
    try:
        picture = request.files['file']
    except:
        return 'Error : upload problem', 500
    
    # sauvegarde l'image dans un dossier temporaire pour effectuer plus tard l'extraction des metadata
    try:
        picture.save(temporary_files_folder / Path(pictureID))
    except:
        return 'Error : metadata extraction problem', 500

    # essai d'ouvrir l'image fourni. Si erreur : retourne 501, fonction pas encore mise en place (les fichiers autre qu'image seront gérés pour le fil rouge)
    
    if not(pichandler.picture_check(picture, pictureID, pictures_folder)):
        return 'Error : file is not recognised as a picture', 501
    else:
        pass

    # extraction de thumbnail
    try:
        with img.open(picture) as new_pic:
            new_pic.save(str(pictures_folder / Path(pictureID + '.' + new_pic.format)))
            pichandler.extractThumbnail(pictureID, new_pic.format)
    except:
        return 'Error : could not extract thumbnail', 501

    # extraction de metadata et sauvegarde en JSON
    try:
        if pichandler.saveMetadataAsJSON(pictureID, pichandler.extractMetadata(str(temporary_files_folder / Path(pictureID)),pictureID), metadata_folder):
        
            return pictureID
        else:
            return 'No metadata extracted'
    except:
        abort(404)


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
            donnees = str('{"status" : "OK"}\n' + str(metadata.readlines()) + '\n' + 'http://127.0.0.1:5000/thumbnails/' + pictureID + '.jpg\n')
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