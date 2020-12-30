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
    explanationLine1 = "/ + GET : to check if the server is alive and get API instructions" + '\n'
    explanationLine2 = "/images/ + POST : to send picture to the server. TIFF, BMP, PNG, JPG, JPEG and TGA are supported." + '\n'
    explanationLine3 = "/images/<pictureID> + GET : to get the picture metadata as a JSON file" + '\n'
    explanationLine4 = "/thumbnails/<pictureID>.jpg + GET : to get back the picture as a thumbnail." + '\n'
    explanationLine5 = "/delete/<pictureID> + DELETE : to delete all data concerning the given pictureID"
    return greetingmessage + explanationLine1 + explanationLine2 + explanationLine3 + explanationLine4 + explanationLine5

# méthode de dépot de l'image sur le serveur (via POST)
@app.route('/images', methods = ['POST'])
def uploadpic():
    
    # obtention d'un identifiant d'image (le dossier des métadonnées est fourni pour définir si l'ID est déjà donnée ou non)

    try :
        pictureID = pichandler.definePictureID(metadata_folder)
    except:
        return 'Error : could not provide proper ID', 500
    # try to load the provided file. If not OK, return error
    
    try:
        picture = request.files['file']
    except:
        pichandler.remove_temp_data(temporary_files_folder, pictureID)
        return 'Error : upload problem', 500
    
    # sauvegarde l'image dans un dossier temporaire pour effectuer plus tard l'extraction des metadata
    try:
        picture.save(temporary_files_folder / Path(pictureID))
    except:
        pichandler.remove_temp_data(temporary_files_folder, pictureID)
        return 'Error : metadata extraction problem', 500

    # essai d'ouvrir l'image fourni. Si erreur : retourne 501, fonction pas encore mise en place (les fichiers autre qu'image seront gérés pour le fil rouge)
    if not(pichandler.picture_check(picture, pictureID, pictures_folder)):
        pichandler.remove_temp_data(temporary_files_folder, pictureID)
        return 'Error : file is not recognised as a picture', 501
    else:
        pass

    # extraction de thumbnail
    try:
        with img.open(picture) as new_pic:
            new_pic.save(str(pictures_folder / Path(pictureID + '.' + new_pic.format)))
            pichandler.extractThumbnail(pictureID, new_pic.format)
    except:
        pichandler.remove_temp_data(temporary_files_folder, pictureID)
        return 'Error : could not extract thumbnail', 501
      
    # extraction de metadata et sauvegarde en JSON
    try:
        if pichandler.saveMetadataAsJSON(pictureID, pichandler.extractMetadata(str(temporary_files_folder / Path(pictureID)),pictureID), metadata_folder):
            pichandler.remove_temp_data(temporary_files_folder, pictureID)
            return pictureID, 200
        else:
            pichandler.remove_temp_data(temporary_files_folder, pictureID)
            return 'No metadata extracted', 501
        
    except:
        pichandler.remove_temp_data(temporary_files_folder, pictureID)
        abort(404)



# méthode d'envoi vers le client des informations et métadata de l'image demandée. 
# Le dossier des métadonnées est en parametre pour permettre d'effectuer les tests 
# sur un dossier spécifique différent du dossier de production
@app.route('/images/<pictureID>', methods = ['GET'])
def metadataaccess(pictureID, metadata_folder=metadata_folder):
    
    try:
        
        with open(str(metadata_folder / Path(pictureID + '.json')), 'r') as metadata:
            donnees = str(str(metadata.readlines()) + '\n')
        return donnees

    # si problème : erreur 404, car cas similaire à une page non trouvée
    except:
        abort(404)


# méthode d'accès au thumbnail de l'image vers le client de l'API (via GET) - façon téléchargement
@app.route('/thumbnails/<pictureID>', methods = ['GET'])
def thumbnailaccess(pictureID,thumbnails_folder=thumbnails_folder):
    try:
        return send_file(str(thumbnails_folder / Path(pictureID)), as_attachment=True)
    # si fichier thumbnail non trouvé : erreur 404, car cas similaire à une page non trouvée
    except FileNotFoundError:
        abort(404)

# methode d'effacement des données d'un élément donné
@app.route('/delete/<pictureID>', methods = ['DELETE'])
def deletedata(pictureID):
    message = 'Delete log :\n'
    try :
               
        try:
            os.remove(str(temporary_files_folder / Path(pictureID)))
            message += 'temp file deleted\n'
        except:
            pass
        
        try:
            os.remove(str(thumbnails_folder / Path(pictureID + '.jpg')))
            message += 'thumbnail deleted\n'
        except:
            pass
        
        try:
            with open(str(metadata_folder / Path(pictureID + '.json'))) as metadata:
                picformat = json.load(metadata)['Format']
            os.remove(str(pictures_folder / Path(pictureID + '.' + picformat)))
            message += 'picture deleted\n'
        except:
            pass
        
        try:
            os.remove(str(metadata_folder / Path(pictureID + '.json')))
            message += 'metadata deleted\n'
        except:
            pass
        
        return message + 'Object data deleted', 200
    except :
        return message, 404
