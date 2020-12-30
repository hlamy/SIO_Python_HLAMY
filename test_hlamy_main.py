# importation d'unittest pour executer les tests
import unittest
from unittest import mock
# importation du script à tester sous le nom "appli" pour pouvoir modifier plus tard le nom du fichier principal
import hlamy_main as appli
# utilisation de la librairie 'Path' pour assurer une bonne gestion des chemins de fichiers
from pathlib import Path
import io
# Ceci est le fichier de test de l'ensemble des fonctions de hlamy_main.py. Il contient des scénarios de tests qui permettent de tester l'ensemble des fonctionnalités et des API de l'application

# définition des dossiers de tests
temporary_files_folder = './test_temp'
pictures_folder = Path('./test_pictures')
thumbnails_folder = Path('./test_thumbnails')
metadata_folder = Path('./test_metadata')

# definition du décorateur pour tester la partie application
def avec_client(f):
    def func(*args, **kwargs):
        with appli.app.test_client() as client:
            return f(*args, client, **kwargs)

    return func


class TestBasicHLamy_Main(unittest.TestCase):


    # test unitaire de la page principale de l'application
    def test_mainPage(self):
        resultatAttendu = 'Server is up and running'
        self.assertIn(resultatAttendu, appli.mainpage())


    # test unitaire de la méthode d'accès aux métadonnées. Le pictureID : '9999999' est connu présent dans le dossier de test.
    def test_metadataaccess(self):
        resultatAttendu = '"PictureId": "9999999"'
        self.assertIn(resultatAttendu ,  appli.metadataaccess('9999999',metadata_folder))

    # test de scénario complet, d'envoi d'une photo, de lecture de ses métadonnées puis de récupération du thumbnail
    @avec_client
    def testScenarioUploadReadDownload(self, client):
        
        # test de réponse négative si metadonnées absentes (pictureID hors champs, donc absent sinon c'est une erreur)
        result = client.get("/images/10000000")
        self.assertEqual(result.status_code, 404)

        # test de réponse négative si thumbnail absent (pictureID hors champs, donc absent sinon c'est une erreur)
        result = client.get("/thumbnails/10000000.jpg")
        self.assertEqual(result.status_code, 404)

        # test d'envoi d'un fichier non image vers le serveur via l'API /images + POST
        fakefilename = 'testfile.txt'
        fakefile = b'bourrage'
        testfile = (io.BytesIO(fakefile), fakefilename)
        testdata = {'file': testfile}
            
        serverresponse = client.post('/images', data=testdata, follow_redirects=True, content_type='multipart/form-data')
        self.assertEqual(serverresponse.status_code, 501)

        


    #def test_thumbnailaccess(self):
    #    pictureID = '9999999'
    #    thumbnailPic = appli.thumbnailaccess(pictureID,thumbnails_folder)

# lancement de la procédure de test
if __name__ == '__main__':
    unittest.main()