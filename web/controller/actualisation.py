from ..data.bdd import config
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
##format d'une date en datetime aaaa-mm-jj hh:mm:ss
def actualisation():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    h_now=str(datetime.now())
    sql = "SELECT Id_Drone FROM Drone WHERE Heure_Dispo<%s ;"
    param = (h_now,)
    cursor.execute(sql, param)
    Drone=cursor.fetchall()
    for elt in Drone:
        id_drone=elt[0]
        sql1 = "SELECT Id_Colis FROM Livraison WHERE Id_Drone=%s ;"
        param1 = (id_drone,)
        cursor.execute(sql1, param1)
        Id_Colis = cursor.fetchall()[0][0]
        sql6 = "SELECT Etat FROM Drone WHERE Id_Drone=%s ;"
        cursor.execute(sql6,param1)
        Etat =  cursor.fetchall()[0][0]
        if Etat == 'En livraison':
            sql2= "UPDATE Drone SET Heure_Dispo=NULL, Etat='Libre' WHERE Id_Drone=%s"
            cursor.execute(sql2,param1)
        else:
            sql2 = "UPDATE Drone SET Heure_Dispo=NULL, Etat='Reserve' WHERE Id_Drone=%s"
            cursor.execute(sql2, param1)
        sql3= "UPDATE Colis SET Etat_Colis='Livré' WHERE Id_Colis=%s"
        param3 = (Id_Colis,)
        cursor.execute(sql3,param3)
        sql4 = "UPDATE Livraison SET Etat_Livraison='Terminé' WHERE Id_Colis=%s"
        cursor.execute(sql4,param3)
    cnx.commit()
    cnx.close()
    return None