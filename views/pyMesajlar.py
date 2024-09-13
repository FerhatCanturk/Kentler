from flask import render_template, Blueprint, current_app, session
##############################################################################################################
Messages = Blueprint('Messages', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@Messages.route("/SanalError")
def SanalError():
     M1 = current_app.config.get('Mesaj', '')
     return render_template("MsgError1.html", Mesaj = M1)
##############################################################################################################
@Messages.route("/SanalStop")
def SanalStop():
     M1 = current_app.config.get('Mesaj1', '')
     M2 = current_app.config.get('Mesaj2', '')
     M3 = current_app.config.get('Mesaj3', '')
     return render_template("MsgStop3.html", Mesaj1 = M1, Mesaj2 = M2, Mesaj3 = M3)
##############################################################################################################
@Messages.route("/SanalYetkisiz")
def SanalYetkisiz():
     M1 = current_app.config.get('Mesaj', '')
     session.clear()
     return render_template("MsgYetkisiz1.html", Mesaj = M1)
##############################################################################################################
@Messages.route("/SanalOK")
def SanalOKSayfasi():
     M1 = current_app.config.get('Mesaj1', '')
     M2 = current_app.config.get('Mesaj2', '')
     M3 = current_app.config.get('Mesaj3', '')
     return render_template("MsgOK.html", Mesaj1 = M1, Mesaj2 = M2, Mesaj3 = M3)
##############################################################################################################
