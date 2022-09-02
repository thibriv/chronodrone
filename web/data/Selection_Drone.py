from bdd import config
import mysql.connector

def selection_drone(Masse,nb_drone):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "SELECT Id_Drone,Etat FROM Drone JOIN Type ON Drone.Id_Type=Type.Id_Type WHERE Masse_Max>=%s AND (Etat='Libre' OR Etat='En livraison') ORDER BY Heure_Dispo;"
    param = (Masse,)
    cursor.execute(sql, param)
    Drone = cursor.fetchall()
    cnx.commit()
    cnx.close()
    return Drone[0:int(nb_drone)] #retourne des tuples contenant (Id_Drone, Etat)
