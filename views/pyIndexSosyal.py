from flask import render_template, Blueprint, redirect, current_app
import SQLServer, SQLToBase64, SessionKontrolleri
##############################################################################################################
IndexSosyal = Blueprint('IndexSosyal', __name__, template_folder = 'templates')
##############################################################################################################
@IndexSosyal.route("/IndexSosyalGoster")
def SosyalGoster():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj']  = "PyIndexSosyal-001"
            return redirect("/SanalYetkisiz")
        
        Socials   = SQLServer.Sorgula("SELECT * FROM SKSocial ORDER BY Tarih DESC")
        Socials   = SQLToBase64.Resim(Socials)
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not(SiteOwner):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyIndexKK-002"
            return redirect("/SanalStop")
        
        return render_template('IndexSosyal.html', SiteOwner = SiteOwner, Socials = Socials)
    except Exception as e:
        current_app.config['Mesaj']  = "PyIndexSosyal-099"
        return redirect("/SanalError")
##############################################################################################################
