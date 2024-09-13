from flask import render_template, Blueprint, redirect, current_app, session, request
import SQLServer, mail_sender, SiteSabit, SessionKontrolleri
##############################################################################################################
AdmMessages = Blueprint('AdmMessages', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@AdmMessages.route("/AdmMessages")
def SANALMODELACMA():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminMessages-001"
            return redirect("/SanalYetkisiz")
        
        Messages  = SQLServer.Sorgula("SELECT * FROM SKMessage ORDER BY CevapDurum, MessageTarih, MessageID DESC")
        SiteOwner = current_app.config.get('BaseSabitler', {})
        
        if not SiteOwner:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyAdminMessages-002"
            return redirect("/SanalStop")  
    
        return render_template("/AdmMessages.html", SiteOwner = SiteOwner, 
                               Messages = Messages)
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminMessages-099 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmMessages.route("/MesajCevap/<string:MessageID>", methods=["POST"])
def CevapGonder(MessageID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminMessages-101"
            return redirect("/SanalYetkisiz")
        
        Cevap  = request.form.get('Cevap')
        MessageID = int(MessageID)
        if not Cevap or MessageID <= 0:
            current_app.config['Mesaj'] = "pyAdminMessages-102"
            return redirect("/SanalYetkisiz")
        
        SQLKomut = "SELECT * FROM SKMessage WHERE MessageID = ?"
        Mesajlar = SQLServer.Sorgula(SQLKomut, (MessageID, ))
        if not(Mesajlar):
                current_app.config['Mesaj'] = "pyAdminMessages-103"
                return redirect("/SanalYetkisiz")
        
        AdminMail     = session.get('AdminMail').strip()
        if not(AdminMail):
            current_app.config['Mesaj'] = "pyAdminMessages-104"
            return redirect("/SanalYetkisiz")
        
        MesajDurumu = int(Mesajlar[0]['CevapDurum'])
        CevapTarih  = Mesajlar[0]['CevapTarih']
        if not(MesajDurumu == 0) or not CevapTarih:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel  Hata Meydana Geldi"
            current_app.config['Mesaj2'] = f"Kullanıcıya Bu Mesaj İçin Daha Önce Cevap Verilmiştir. ({CevapTarih})"
            current_app.config['Mesaj3'] = "pyAdminMessages-105"
            return redirect("/SanalStop")
        
        UserMail    = Mesajlar[0]["MailAdres"]
        AdSoyad     = Mesajlar[0]["AdSoyad"]
        MesajKonusu = f"Sayın: {AdSoyad}"
               
        Cevap       = f"""Serap KOÇAK Web Sayfamızdan {Mesajlar[0]['MessageTarih'].strftime("%d-%m-%Y")} 
                    tarihli tarafımıza gönderdiğiniz mesajın cevabıdır...\n\n{Cevap}"""
        MailDurum   = mail_sender.MailGonderme(UserMail, MesajKonusu, Cevap)
        if not MailDurum:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2'] = f"Kullanıcının ({Mesajlar[0]['MailAdres']}) Mail Adresine Bilgilendirilme eMail'i Gönderilemedi."
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-106"
            return redirect("/SanalStop")
        
        SQLKomut = "UPDATE SKMessage SET CevapDurum = ?, Cevap=?, CevapTarih = GETDATE() WHERE MessageID = ?"
        Params   = (1, Cevap, MessageID)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Kullanıcıya Mail Gönderildi. Ancak Bekleyen Mesajlarınızdan Gönderilmiş Olarak İşaretlenemedi."
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-107"
            return redirect("/SanalStop")
        
        SQLWebSabit = "UPDATE SkWebSabitler SET Sutun13 = COALESCE((SELECT COUNT(*) FROM SKMessage WHERE CevapDurum=0), 0)"
        SQLCevap    = SQLServer.Calistir(SQLWebSabit)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Kullanıcıya Mail Gönderildi. Ancak Bekleyen Mesajlarınızdan Gönderilmiş Olarak İşaretlenemedi."
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-108"
            return redirect("/SanalStop")
    
        current_app.config['BaseSabitler'] = []
        current_app.config['BaseSabitler'] = SiteSabit.Sabitler()
        return redirect("/AdmMessages")
    
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminMessages-199 ({e})"
        return redirect("/SanalError")     
##############################################################################################################