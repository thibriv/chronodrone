import mysql.connector
from web.annexe.envoi_mail import mailing
from web.annexe import distance_temps as drone
from datetime import datetime

config = {
        'user': 'chronodrone',
        'password': 'groupeB',
        'host': 'localhost',
        'port': 3306 ,
        'database': 'IENAC20_Allietta_Jouquey_Lemoine_Rivoalen',
        'raise_on_warnings': True
    }

vitesse = 10
ADRESSE_ENTREPRISE = "7 avenue Edouard Belin Toulouse 31400"

#################################################################################################################
# connexion au serveur de la base de données
def addDroneData(typeD):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    Etat = 'Libre'
    sql1 = "SELECT Id_Type FROM type WHERE Nom_Type = %s;"
    param1 = (typeD,)
    cursor.execute(sql1, param1)
    id_type = cursor.fetchall()[0][0]
    sql = "INSERT INTO drone(Etat, Heure_Dispo, Id_Type) VALUES (%s,NULL,%s);"
    param = (Etat, id_type)
    cursor.execute(sql, param)
    cnx.commit()
    cnx.close()
    msg = "ok"
    return msg

def deleteDroneData(idDrone):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "DELETE FROM drone WHERE Id_Drone = %s;"
    param = (idDrone,)
    cursor.execute(sql, param)
    cnx.commit()
    cnx.close()
    msg = "ok"
    return msg

def deleteResaData(idColis, idDrone):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "DELETE FROM Reservation WHERE Id_Colis = %s;"
    param = (idColis,)
    cursor.execute(sql, param)
    sql1 = "UPDATE Drone SET Etat = 'Libre' WHERE Id_Drone = %s"
    param1 = (idDrone,)
    cursor.execute(sql1, param1)
    sql2 = "DELETE FROM Livraison WHERE Id_Colis = %s"
    cursor.execute(sql2,param)
    cnx.commit()
    cnx.close()
    msg = "ok"
    return msg

def deletePeopleData(idPers):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "DELETE FROM personne WHERE Id_Personne = %s;"
    param = (idPers,)
    cursor.execute(sql, param)
    cnx.commit()
    cnx.close()
    msg = "ok"
    return msg


def get_employeeData():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary = True)
    sql = "SELECT Nom, Prenom, login, service, personne.Id_Personne FROM personne JOIN employe ON personne.Id_Personne = employe.Id_Personne;"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnx.close()
    msg = "ok"
    return msg, res

def get_droneData():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary = True)
    sql = "SELECT Id_Drone, Nom_Type, Etat, Heure_vol, nb_maintenance, Heure_Dispo FROM Drone JOIN Type ON Drone.Id_Type = Type.Id_Type;"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnx.close()
    msg = 'ok'
    return msg, res

def get_packageData():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary = True)
    sql = "SELECT Prenom, Nom, Entreprise , Masse_Colis, Adresse_Destination, Etat_Colis, Id_Colis FROM colis JOIN Client ON Client.Id_Personne=Colis.Id_Expediteur JOIN Personne ON Personne.Id_Personne=Colis.Id_Expediteur;"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnx.close()
    msg = 'ok'
    return msg, res

def droneReserveData(idDrone):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    sql0 = "SELECT Etat FROM Drone WHERE Id_Drone = %s;"
    param = (idDrone,)
    cursor.execute(sql0, param)
    etat = cursor.fetchone()['Etat']
    print(etat)
    if etat=='En Livraison':
        sql = "UPDATE Drone SET Etat = 'En livraison/Reserve' WHERE Id_Drone = %s;"
    else:
        sql = "UPDATE Drone SET Etat = 'Reserve' WHERE Id_Drone = %s;"
    cursor.execute(sql, param)
    cnx.commit()
    cnx.close()

def haveResaData(idp):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary = True)
    sql = "SELECT Id_Drone FROM Reservation WHERE Id_Colis = %s;"
    param = (idp,)
    cursor.execute(sql, param)
    idDroneR = cursor.fetchall()
    cnx.close()
    return idDroneR

