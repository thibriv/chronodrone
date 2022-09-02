from flask import Flask, render_template, session, request, redirect
from .controller import formulaire as f
from .controller.actualisation import actualisation
from .data import bdd as b

app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "template"
app.config.from_object("config")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/webmasters")
def webmasters():
    return render_template("webmasters.html")

@app.route("/global_view")
def global_view():
    try:
        session['login']
        actualisation()
        return render_template("global_view.html",drones=get_drone(), colis=get_Package(), livraisons=get_delivery())
    except Exception as e:
        print(e)
        return redirect("/denied")

def get_Package():
    msg, data = b.get_packageData()
    return data

@app.route("/profil")
def profil():
    try :
        session['login']
        return render_template("profil.html")
    except Exception as e:
        print(e)
        return redirect("/denied")

@app.route("/selectDrone", methods = ['POST'])
def selectDrone():
    idDroneS, idColis = f.selectADrone(request)[0], f.selectADrone(request)[1]
    addReservation(idDroneS, idColis)
    return redirect("/reservations")

@app.route("/reservations")
def reservations():
    colis, packageToDeliver, drones = get_reservation()
    try :
        if session['service'] != 'livraison':
            actualisation()
            return render_template("reservation.html", colis = colis, packageToDeliver = packageToDeliver, drones = drones)
        else:
            return redirect("/denied")
    except Exception as e:
        print(e)
        return redirect("/denied")

def addReservation(idDroneS, idColis):
    login = f.getSession()
    msg = b.addResaData(idDroneS, idColis, login)
    if msg == 'erreur':
        actualisation()
        colis, packageToDeliver, drones = get_reservation()
        return render_template('reservation.html', colis = colis, packageToDeliver = packageToDeliver, drones = drones, msg_add=msg)
    else:
        return redirect("/reservations")

def get_reservation():
    colis = b.Affichage_Reservation()
    packageToDeliverWR = get_packageToDeliver()
    drones = []
    toPop = []
    for p in packageToDeliverWR:
        idp = p['Id_Colis']
        haveResa = b.haveResaData(
            idp)  # return l'id du drone (dans une liste) associé à la resa si existe. Sinon return []
        if haveResa != []:
            toPop.append(packageToDeliverWR.index(p))
    packageToDeliverWRNew = []  # Ne contiendra que les colis qui n'ont pas encore de réservation associée
    for p in packageToDeliverWR:
        if packageToDeliverWR.index(p) not in toPop:
            packageToDeliverWRNew.append(p)
    packageToDeliverWR = packageToDeliverWRNew
    for p in packageToDeliverWR:
        masse = p["Masse_Colis"]
        drone = b.ShowDroneData(masse)
        drones.append(drone)
    return colis, packageToDeliverWR, drones

def get_waiting_package():
    msg, data = b.get_waitingPackageData()
    return data

def get_packageToDeliver():
    msg, data = b.get_waitingPackageData()
    return data

@app.route("/livraisons")
def livraisons():
    try :
        if session['service'] != 'commande':
            actualisation()
            return render_template("livraison.html", livraisons=get_delivery())
        else:
            return redirect("/denied")
    except Exception as e:
        print(e)
        return redirect("/denied")

def get_delivery():
    return b.get_delivery()

@app.route("/validLiv", methods=['POST'])
def validLiv():
    msg = f.validDelivery(request)
    if msg == 'erreur':
        return render_template("livraison.html", livraisons=get_delivery(), add = msg)
    else:
        return redirect("/livraisons")

@app.route("/delLiv", methods=['POST'])
def delLiv():
    msg = f.deleteLiv(request)
    if msg == 'erreur':
        return render_template("livraison.html", livraisons=get_delivery(), del_msg = msg)
    else:
        return redirect("/livraisons")

@app.route("/admin")
def admin():
    try :
        if session['service']=='admin':
            actualisation()
            return render_template("admin.html",personnes=get_employee(), drones=get_drone(), colis=get_Package())
        else:
            return redirect("/denied")
    except Exception as e:
        print(e)
        return redirect("/denied")

def get_employee():
    msg, data = b.get_employeeData()
    return data

def get_drone():
    msg, data = b.get_droneData()
    return data

@app.route("/denied")
def denied():
    return render_template("denied.html")

@app.route("/login_request", methods = ['POST'])
def login_request():
    msg = f.verifAuth(request)
    if msg == "erreur":
        return render_template('login.html', info = msg)
    else :
        return redirect("/global_view")

