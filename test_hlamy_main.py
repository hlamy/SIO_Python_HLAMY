# coding=UTF-8
# importation d'unittest pour executer les tests
import unittest
# importation du script à tester sous le nom "appli" pour pouvoir modifier plus tard le nom du fichier principal
import hlamy_main as appli
# utilisation de la librairie 'Path' pour assurer une bonne gestion des chemins de fichiers
from pathlib import Path
# importation de la librairie io pour gérer les fichiers binaires
import io
# importation de la librairie json pour gérer les fichiers métadonnées générés par l'application
import json
from PIL import Image

# Ceci est le fichier de test de l'ensemble des fonctions de hlamy_main.py. Il contient des scénarios de tests qui permettent de tester l'ensemble des fonctionnalités et des API de l'application

# définition des dossiers de tests
temporary_files_folder = './tests/test_temp'
pictures_folder = Path('./tests/test_pictures')
thumbnails_folder = Path('./tests/test_thumbnails')
metadata_folder = Path('./tests/test_metadata')
testsfile_folder = Path('./tests/test_files')


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
        self.assertIn(resultatAttendu, appli.metadataaccess('9999999', metadata_folder))

    # test de remontée d'erreur, en cas d'envoi de mauvais fichiers par exemple.
    @avec_client
    def testOfErrors(self, client):
        # test de réponse négative si metadonnées absentes (pictureID hors champ, donc absent - sinon c'est une erreur)
        with client.get("/images/10000000") as result:
            self.assertEqual(result.status_code, 404)

        # test de réponse négative si thumbnail absent (pictureID hors champ, donc absent - sinon c'est une erreur)
        with client.get("/thumbnails/10000000.jpg") as result:
            self.assertEqual(result.status_code, 404)

        # test d'envoi d'un fichier non image vers le serveur via l'API /images + POST - réponse erreur 501 attendue (gestion des fichiers non image non implémentée)
        fakefilename = 'testfile.txt'
        fakefile = b'bourrage'
        testfile = (io.BytesIO(fakefile), fakefilename)
        testdata = {'file': testfile}
        with client.post('/images', data=testdata, follow_redirects=True,
                         content_type='multipart/form-data') as serverresponse:
            self.assertEqual(serverresponse.status_code, 501)

        # verification qu'un fichier non image, même avec une extension image, remonte bien une erreur 501 (gestion des fichiers non image non implémentée)
        fakefilename = 'testbrokenpic.jpg'
        fakefile = b'Ceci n"est pas une photo'
        testfile = (io.BytesIO(fakefile), fakefilename)
        testdata = {'file': testfile}
        with client.post('/images', data=testdata, follow_redirects=True,
                         content_type='multipart/form-data') as serverresponse:
            self.assertEqual(serverresponse.status_code, 501)

    # test de scénario complet, d'envoi d'une photo, de lecture de ses métadonnées puis de récupération du thumbnail, pour enfin effacer les données créées. Les 4 API sont testées.
    @avec_client
    def testScenarioUploadReadDownloadDelete(self, client):
        # Enchainement des tests avec différents formats
        formatlist = ['bmp', 'jpg', 'png', 'tga', 'tiff']
        for formattype in formatlist:
            # ETAPE 1 : envoi d'un fichier image vers le serveur - attente d'une réponse OK - 200
            testpicturename = 'testpic' + '.' + formattype
            testpicpath = str(testsfile_folder / Path(testpicturename))
            with open(testpicpath, 'rb') as img:
                testdata = {'file': (testpicpath, img, 'multipart/form-data')}

            serverresponse = client.post('/images', data=testdata, follow_redirects=True)

            # on récupère le pictureID donné par le serveur pour en vérifier la validité et le réutiliser par la suite
            receivedPictureID = int(serverresponse.data)
            self.assertGreater(receivedPictureID, 999999)
            self.assertLess(receivedPictureID, 9999999)
            # on vérifie qu'on obtient bien un code de réponse "200"
            self.assertEqual(serverresponse.status_code, 200)
            serverresponse.close()

            # ETAPE 2 : récupération des métadonnées issues de l'étape précédente
            with client.get('/images' + '/' + str(receivedPictureID)) as serverresponse:
                receivedMetadata = str(serverresponse.data.decode("utf-8"))

                # verification du code de réponse reçu à 200 et que le fichier de métadonnées contient bien à minima le pictureID du thumbnail
                self.assertIn('PictureId' and str(receivedPictureID), receivedMetadata)
                self.assertEqual(serverresponse.status_code, 200)

            # ETAPE 3 : récupération du thumbnail
            with client.get('/thumbnails' + '/' + str(receivedPictureID) + '.jpg') as serverresponse:
                # verification que la réponse reçue est bien "200"
                self.assertEqual(serverresponse.status_code, 200)

                # verification que le thumbnail reçu à bien une dimension à 75 (hauteur ou largeur)
                receivedThumbnail = Image.open(io.BytesIO(serverresponse.data))
                self.assertIn('75', str(receivedThumbnail.size))
                receivedThumbnail.close()

            # pour terminer le scénario, suppression de l'ensemble des données créées précédement
            with client.delete('/delete' + '/' + str(receivedPictureID)) as serverresponse:
                self.assertEqual(serverresponse.status_code, 200)


# lancement de la procédure de test
if __name__ == '__main__':
    unittest.main()
