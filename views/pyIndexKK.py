from flask import render_template, Blueprint, redirect, current_app
from YorumIndex import AbonelikPaketiSorgulari
import SessionKontrolleri
##############################################################################################################
IndexKK = Blueprint('IndexKK', __name__, template_folder = 'templates')
##############################################################################################################
##############################################################################################################
@IndexKK.route("/IndexKKGoster")
def IndexKKGosterme():
    try:
        SessKontrol = SessionKontrolleri.IndexSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyIndexKK-001"
            return redirect("/SanalYetkisiz")
        
        APaket    = AbonelikPaketiSorgulari()
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not (SiteOwner):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyIndexKK-002"
            return redirect("/SanalStop")
        
        return render_template('IndexKullanimSartlari.html', SiteOwner = SiteOwner, APaket = APaket)
    except Exception as e:
        current_app.config['Mesaj']  = f"pyIndexKK-099 ({e})"
        return redirect("/SanalError")
##############################################################################################################
