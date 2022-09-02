import requests, json
import urllib.parse
from geopy import distance
from datetime import datetime,timedelta


def calcul_distance(ad1,ad2):
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    r1=requests.get(api_url + urllib.parse.quote(ad1))
    r2=requests.get(api_url + urllib.parse.quote(ad2))
    d=distance.distance(r1.json()["features"][0]['geometry']["coordinates"],r2.json()["features"][0]['geometry']["coordinates"])
    return int(d.meters)

def display_date(seconde):
    d=datetime.now()
    dt=timedelta(seconds=seconde,microseconds=-d.microsecond)
    d=d+dt
    return d.isoformat(sep=" ")


def heure_retour_estim(ad2):
    ad1 = "7 avenue Edouard Belin TOULOUSE 31400"
    vitesse = 10
    d=calcul_distance(ad1,ad2)
    temps=(d//vitesse)*2
    date_retour=display_date(temps)
    return date_retour,temps