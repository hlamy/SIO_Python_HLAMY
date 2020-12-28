import unittest
import pichandler
# utilisation de la librairie 'Path' pour assurer une bonne gestion des chemins de fichiers
from pathlib import Path
from random import randint

temporary_files_folder = './temp'
pictures_folder = Path('./pictures')
thumbnails_folder = Path('./thumbnails')
metadata_folder = Path('./metadata')


class TestPicHandler(unittest.TestCase):


    # vérifie la définition d'un ID
    def test_definePictureID(self):
       self.assertGreater(int(pichandler.definePictureID(metadata_folder)),999999)


    # test de l'extraction de metadonnées (soit un fichier de métadonnée en erreur, soit un fichier avec les données de l'image, si celle-ci existe)
    def test_extractMetadata(self):
       
       metadatatest = pichandler.extractMetadata(pichandler.definePictureID(metadata_folder))
     
       self.assertTrue(('Error' in metadatatest) or ('PictureId') in metadatatest)

    # test du retour de la vérification d'ID : doit retourner un bouleen "faux", si le dossier de metadata est vide (c'est à dire qu'aucune photo n'est présente), ce qui doit être le cas avant l'utilisation de l'application
    def test_verifyifIDtaken(self):
        bouleantest = pichandler.verifyifIDtaken(str(randint(1000000,9999999)), metadata_folder)
        self.assertFalse(bouleantest)




# lancement de la procédure de test
if __name__ == '__main__':
    unittest.main()