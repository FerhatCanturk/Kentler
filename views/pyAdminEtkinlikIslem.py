from flask import render_template, Blueprint, redirect, current_app, request
import SQLServer, SQLToBase64, SessionKontrolleri
from werkzeug.utils import secure_filename
import mimetypes
from DataBaseConfig import DATABASE_CONFIG
##############################################################################################################
Etkinlik = Blueprint('Etkinlik', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@Etkinlik.route("/AdmEtkinlikler")
def ADM_ETKINLIK_00():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminEtkinlik-001"
            return redirect("/SanalYetkisiz")
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        Social    = "SELECT * FROM SKSocial ORDER BY Tarih DESC"
        Social    = SQLServer.Sorgula(Social)
        Social    = SQLToBase64.Resim(Social)
        
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not(SiteOwner):
            current_app.config['Mesaj1']    = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2']    = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3']    = "pyAdminEtkinlik-002"
            return redirect("/SanalStop")  
        
        return render_template('AdmEtkinlikler.html', SiteOwner = SiteOwner, Social = Social)
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminEtkinlik-099 ({e})"
        return redirect("/SanalError")    
##############################################################################################################
@Etkinlik.route("/YeniEtkinlikKaydet", methods=['POST'])
def ADM_ETKINLIK_01():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminEtkinlik-101"
            return redirect("/SanalYetkisiz")

        Tarih = request.form.get("EtkinlikTarih1")
        Baslik = request.form.get("EtkinlikBaslik1")
        Aciklama = request.form.get("EtkinlikAciklama1")
        file = request.files.get('file')

        if not file or file.filename == '':
            current_app.config['Mesaj'] = "pyAdminEtkinlik-102"
            return redirect("/SanalYetkisiz")
        
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        
        if file_ext not in allowed_extensions:
            current_app.config['Mesaj'] = "pyAdminEtkinlik-103"
            return redirect("/SanalYetkisiz")
        
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
            current_app.config['Mesaj'] = "pyAdminEtkinlik-104"
            return redirect("/SanalYetkisiz")

        file_data = file.read()

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = "INSERT INTO SKSocial (Tarih, Baslik, Aciklama, Picture) VALUES (?, ?, ?, ?)"
        SQLCevap = SQLServer.Calistir(SQLKomut, (Tarih, Baslik, Aciklama, file_data))
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Etkinkik Kayıt İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminEtkinlik-105"
            return redirect("/SanalStop")
        
        return redirect("/AdmEtkinlikler")

    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminEtkinlik-199 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@Etkinlik.route("/EtkinlikSilme/<string:SocialID>", methods=['POST'])
def ADM_ETKINLIK_02(SocialID):
    try:
        # Oturum kontrolü
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminEtkinlik-201"
            return redirect("/SanalYetkisiz")
        
        SocialID = int(SocialID)
        # SocialID'yi doğrula
        if SocialID <= 0:
            current_app.config['Mesaj'] = "pyAdminEtkinlik-202"
            return redirect("/SanalYetkisiz")

        # SQL sorgusunu parametreli sorgu ile çalıştır
        SQLKomut = "DELETE FROM SKSocial WHERE SocialID = ?"
        SQLCevap = SQLServer.Calistir(SQLKomut, (SocialID,))
        
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi."
            current_app.config['Mesaj2'] = "Etkinlik Silme İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminEtkinlik-203"
            return redirect("/SanalStop")
        
        return redirect("/AdmEtkinlikler")

    except Exception as e:
        # Hata yönetimi
        current_app.config['Mesaj'] = f"pyAdminEtkinlik-299 ({e})"
        return redirect("/SanalError")
##############################################################################################################