def Affichage_Reservation():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT Nom,Prenom,Entreprise,Adresse_Destination,Reservation.Id_Colis,Masse_Colis, Id_Drone FROM colis_personne JOIN Reservation ON colis_personne.Id_Colis=Reservation.Id_Colis;"
    cursor.execute(sql)
    dicoResa = cursor.fetchall()
    cnx.close()
    return dicoResa

def get_waitingPackageData():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT Prenom, Nom, Entreprise , Masse_Colis, Adresse_Destination, Id_Colis FROM colis JOIN Client ON Client.Id_Personne=Colis.Id_Expediteur JOIN Personne ON Personne.Id_Personne=Colis.Id_Expediteur WHERE Etat_Colis = 'En attente';"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnx.close()
    msg = 'ok'
    return msg, res

def addResaData(idDroneS, idColis, login):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "SELECT Id_Personne FROM Employe WHERE login = %s;"
    param = (login,)
    cursor.execute(sql, param)
    idPersonne = cursor.fetchall()[0][0]
    sql1 = "INSERT INTO Reservation(Id_Colis, Id_Drone, Id_Personne) VALUES (%s,%s,%s);"
    param1 = (idColis, idDroneS, idPersonne)
    cursor.execute(sql1, param1)
    sql2 =  "INSERT INTO Livraison(Id_Colis, Id_Drone, Etat_livraison) VALUES (%s,%s,'En attente');"
    param2 = (idColis,idDroneS)
    cursor.execute(sql2, param2)
    cnx.commit()
    cnx.close()
    msg = 'ok'
    return msg

def ShowDroneData(Masse):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary = True)
    sql = "SELECT Id_Drone, Nom_Type, Etat FROM Drone JOIN Type ON Drone.Id_Type=Type.Id_Type WHERE Masse_Max>%s AND (Etat='Libre' OR Etat='En livraison') ORDER BY Heure_Dispo;"
    param = (Masse,)
    cursor.execute(sql, param)
    Drone = cursor.fetchall()
    drone_propose = Drone[0:3] #retourne des tuples contenant (Id_Drone, Etat)
    cnx.close()
    return drone_propose

def addPerson(Nom, Prenom, login, mdp, service):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "INSERT INTO Personne(Nom, Prenom) VALUES (%s,%s);"
    param = (Nom, Prenom)
    cursor.execute(sql, param)
    sql2 = "SELECT Id_Personne FROM Personne WHERE Nom = %s AND Prenom = %s;"
    cursor.execute(sql2, param)
    Id_Personne = cursor.fetchall()[0][0] #Premiere ligne/premiere colonne du resultat de la requete sql2
    sql3 = "INSERT INTO Employe(Id_Personne, login, mdp, service) VALUES (%s,%s,%s,%s);"
    param3 = (Id_Personne, login, mdp, service)
    cursor.execute(sql3, param3)
    cnx.commit()
    cnx.close()
    msg = "Employé ajouté avec succès !"
    return msg