@app.route("/newPackage", methods = ['POST'])
def newPackage():
    msg = f.addPackage(request)
    if msg == "erreur":
        actualisation()
        return render_template("admin.html",personnes=get_employee(), drones=get_drone(), colis=get_Package(),msg_pack_add=msg)
    else:
        return redirect("/admin")

@app.route("/delPerson", methods = ['POST'])
def delPerson():
    msg = f.deletePeople(request)
    if msg == 'erreur':
        actualisation()
        return render_template("admin.html",personnes=get_employee(), drones=get_drone(), colis=get_Package(), del_per=msg)
    else:
        return redirect("/admin")

@app.route("/delResa", methods = ['POST'])
def delResa():
    msg = f.deleteResa(request)
    if msg == 'erreur':
        actualisation()
        colis, packageToDeliver, drones = get_reservation()
        return render_template('reservation.html', colis=colis, packageToDeliver=packageToDeliver, drones=drones, msg_del=msg)
    else:
        return redirect("/reservations")


@app.route('/newPerson', methods = ['POST'])
def newPerson():
    msg = f.addSomeone(request)
    if msg == 'erreur':
        actualisation()
        return render_template("admin.html",personnes=get_employee(), drones=get_drone(), colis=get_Package(), msg_emp=msg)
    else:
        return redirect("/admin")
@app.route('/newDrone', methods = ['POST'])
def newDrone():
    msg = f.addDrone(request)
    if msg == 'erreur':
        actualisation()
        return render_template("admin.html",personnes=get_employee(), drones=get_drone(), colis=get_Package(), msg_dro=msg)
    else:
        return redirect("/admin")

@app.route('/delDrone', methods = ['POST'])
def delDrone():
    msg = f.deleteDrone(request)
    if msg == 'erreur':
        actualisation()
        return render_template("admin.html",personnes=get_employee(), drones=get_drone(), colis=get_Package(), msg_dro=msg)
    else:
        return redirect("/admin")

@app.route('/delPackage', methods = ['POST'])
def delPackage():
    msg = f.deletePackage(request)
    if msg == 'erreur':
        actualisation()
        return render_template("admin.html",personnes=get_employee(), drones=get_drone(), colis=get_Package(), msg_pack_del=msg)
    else:
        return redirect("/admin")

@app.route('/changePassword', methods=['POST'])
def changePassword():
    msg = f.changeMdp(request)
    if msg =='erreur':
        return render_template('profil.html', msg = msg)
    else:
        return redirect('/profil')

@app.route("/lemoine")
def lemoine():
    return render_template("lemoine.html")

@app.route("/rivoalen")
def rivoalen():
    return render_template("rivoalen.html")

@app.route("/allietta")
def allietta():
    return render_template("allietta.html")

@app.route("/jouquey")
def jouquey():
    return render_template("jouquey.html")

@app.route('/addComment', methods = ['POST'])
def commentaire():
    msg = f.addComment(request)
    if msg == 'erreur':
        return render_template('index.html', comment = msg)
    else:
        return redirect("/")


@app.route('/addNewsletter', methods = ['POST'])
def addNewsletter():
    msg = f.addNewsletter(request)
    if msg == 'erreur':
        return render_template('index.html', news = msg)
    else:
        return redirect("/")

@app.route("/serviceclient")
def serviceclient():
    return render_template('service_client.html', messages = b.getContact())

@app.route("/sendRes", methods=['POST'])
def sendRes():
    mail,base = f.sendResponse(request)
    if mail == "erreur" or base == "erreur":
        return render_template("service_client.html",messages = b.getContact(), contact = "erreur")
    else:
        return redirect("/serviceclient")

@app.route("/sendNews", methods=['POST'])
def sendNews():
    mail= f.sendNews(request)
    if mail == "erreur":
        return render_template("service_client.html", newsletter = "erreur")
    else:
        return redirect("/serviceclient")

@app.route("/maintenance")
def maintenance():
    try :
        if session['service']=='admin' or session['service']=='maintenance':
            actualisation()
            return render_template("maintenance.html", drones_maintenance = get_drone_maintenance(), drones = get_drone())
        else:
            return redirect("/denied")
    except Exception as e:
        print(e)
        return redirect("/denied")

def get_drone_maintenance():
    res = b.get_maintenance()
    return res

@app.route("/maintenanceDrone", methods = ['POST'])
def maintenanceDrone():
    msg = f.maintenanceDrone(request)
    if msg == "erreur":
        return render_template("maintenance.html", msg = msg)
    else:
        return redirect("/maintenance")