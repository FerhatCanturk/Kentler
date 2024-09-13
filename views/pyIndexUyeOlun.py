from flask import render_template, Blueprint, redirect, current_app, session, request
import YorumIndex, SQLServer, Sifreleme, random, SessionKontrolleri
##############################################################################################################
UyeOlun = Blueprint('UyeOlun', __name__, template_folder='templates')
##############################################################################################################
@UyeOlun.route("/IndexUyeOlunGoster")
def IndexUyeOlunGoster():
    try:
        SessKontrol = SessionKontrolleri.IndexSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']   = "pyIndexUyeOlun-001"
            return redirect("/SanalYetkisiz")
        else:
            AbonePaket = YorumIndex.AbonelikPaketiSorgulari()
            SiteOwner  = current_app.config.get('BaseSabitler', {})
            if not(AbonePaket and SiteOwner):
                current_app.config['Mesaj']   = "pyIndexUyeOlun-002"
                return redirect("/SanalYetkisiz")
            else:
                return render_template("IndexUyeOlun.html", SiteOwner=SiteOwner, APaket = AbonePaket)
    except Exception as e:
        current_app.config['Mesaj']   = f"pyIndexUyeOlun-099 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@UyeOlun.route("/BtnUyelikKaydiTalepAnaliz.html", methods=["POST"])
def BtnUyelikKaydiTalepAnaliz():
    Kontrol   = False
    try:
        SessKontrol = SessionKontrolleri.IndexSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']   = "pyIndexUyeOlun-101"
            return redirect("/SanalYetkisiz")
        
        FormDurum = request.form.get("check") 
        if FormDurum is None:
            current_app.config['Mesaj1']  = "Kullanım Şartalarımızı Kabul Etmelisiniz."
            current_app.config['Mesaj2']  = "Aksi Halde Üyelik Talebiniz Kabul Edilmeyecektir"
            current_app.config['Mesaj3']  = "pyIndexUyeOlun-102"
            return redirect("/SanalStop")
        
        FormSifre1     = request.form.get("Sifre1")
        FormSifre2     = request.form.get("Sifre2")
        if FormSifre1 != FormSifre2:
            current_app.config['Mesaj1']  = "Şifreler Biirbiriyle Aynı Olmalıdır"
            current_app.config['Mesaj2']  = "Aksi Halde Üyelik Talebiniz Kabul Edilmeyecektir"
            current_app.config['Mesaj3']  = "pyIndexUyeOlun-103"
            return redirect("/SanalStop")
            
        FormAd        = request.form.get("Ad").upper().strip()
        FormAd        = FormAd[:1] + FormAd[1:].lower()
        FormSoyad     = request.form.get("Soyad").upper().strip()
        FormGSMNo     = request.form.get("GsmNo").upper().strip()
        FormMailAdres = request.form.get("MailAdres").strip()
        FormUserName  = request.form.get("UserName").strip()
        FormMailAdres = FormMailAdres.lower().strip()
        FormPaketID   = request.form.get("PaketID").upper().strip()
        SQLSorgu      = f"SELECT * FROM SKUsers WHERE RTRIM(UserMailAdress) = '{FormMailAdres}'"
        Users1        = SQLServer.Sorgula(SQLSorgu)
        ##Burada Blokaj kontrolleri yapılacak....
        Kontrol  = True 
        if not(Users1):
            # Kullanıcı Bulunamadı Yeni Kayıt Edebiliriz.
            Kontrol  = True 
        else:
            # Kullanıcı Daha Önce Varsa ????
            BlokajDurum = False 
            for User in Users1:
                if int(User["DurumID"]) == 81:
                    Aciklama    = "Talebiniz Daha Önce Red Edildi"
                    BlokajDurum = True
                    break
                elif int(User["DurumID"]) == 91:
                    Aciklama = "Blokelisiniz"
                    BlokajDurum = True
                    break
            
            if BlokajDurum:
                #Bu Mail Adresi Blokeli veya Daha Önce Red Edildi
                current_app.config['Mesaj1'] = Aciklama
                current_app.config['Mesaj2'] = "Tekrar Abone Olamazsınız"
                current_app.config['Mesaj3'] = "pyIndexUyeOlun-104"
                return redirect("/SanalStop")
            #Bu Mail Adresi Kullanılıyormu
            SQLSorgu = f"SELECT * FROM SKUsers WHERE RTRIM(UserMailAdress)='{FormMailAdres}' AND RTRIM(UserName)='{FormUserName}'"
            Users2   = SQLServer.Sorgula(SQLSorgu)
            
            if Users2:
                current_app.config['Mesaj1'] = "Mail Adres Hatası"
                current_app.config['Mesaj2'] = "Girdiğiniz Bilgiler Başka Bir Kullanıcı Tarafından Kullanılıyor"
                current_app.config['Mesaj3'] = "pyIndexUyeOlun-105"
                return redirect("/SanalStop")
            
            Kontrol  = True
        # Kontroller Bitti Kayıt İşlemlerine Geldik
        # Kontroller Bitti Kayıt İşlemlerine Geldik
        # Kontroller Bitti Kayıt İşlemlerine Geldik
        if Kontrol:
            AdiSoyadi = FormAd + " " + FormSoyad
            SQLKomut = """
            INSERT INTO SKUsers (PaketID, DurumID, AtolyeID, SqlCihazKodu, VerifyMailCode, UserAdiSoyadi, UserName, PassWord, UserGSMNumber, UserMailAdress, 
            UyelikTalepTarihi, SQLMemberDateID) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), 0)"""
            FormSifre1 = Sifreleme.Sifrele(FormSifre1)
            VFM        = random.randint(100000, 999999)
            SQLParams = (FormPaketID, 21, 0, 'Tanımsız', VFM, AdiSoyadi, FormUserName, FormSifre1, FormGSMNo, FormMailAdres)
            SQLCevap   = SQLServer.Calistir(SQLKomut, SQLParams)
            if SQLCevap:
                current_app.config['Mesaj']   = f"pyIndexUyeOlun-106"
                return redirect("/SanalError")
            
            current_app.config['Mesaj1'] = "Teşekkür Ederiz"
            current_app.config['Mesaj2'] = "Üyelik Talebiniz Kayıt Altına Alınmıştır"
            current_app.config['Mesaj3'] = "Ödeme Dekontunu Paylaşmanız Ardından Giriş İçin Kullanacağınız Bilgiler Tarafınızla Paylaşılacaktır."
            return redirect("/SanalOK")  
    except Exception as e:
        current_app.config['Mesaj']   = F"pyIndexUyeOlun-199{e}"
        return redirect("/SanalError")     
##############################################################################################################
