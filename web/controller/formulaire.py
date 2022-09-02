from ..data import bdd as b
from flask import session
from hashlib import md5
from web.annexe.envoi_mail import mailing
config = {
        'user': 'chronodrone',
        'password': 'groupeB',
        'host': 'localhost',
        'port': 3306 ,
        'database': 'IENAC20_Allietta_Jouquey_Lemoine_Rivoalen',
        'raise_on_warnings': True
    }
def crypt_mdp(mdp):
    return md5(mdp.encode()).hexdigest()

def getSession():
    login = session['login']
    return login

def addSomeone(request):
    nom = request.form['nom']
    prenom = request.form['prenom']
    login = request.form['login']
    mdp = request.form['mdp']
    service = request.form['service']
    msg = b.addPerson(nom,prenom, login, crypt_mdp(mdp), service)
    return msg

def addPackage(request):
    nom_expediteur = request.form["nom_expediteur"]
    prenom_expediteur = request.form["prenom_expediteur"]
    entreprise = request.form["entreprise"]
    nom_destinataire = request.form["nom_destinataire"]
    prenom_destinataire = request.form["prenom_destinataire"]
    adresse_destination = request.form["adresse_destination"]
    masse_colis = request.form["masse_colis"]
    msg = b.addColisData(nom_expediteur, prenom_expediteur, entreprise, nom_destinataire, prenom_destinataire, adresse_destination, masse_colis)
    return msg

def addDrone(request):
    type = request.form['type']
    msg = b.addDroneData(type)
    return msg

def verifAuth(request):
    login = request.form['login']
    mdp = crypt_mdp(request.form['mdp'])
    msg, empl, pers = b.verifAuthData(login, mdp)
    try:
        session['login'] = empl['login']
        session['prenom'] = pers['Prenom']
        session['nom'] = pers['Nom']
        session['service'] = empl['service']
    except Exception as e:
        msg = "erreur"
    return msg

def deletePeople(request):
    idPers = request.form['Id_Personne']
    msg = b.deletePeopleData(idPers)
    return msg

def deleteResa(request):
    idColis = request.form['Id_Colis']
    idDrone = request.form['Id_Drone']
    msg = b.deleteResaData(idColis, idDrone)
    return msg

def deleteDrone(request):
    idDrone = request.form['Id_Drone']
    msg = b.deleteDroneData(idDrone)
    return msg

def selectADrone(request):
    idDroneS = request.form['Id_Drone']
    idColis = request.form['Id_Colis']
    b.droneReserveData(idDroneS)
    return idDroneS, idColis

def addComment(request):
    nom=request.form['nom']
    email=request.form['email']
    text=request.form['textarea']
    msg = b.addCommentData(nom,email,text)
    return msg

def addNewsletter(request):
    email=request.form['email']
    msg = b.addNewsletterData(email)
    return msg

def changeMdp(request):
    oldmdp = request.form['oldmdp']
    newmdp = request.form['newmdp']
    confmdp = request.form['confmdp']
    if newmdp == confmdp:
        mdp = crypt_mdp(newmdp)
        oldmdp = crypt_mdp(oldmdp)
        msg = b.changeMdpData(mdp, oldmdp, session['login'])
    else:
        msg = "erreur"
    return msg

def deletePackage(request):
    idColis = request.form['Id_Colis']
    msg = b.deleteColisData(idColis)
    return msg

def sendResponse(request):
    objet = request.form['objet']
    text = request.form['textarea']
    t = text.split('\n')
    text = "<br />".join(t)
    email = request.form['email']
    message = request.form['msg']
    m = message.split('\n')
    msg = "<br />".join(m)
    idMessage = request.form['Id_Message']
    nom = request.form['nom']
    html = """<html>
                <head>
                    <meta charset="utf-8" />
                </head>
                <body>
                    <header>Bonjour {},</header>
                    <p>{}</p>
                    <p>Bien cordialement, <br /> L'équipe du service client Chronodrone</p>
                    <i><p>Pour rappel, vous nous aviez envoyé :<br /><br />"{}"</p></i>
                </body>
                </html>""".format(nom,text, msg)
    mail = mailing(objet, html, email, "Réponse")
    base = b.sendResData(idMessage)
    return mail, base

def sendNews(request):
    objet = request.form['objet']
    text = request.form['textarea']
    t = text.split('\n')
    text = "<br />".join(t)
    html = """<html>
                    <head>
                        <meta charset="utf-8" />
                    </head>
                    <body>
                        <header>Bonjour,</header>
                        <p>{}</p>
                        <p>Bien cordialement, <br /> L'équipe du service client Chronodrone<br /><br /><i>Merci de ne pas répondre à ce mail</i></p>
                        
                    </body>
                    </html>""".format(text)
    b.sendNews(objet, html)

def validDelivery(request):
    idColis = request.form['Id_Colis']
    msg = b.validLivData(idColis)
    return msg

def deleteLiv(request):
    idColis = request.form['Id_Colis']
    idDrone = request.form['Id_Drone']
    msg = b.deleteLivData(idColis,idDrone)
    return msg

def maintenanceDrone(request):
    idDrone = request.form['Id_Drone']
    msg = b.maintenance(idDrone)
    return msg