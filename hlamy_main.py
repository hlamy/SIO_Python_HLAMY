import json
import pprint
from flask import Flask

app = Flask(__name__)
texte = pprint.pformat(__name__) + '\n'

#page racine de l'API
@app.route('/')
def mainpage():
    page = "Test 2"
    return page

# lancement de l'application :
app.run()