from flask import Flask, render_template ,url_for,request,redirect,flash
import psycopg2 as psy 
import datetime

#On donne ensuite un nom à l’application ici ce sera app
app = Flask(__name__)
app.secret_key = "flash message"



def connectionDB():
    try:
        #connection a la base de donnee
        connection=psy.connect(host= "localhost",
                                database="sonatel7",
                                user="postgres",
                                password="ngagne03",
                                port ="5432"
                            )
        return connection
    except (Exception) as error:
        print(" PROBLE;E DE CONNECTION AU SERVEUR ",error)
connection=connectionDB()
curseur=connection.cursor()
#@app.route permet de préciser à quelle adresse ce qui suit va s’appliquer
@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/accueil')
def fondconnect():
    return render_template('con1.html')


@app.route('/')
def deconnect():
    return render_template('con1.html')

@app.route('/utilisateur' , methods=['GET','POST'])
def connect():
    if request.method == "POST":
        details = request.form
        username=details['username']
        password=details['password']
        curseur.execute("SELECT * from utilisateur WHERE username='"+ username +"' and password = '"+ password +"'  ")
        user=curseur.fetchone()
        if user is None:
            return " password incorrect"
        else:
            return render_template('fond.html')
            



@app.route('/inscription')
def kha():
    curseur.execute("SELECT *FROM promotion")
    promo=curseur.fetchall()
    requete_liste_matricule = "SELECT max(id_ap) FROM apprenant2"
    curseur.execute(requete_liste_matricule)
    result_matricule = curseur.fetchall()
    for mat in result_matricule:                
        matricule=mat[0]
    

    if matricule == None:
        num=1
        val='-'+str(num)
        naf = "SA"+val
    else:
        num=matricule+1
        val='-'+str(num)
        naf="SA"+val
    return render_template('inscription.html',n=promo,naf=naf)



@app.route('/inscription', methods=['GET','POST'])
def inscription():
    curseur.execute("SELECT pseudo FROM apprenant2")
    do=curseur.fetchall()
    if request.method == "POST":
        details = request.form
        matricule =details['matricule']
        pseudo= details['pseudo']
        nom_ap = details['nom_ap']
        prenom_ap = details['prenom_ap']
        date_nais= details['date_nais']
        statu= details['statu']
        sexe_ap= details['sexe_ap']
        control=False
        for i in do:
            if i[0]==pseudo:
                control=True
                break
            if control==True:
                flash("apprenant existe deja")
                return render_template('inscription.html',i=do)
            else:
                requete_ajout_ap="INSERT INTO apprenant2(matricule,pseudo,nom_ap,prenom_ap,date_nais,sexe_ap,statu) VALUES (  %s, %s, %s, %s,%s, %s,%s)"
                curseur.execute(requete_ajout_ap,(matricule,pseudo,nom_ap,prenom_ap,date_nais,sexe_ap,statu))
                connection.commit()
                flash("inscrit avc succe")
                return render_template('inscription.html')
    return render_template('inscription.html')
        
        
    




# -----------------------------SCOLARITE------------------------------
# ------------------LIST---DES-----APPRENANTS--------------------------
@app.route('/listapp', methods=['GET','POST'])
def listapp():
    curseur.execute("SELECT *FROM apprenant2")
    lister1=curseur.fetchall()   
    return render_template('listapp.html',l1=lister1)
# -----------------------UPDATE-APPRENANT----------------------

@app.route('/modifap2', methods = ['POST', 'GET'])
def modifap2():
    
    
    curseur.execute("SELECT *FROM promotion")
    lister2=curseur.fetchall()
    curseur.execute("SELECT apprenant2.id_ap,apprenant2.pseudo,apprenant2.nom_ap,apprenant2.prenom_ap,apprenant2.date_nais,apprenant2.statu,apprenant2.sexe_ap,promotion.nom_promo FROM apprenant2,promotion ")
    lister1=curseur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        id_ap=details['id_ap']
        pseudo= details['pseudo']
        nom_ap = details['nom_ap']
        prenom_ap = details['prenom_ap']
        date_nais= details['date_nais']
        statu= details['statu']
        sexe_ap= details['sexe_ap']
        id_promo= int(details['id_promo'])
        curseur.execute("""
        UPDATE apprenant2
        SET nom_ap=%s,pseudo=%s, prenom_ap=%s,date_nais=%s,statu=%s,sexe_ap=%s,id_promo=%s   
        WHERE id_ap=%s 
        """,(pseudo,nom_ap,prenom_ap,date_nais,statu,sexe_ap,id_promo,id_ap))
        curseur.execute("SELECT apprenant2.id_ap,apprenant2.pseudo,apprenant2.nom_ap,apprenant2.prenom_ap,apprenant2.date_nais,apprenant2.statu,apprenant2.sexe_ap,promotion.nom_promo FROM apprenant2,promotion ")  
        lister11=curseur.fetchall()
        
        connection.commit()
        return render_template('modifap2.html',l1=lister11,l2=lister2)
    return render_template('modifap2.html',l1=lister1,l2=lister2)

#----------------annuler apprenant---------------------

@app.route('/listapan')
def listapan():
    

    curseur.execute("SELECT apprenant2.id_ap,apprenant2.pseudo,apprenant2.nom_ap,apprenant2.prenom_ap,apprenant2.date_nais,apprenant2.statu,apprenant2.sexe_ap,promotion.nom_promo FROM apprenant2,promotion where statu='inscrit' ")
    lister1=curseur.fetchall()
    return render_template('anulap.html',l1=lister1)



