# coding=UTF-8
# importation d'unittest pour executer les tests
import unittest
# importation du script à tester
import pichandler
# utilisation de la librairie 'Path' pour assurer une bonne gestion des chemins de fichiers
from pathlib import Path
# fonction random.randint pour générer des tests plus aléatoires
from random import randint

# Ceci est le fichier de tests unitaires des fonctions de pichandler.py.
# Les fonctions de pichandler.py 'extractThumnail' et 'saveMetadataAsJSON' sont testés via l'API et des scénarios de tests plus complexes dans test_hlamy_main.py ;
# celles-ci ne retourne rien de vraiment testable autre que les fichiers créés. Il me semble donc plus pertinent de les tester dans des scénarios complets.

# définition des dossiers de tests
temporary_files_folder = './tests/test_temp'
pictures_folder = Path('./tests/test_pictures')
thumbnails_folder = Path('./tests/test_thumbnails')
metadata_folder = Path('./tests/test_metadata')


class TestPicHandler(unittest.TestCase):


    # vérifie la définition d'un ID correct (testé 25 fois)
    def test_definePictureID(self):
        for i in range(25):
            self.assertGreater(int(pichandler.definePictureID(metadata_folder)),999999)
            self.assertLess(int(pichandler.definePictureID(metadata_folder)),9999999)

    # test de l'extraction de metadonnées (soit un fichier de métadonnée en erreur, soit un fichier avec les données de l'image, si celle-ci existe)
    def test_extractMetadata(self):
       pictureID = pichandler.definePictureID(metadata_folder)
       pichandler.extractMetadata(str(temporary_files_folder / Path(pictureID)),pictureID)
       metadatatest = pichandler.extractMetadata(str(temporary_files_folder / Path(pictureID)),pictureID)
     
       self.assertIn('Error', metadatatest)

        # verification que le string de métadonnées est bien construit si l'image existe
       pictureID = str(9999999)
       pichandler.extractMetadata(str(temporary_files_folder / Path(pictureID)),pictureID)
       metadatatest = pichandler.extractMetadata(str(temporary_files_folder / Path(pictureID)),pictureID)
     
       self.assertIn('PictureId', metadatatest)


    # test de la vérification d'ID : doit retourner un bouleen "faux" (testé 25 fois) sauf pour 9999999 (testé une fois), le seul fichier de métadata présent.
    def test_verifyifIDtaken(self):
        for i in range(25):
            resultat = pichandler.verifyifIDtaken(str(randint(1000000,9999998)), metadata_folder)
            self.assertFalse(resultat)
        
        resultat = pichandler.verifyifIDtaken(str(9999999), metadata_folder)
        self.assertTrue(resultat)

    # test de la fonction de vérification qu'un fichier est - ou non - une image
    def test_picture_check(self):
        pictureID = '9999999'
        # verifie qu'un fichier image est bien reconnu comme tel (retourne 'True')
        self.assertTrue(pichandler.picture_check(pictures_folder / Path(pictureID + '.tga'), pictureID, pictures_folder))
        self.assertTrue(pichandler.picture_check(pictures_folder / Path('png.png'), pictureID, pictures_folder))

        # verifie qu'un fichier non image est bien reconnu comme tel (retourne 'False')
        self.assertFalse(pichandler.picture_check(pictures_folder / Path(pictureID + '.txt'), pictureID, pictures_folder))
        self.assertFalse(pichandler.picture_check(pictures_folder / Path(pictureID + '.pdf'), pictureID, pictures_folder))

    # test de la fonction de convertion en string, int ou float (qui sert notamment à la génération correcte de fichiers de métadonnées)
    def test_convertvalue(self):
        self.assertEqual(pichandler.convertvalue('00001'), 1)
        self.assertEqual(pichandler.convertvalue('000.1'), 0.1)
        self.assertEqual(pichandler.convertvalue('bobleponge'), 'bobleponge')
        self.assertEqual(pichandler.convertvalue('éù%^$'), 'éù%^$')


# lancement de la procédure de test
if __name__ == '__main__':
    unittest.main()
