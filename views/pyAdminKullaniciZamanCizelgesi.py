from flask import render_template, Blueprint, redirect, current_app, session
import YorumAdminKullaniciZamanCizelgesi, SessionKontrolleri
##############################################################################################################
AdmUserDetaySayfasi = Blueprint('AdmUserDetaySayfasi', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@AdmUserDetaySayfasi.route("/AdmUserDetail", methods=["GET"])
def ADM_USERCIZELGE_00():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullaniciZamanCizelgesi-001"
            return redirect("/SanalYetkisiz")
        
        UserID            = session.get('UserID')
        User              = YorumAdminKullaniciZamanCizelgesi.KullaniciSorgusu(UserID)
        AboneTarihDetails = YorumAdminKullaniciZamanCizelgesi.AboneSorgusu(UserID)          
        SiteOwner = current_app.config.get('BaseSabitler', {})

        if not SiteOwner or not(AboneTarihDetails) or not(User):
            current_app.config['Mesaj1']    = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2']    = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3']    = "pyAdminKullaniciZamanCizelgesi-002"
            return redirect("/SanalStop") 
        
        return render_template("AdmKullaniciDetay.html", SiteOwner = SiteOwner, 
            User = User, AboneTarihDetails = AboneTarihDetails)
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminKullaniciZamanCizelgesi-099 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