# ---------------------------------------------
@app.route('/anulap/<string:id_data>', methods = ['POST', 'GET'])
def anulap(id_data):
    flash("Data annuler Successfully")
    curseur.execute("""UPDATE apprenant2 SET statu='annuler'WHERE id_ap=%s""",(id_data))
    connection.commit()
    return redirect(url_for('listapan'))
#---------------------suspendre Apprenant-----------------------

#-------------------------------------

@app.route('/listapsus')
def listapsus():
    

    curseur.execute("SELECT apprenant2.id_ap,apprenant2.pseudo,apprenant2.nom_ap,apprenant2.prenom_ap,apprenant2.date_nais,apprenant2.statu,apprenant2.sexe_ap,promotion.nom_promo FROM apprenant2,promotion where statu='inscrit' ")
    lister1=curseur.fetchall()
    return render_template('suspenap.html',l1=lister1)
# ------------------------------------------------------------------------------------------------------
@app.route('/suspenqp/<string:id_data>', methods = ['POST', 'GET'])
def suspenap(id_data):
    flash("Data annuler Successfully")
    
    curseur.execute(""" UPDATE apprenant2 SET statu='suspend' WHERE id_ap=%s""",(id_data))
    connection.commit()
    return redirect(url_for('suspenap'))


# -----------------------UPDATE-reference-----------------------------------------


#------------reference--------------------------------------------------------------------
#--------insertion----------------------------

@app.route('/nouveauref', methods=['GET','POST'])
def nouveauref():
    if request.method == "POST":
        details = request.form
        nom_ref = details['nom_ref']
        requete_ajout_ref="INSERT INTO referentiel(nom_ref) VALUES (%s)"
        curseur.execute(requete_ajout_ref,(nom_ref,))
        connection.commit()
    return render_template('newref.html')

#------------list ref--------------------

@app.route('/listref', methods=['GET','POST'])
def listreferentiel():
    curseur.execute("SELECT *FROM referentiel")
    listrefe=curseur.fetchall()
    return render_template('listref.html',referentiel=listrefe)


#------------update ref---------------------------
@app.route('/modifref', methods = ['POST', 'GET'])
def modifref():
    curseur.execute("SELECT *FROM referentiel")
    listrefe=curseur.fetchall()
    if request.method == 'POST':
            details = request.form
            id_ref =details['id_ref']
            nom_ref =details['nom_ref']
            curseur.execute("""
            
            UPDATE referentiel
            SET nom_ref=%s 
            WHERE id_ref=%s

            """, (nom_ref, id_ref))
            connection.commit()
            curseur.execute("SELECT *FROM referentiel")
            listrefe1=curseur.fetchall()
            return render_template('modifref.html', referentiel=listrefe1)
    return render_template('modifref.html', referentiel=listrefe)

#---------------promo--------------------------
#----------------------insertion-----------------
@app.route('/nouveaupromo',methods=['GET','POST'])
def nouveaupromo():
    curseur.execute("SELECT id_ref ,nom_ref FROM referentiel")
    promo=curseur.fetchall()
    if request.method == "POST":
        details = request.form
        nom_promo = details['nom_promo']
        date_deb = details['date_deb']
        date_fin = details['date_fin']
        id_ref=int(details['referentiel'])
        requete_ajout_promo="INSERT INTO promotion(nom_promo,date_deb,date_fin,id_ref) VALUES ( %s,%s, %s,%s)"
        curseur.execute(requete_ajout_promo,(nom_promo,date_deb,date_fin,id_ref))
        connection.commit()
    return render_template('newpromo.html',n = promo)
#----------------------listpromo-------------------

@app.route('/listpromo', methods=['GET','POST'])
def listpromo():
    curseur.execute("SELECT id_promo,nom_promo,date_deb,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref")
    listpro=curseur.fetchall()
    return render_template('listpromo.html',promotion=listpro)

@app.route('/listapp1', methods=['GET','POST'])
def listapp1():
    curseur.execute("SELECT *FROM apprenant2")
    ap1=curseur.fetchall()
    return render_template('listapp1.html',ap2=ap1)

#---------------update--------------------------------
@app.route('/modifpromo',  methods=['GET','POST'])
def modifpromo():
    curseur.execute("SELECT *FROM referentiel")
    ref=curseur.fetchall()

    curseur.execute("SELECT id_promo,nom_promo,date_deb,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref ")
    listpro=curseur.fetchall()

    if request.method == 'POST':
            details = request.form
            id_promo =details['id_promo']
            nom_promo =details['nom_promo']
            date_deb =details['date_deb']
            date_fin =details['date_fin']
            id_ref =details['id_ref']
            curseur.execute("""
            
            UPDATE promotion
            SET nom_promo=%s, 
            date_deb=%s, 
            date_fin=%s,
            id_ref=%s
            WHERE id_promo=%s

            """, (nom_promo, date_deb,date_fin,id_ref,id_promo))
           

            curseur.execute("SELECT id_promo,nom_promo,date_deb,date_fin,nom_ref FROM referentiel, promotion WHERE referentiel.id_ref=promotion.id_ref")
            listpro1=curseur.fetchall()
            connection.commit()
            return render_template('modifpromo.html',referentiel=ref,promotion=listpro1)    
    return render_template('modifpromo.html',referentiel=ref,promotion=listpro)





#def connexion():
if __name__ == "__main__":
    app.run(debug=True, port=5000)