def addColisData(nom_expediteur, prenom_expediteur, entreprise, nom_destinataire, prenom_destinataire, adresse_destination, masse_colis):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "SELECT Client.Id_Personne FROM Client JOIN Personne ON Client.Id_Personne=Personne.Id_Personne WHERE Personne.nom=%s AND Personne.prenom=%s;"
    param = (nom_expediteur,prenom_expediteur)
    cursor.execute(sql,param)
    id_exp = cursor.fetchall()
    if id_exp == []:
        sql1 = "INSERT INTO Personne(Nom,Prenom) VALUES (%s,%s);"
        cursor.execute(sql1,param)
        sql2 = "SELECT Id_Personne FROM Personne WHERE nom = %s and prenom = %s;"
        cursor.execute(sql2, param)
        id_exp = cursor.fetchall()[0][0]
        sql3 = "INSERT INTO Client(Id_Personne,Entreprise) VALUES (%s,%s);"
        param3 = (id_exp, entreprise)
        cursor.execute(sql3,param3)
    else :
        id_exp = id_exp[0][0]
    sql4 = "SELECT Id_Personne from Personne WHERE Nom = %s AND Prenom = %s;"
    param4 = (nom_destinataire, prenom_destinataire)
    cursor.execute(sql4, param4)
    Id_Destinataire = cursor.fetchall()
    if Id_Destinataire == []:
        param5 = (nom_destinataire,prenom_destinataire)
        sql5 = "INSERT INTO Personne(Nom,Prenom) VALUES (%s,%s);"
        cursor.execute(sql5,param5)
        sql6 = "SELECT Id_Personne FROM Personne WHERE nom = %s and prenom = %s;"
        cursor.execute(sql6, param5)
        Id_Destinataire = cursor.fetchall()
    Id_Destinataire = Id_Destinataire[0][0]
    sql7 = "INSERT INTO colis(Etat_Colis, Masse_Colis, Id_Expediteur, Adresse_Destination, Id_Destinataire) VALUES (%s,%s,%s,%s,%s);"
    param7 = ('En attente', masse_colis, id_exp, adresse_destination, Id_Destinataire)
    cursor.execute(sql7, param7)
    cnx.commit()
    cnx.close()
    msg = "Colis ajouté avec succès !"
    return msg

def verifAuthData(login, mdp):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM Employe WHERE login=%s and mdp=%s"
        param = (login, mdp)
        cursor.execute(sql, param)
        empl = cursor.fetchone()
        sql2 = 'SELECT Nom, Prenom FROM Personne WHERE Id_Personne = %s LIMIT 1;'
        id = empl['Id_Personne']
        param2=(id,)
        cursor.execute(sql2,param2)
        pers = cursor.fetchone()
        cnx.close()
        msg = "okAuth"
        return msg, empl, pers
    except Exception as err:
        res = None
        msg = "Failed authentification : {}".format(err)
        cnx.close()
        return msg, '', ''

def addCommentData(nom,email,msg):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        sql = "INSERT INTO Nous_Contacter(Nom, Email, Message) VALUES (%s,%s,%s);"
        param = (nom,email,msg)
        cursor.execute(sql, param)
        res = "okComment"
        cnx.commit()
    except Exception as err:
        res = "erreur"
        cnx.rollback()
    cnx.close()
    return res

def addNewsletterData(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        sql = "INSERT INTO Newsletter(Email) VALUES (%s);"
        param = (email,)
        cursor.execute(sql, param)
        res = "okNewsletter"
        cnx.commit()
    except Exception as err:
        res = "erreur"
        cnx.rollback()
    cnx.close()
    return res

def changeMdpData(newmdp, oldmdp, login):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        sql = "SELECT mdp FROM Employe WHERE login=%s"
        param = (oldmdp,)
        cursor.execute(sql, param)
        mdpbase = cursor.fetchone()
        if mdpbase == oldmdp:
            sql2 = "UPDATE Employe SET mdp=%s WHERE login=%s;"
            param2 = (newmdp,login)
            cursor.execute(sql2, param2)
            res = "okMdp"
            cnx.commit()
        else:
            res = "erreur"
    except Exception as err:
        res = "erreur"
        cnx.rollback()
    cnx.close()
    return res

def deleteColisData(idColis):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "DELETE FROM Colis WHERE Id_Colis = %s;"
    param = (idColis,)
    cursor.execute(sql, param)
    cnx.commit()
    cnx.close()
    msg = "ok"
    return msg

def getContact():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * FROM Nous_Contacter;"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnx.close()
    return res

def sendResData(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        sql = "UPDATE Nous_Contacter SET Etat='repondu' WHERE Id_Message = %s;"
        param = (id,)
        cursor.execute(sql,param)
        cnx.commit()
        res = "okContact"
    except Exception:
        res = "erreur"
        cnx.rollback()
    cnx.close()
    return res

def sendNews(objet, html):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "SELECT Email FROM Newsletter;"
    cursor.execute(sql)
    emails = cursor.fetchall()
    cnx.close()
    for email in emails:
        mailing(objet, html, email[0], "Newsletter")

def get_delivery():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT Prenom, Nom, Entreprise, Adresse_Destination, Etat_Livraison, Livraison.Id_Drone, Nom_Type, Colis.Id_Colis, Etat, Heure_Dispo FROM Colis JOIN Client ON Colis.Id_Expediteur=Client.Id_Personne JOIN Personne ON Client.Id_Personne=Personne.Id_Personne JOIN Livraison ON Livraison.Id_Colis=Colis.Id_Colis JOIN Drone ON Drone.Id_Drone=Livraison.Id_Drone JOIN Type ON Drone.Id_Type=Type.Id_Type;"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnx.close()
    for colis in res:
        dist=drone.calcul_distance("7 avenue Edouard Belin TOULOUSE 31400", colis['Adresse_Destination'])
        km = dist//1000
        if km == 0:
            colis['Distance']=str(dist)+" m"
        else:
            m = dist%1000
            colis['Distance']=str(km)+","+str(m)+" km"
    return res

def validLivData(Id_Colis):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try :
        sql1 = "SELECT Id_Drone FROM Reservation WHERE Id_Colis=%s ;"
        param1 = (Id_Colis,)
        cursor.execute(sql1, param1)
        Id_Drone = cursor.fetchall()[0][0]
        sql7 = "SELECT Adresse_Destination FROM Colis WHERE Id_Colis=%s ;"
        cursor.execute(sql7, (Id_Colis,))
        ad = cursor.fetchall()[0][0]
        (ha_est,temps) = drone.heure_retour_estim(ad)
        temps/=3600
        sql2 = "UPDATE Drone SET Etat='En livraison', Heure_Dispo=%s, Heure_vol = Heure_vol+%s WHERE Id_Drone=%s ;"
        param2 = (ha_est,temps, Id_Drone)
        cursor.execute(sql2, param2)
        sql4 = "UPDATE Livraison SET Etat_Livraison='En livraison' WHERE Id_Colis = %s;"
        param4 = (Id_Colis,)
        cursor.execute(sql4, param4)
        sql5 = "DELETE FROM Reservation WHERE Id_Colis=%s ;"
        cursor.execute(sql5, param4)
        sql6 = "UPDATE Colis SET Etat_Colis='En livraison' WHERE Id_Colis=%s ;"
        param6 = (Id_Colis,)
        cursor.execute(sql6, param6)
        cnx.commit()
        msg = "ok"
    except Exception as e:
        msg = "erreur"
        cnx.rollback()
    cnx.close()
    return msg

def deleteLivData(idcolis,iddrone):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    try:
        sql = "DELETE FROM Livraison WHERE Id_Colis = %s;"
        param = (idcolis,)
        sql1 = "UPDATE Drone SET Etat='En maintenance' WHERE Id_Drone=%s;"
        param1 = (iddrone,)
        cursor.execute(sql1, param1)
        cursor.execute(sql,param)
        sql2 = "DELETE FROM Reservation WHERE Id_Colis = %s;"
        cursor.execute(sql2,param)
        cnx.commit()
        msg = "ok"
    except Exception as e:
        msg = "erreur"
        cnx.rollback()
    cnx.close()
    return msg

def get_maintenance():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT Id_Drone, Nom_Type FROM Drone JOIN Type ON Type.Id_Type=Drone.Id_Type WHERE Etat ='En maintenance';"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnx.close()
    return res

def maintenance(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    try :
        sql = "UPDATE Drone SET Etat='Libre',nb_maintenance=nb_maintenance+1 WHERE Id_Drone=%s;"
        param = (id,)
        cursor.execute(sql,param)
        cnx.commit()
        msg = 'ok'
    except Exception as e:
        cnx.rollback()
        msg = 'erreur'
    cnx.close()
    return msg