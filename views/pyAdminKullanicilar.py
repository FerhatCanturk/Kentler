from flask import render_template, Blueprint, redirect, current_app, session, request
import mail_sender, SQLServer, Sifreleme, YorumAdminKullanicilar, SessionKontrolleri
##############################################################################################################
AdmKullanicilar = Blueprint('AdmKullanici', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
##############################################################################################################
@AdmKullanicilar.route("/AdminGoster")
def ADM_KULLANICILAR_00():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-001"
            return redirect("/SanalYetkisiz")

        ClientID = session.get("ClientID")
        ClientName = session.get("ClientName")
        DurumFiltreID = session.get("DurumFiltreID")
        AdSoyadFiltre = session.get("AdSoyadFiltre")
        IlkSatirIndis = int(session.get("IlkSatirIndis", 0))
        SayfaAdim = int(session.get("SayfaAdim", 10))
        SQLKomut = "SELECT * FROM SKUsers WHERE UserID = ?"
        User     = SQLServer.Sorgula(SQLKomut, (ClientID,))
        UserData = User[0]
        if not User:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-002"
            return redirect("/SanalYetkisiz")
            
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if IlkSatirIndis < 0:
            IlkSatirIndis = 0
        session['IlkSatirIndis'] = str(IlkSatirIndis)

        ToplamUserSys = YorumAdminKullanicilar.KullaniciSayisi(DurumFiltreID)
        UsersSayfa    = YorumAdminKullanicilar.KullanicilarListesi(IlkSatirIndis, SayfaAdim, DurumFiltreID, AdSoyadFiltre, 0)
        Paketler      = YorumAdminKullanicilar.AbonelikPaketiSorgulari()
        UserBaslik    = YorumAdminKullanicilar.AboneBasliklari()

        SonSatirIndis = min(IlkSatirIndis + SayfaAdim - 1, ToplamUserSys - 1)
        Onceki = IlkSatirIndis == 0
        Sonraki = ToplamUserSys > IlkSatirIndis + len(UsersSayfa)
        
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not SiteOwner:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa yükleme hatası"
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-003"
            return redirect("/SanalStop")

        return render_template("AdmKullanicilar.html", SiteOwner=SiteOwner,
                IsAdmin = True, ClientAdi = ClientName, UsersSayfa = UsersSayfa, 
                Paketler = Paketler, UserBaslik = UserBaslik, 
                FiltreID = DurumFiltreID, FiltreAdSoyad = AdSoyadFiltre,
                Onceki = Onceki, Sonraki = Sonraki, ToplamUserSys = ToplamUserSys,
                IlkSatirIndis = IlkSatirIndis, SonSatirIndis = SonSatirIndis)
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminKullanicilar-099 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route('/AdmUyeAktifle/<string:UserID>', methods=["POST"])
def ADM_KULLANICILAR_01(UserID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-101"
            return redirect("/SanalYetkisiz")
        
        if not UserID or UserID == None:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-102"
            return redirect("/SanalYetkisiz")
        
        UserID          = int(UserID)
        PaketID         = int(request.form.get("PaketID"))
        GuncelTarih     = request.form.get("Acilis")

        if UserID <= 0 or PaketID <= 0:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-103"
            return redirect("/SanalYetkisiz")
        
        if not(GuncelTarih and PaketID > 11):
            current_app.config['Mesaj']    = "pyAdminKullanicilar-104"
            return redirect("/SanalYetkisiz")
        
        SQLKomut  = "INSERT INTO SKMemberDates (UserID, PaketID, BaslamaTarihi) VALUES  (?, ? , ?)"
        Params    = (UserID, PaketID, GuncelTarih)
        SQLDeger  = SQLServer.IdentityCalistir(SQLKomut, Params)
        if SQLDeger == 0 or SQLDeger is None:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üye Aktifleme İşlemi Yapılamadı (SKMemberDates)"
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-105"
            return redirect("/SanalStop")
        
        SQLKomut  = "UPDATE SKUsers SET SQLMemberDateID = ?, DurumID = ?, PaketID = ? WHERE UserID = ?"
        Params    = (SQLDeger, 31, PaketID, UserID)
        SQLCevap1 = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap1:
            # SKUsers'i Yazarken Hata Oluştuğu İçin MemberDate'i siliyoruz....
            SQLKomut  = "DELETE FROM SKMemberDates WHERE ID = ? AND UserID = ?"
            SQLCevap2 = SQLServer.Calistir(SQLKomut, (SQLDeger, UserID))
            if SQLCevap2:
                # MemberDate'i silemediğimizden kullanıcının bütün MemberDate Kayıtlarını Silelim....
                SQLKomut  = "DELETE FROM SKMemberDates WHERE UserID = ?"
                SQLCevap3 = SQLServer.Calistir(SQLKomut, (UserID, ))
                if SQLCevap3:
                    # Bütün Member Date'i de silemedik
                    current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
                    current_app.config['Mesaj2'] = """Ciddi Bir Hata Oluşmuştur. VeriTabanı'nızla Bağlantı Hatası veya Daha
                                                Büyük Bir Gerekçeden Dolayı Abonelik Tarihlerinin Gözden Geçirilmesinde
                                                Fayda Görülmektedir (SKUsers)"""
                    current_app.config['Mesaj3'] = "pyAdminKullanicilar-106"
                    return redirect("/SanalStop")
                
                # Bütün Member Date'i de sildik
                current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
                current_app.config['Mesaj2'] = """Üye Aktifleme İşlemi Yapılamadığığı Gibi Güvenlik
                                                Gerekçelerinden Dolayı Bütün Abonelik Tarih Aralıkları Boşaltıldı."""
                current_app.config['Mesaj3'] = "pyAdminKullanicilar-107"
                return redirect("/SanalStop")
        
            # Yeni Kayıt Edilen MemberDate'i sildik....
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üye Aktifleme İşlemi Yapılamadı (SKUsers)"
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-108"
            return redirect("/SanalStop")
        else:
            #Kullanıcıya Üyeliğiniz Açıldı Bilgisini Gönderelim...
            User        = SQLServer.Sorgula(f"SELECT * FROM SKUsers WHERE UserID={UserID}")
            Baslik      = "Serap KOÇAK Web Sitesi Bilgilendirmesi"
            MesajGovde  = f"Sayın: {User[0]['UserAdiSoyadi'].strip()}\n\n"
            MesajGovde += f"Serap KOÇAK Web Sitesine Erişiminiz İçin Site Giriş Bilgileriniz Aşağıda Sunulmuştur...\n\n\n"
            MesajGovde += f"Adınız Soyadınız: {User[0]['UserAdiSoyadi'].strip()}\n"
            MesajGovde += f"Mail Adresiniz: {User[0]['UserMailAdress'].strip()}\n"
            MesajGovde += f"Şifreniz: {Sifreleme.SifreyiCoz(User[0]['PassWord'].strip())}\n"
            MesajGovde += f"Onay Kodunuz: {User[0]['VerifyMailCode']}\n\n\n"
            MesajGovde += f"İlk Giriş Yaptığınızda Kullandığınız Cihaz Bilgileri Sistemimizde Kayıt Edilecek Olup, "
            MesajGovde += f"Tekrar sisteme başka bir cihazla giriş yaparsanız üyeliğinizin iptal edileceğini, "
            MesajGovde += f"SİTE KULLANIM KURALLARI gereğince önemle hatırlatırız."
            MailKime    = User[0]["UserMailAdress"].strip()
            MailDurum   = mail_sender.MailGonderme(MailKime, Baslik, MesajGovde)
            if not MailDurum:
                current_app.config['Mesaj1']  = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
                current_app.config['Mesaj2']  = """Üye Aktifleme İşlemi Başarıyla Yapıldı. Ancak 
                                            Kullanıcıya Bilgilendirilme eMail'i Gönderilemedi."""
                current_app.config['Mesaj3']  = "pyAdminKullanicilar-109"
                return redirect("/SanalStop")
            
            return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-199 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route(f'/AdmUyePasifle/<string:UserID>', methods=["POST"])
def ADM_KULLANICILAR_02(UserID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-201"
            return redirect("/SanalYetkisiz")
        
        if not UserID or UserID is None:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-202"
            return redirect("/SanalYetkisiz")
        
        if not UserID or UserID == None:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-203"
            return redirect("/SanalYetkisiz")
        
        UserID   = int(UserID)
        Kapanis  = str(request.form.get("Kapanis"))
        if not(Kapanis):
            current_app.config['Mesaj'] = f"pyAdminKullanicilar-204"
            return redirect("/SanalYetkisiz")
        
        SQLKomut = f"UPDATE SKUsers SET AtolyeID = ?, DurumID = ? WHERE UserID = ?"
        Params   = (0, 41, UserID)
        SQLCevap  = SQLServer.Calistir(SQLKomut, Params)
        
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üye Pasifleme İşlemi Yapılamadı. (SKUsers)"
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-205"
            return redirect("/SanalStop")
        
        SQLKomut = "SELECT * FROM SKUsers WHERE UserID = ?"
        Params   = (UserID, )
        User     = SQLServer.Sorgula(SQLKomut, Params)
        SQLMemberDateID = User[0]["SQLMemberDateID"]
        if SQLMemberDateID == 0:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üye Pasifleme İşlemi Yapılamadı. (SKUsers)"
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-206"
            return redirect("/SanalStop")
        
        SQLKomut = f"UPDATE SKMemberDates SET SonlanmaTarihi = ? WHERE UserID = ? AND ID = ?"
        Params   = (Kapanis, UserID, SQLMemberDateID)     
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üye Pasifleme İşlemi Yapılamadı. (SKUsers)"
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-207"
            return redirect("/SanalStop")
        
        # Kullanıcıya Üyeliğiniz Kapatıldı Bilgisini Verelim...
        MailKime   = User[0]["UserMailAdress"].strip()
        Baslik     = "Serap KOÇAK Web Sitesi Bilgilendirme"
        Mesaj      = f"""
            Sayın: { User[0]['UserAdiSoyadi'].strip() }\n\n
            Serap KOÇAK Web Sitesi'nde Yeni Projelere Erişiminiz Kapatılmıştır.\n\n
            Üyeliğinizin aktif olduğu tarihler arasında yayınlanan projelere erişiminiz açıktır.
            """
        DurumMail  = mail_sender.MailGonderme(MailKime, Baslik, Mesaj)
        if not DurumMail:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üye Pasifleme İşlemi Başarıyla Yapıldı. Ancak Kullanıcıya Bilgilendirilme eMail'i Gönderilemedi."
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-208"
            return redirect("/SanalStop")
        else:
            return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-299 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route(f'/AdmUyeCihazReset/<string:UserID>', methods=["POST"])
def ADM_KULLANICILAR_03(UserID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-301"
            return redirect("/SanalYetkisiz")
        
        if not UserID or UserID is None:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-302"
            return redirect("/SanalYetkisiz")
        
        User = int(UserID)
        if UserID == 0:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-303"
            return redirect("/SanalYetkisiz")
        
        SQLKomut   = f"UPDATE SKUsers SET SQLCihazKodu = ? WHERE UserID = ?"
        Params  = ("Tanımsız", UserID)
        SQLCevap    = SQLServer.Calistir(SQLKomut, Params)
        
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üyenin Cihaz Resetleme İşlemi Yapılamadı. (SKUsers)"
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-304"
            return redirect("/SanalStop")
        
        User     = SQLServer.Sorgula(f"SELECT * FROM SKUsers WHERE UserID={UserID}")
        MailKime = User[0]["UserMailAdress"].strip()
        Baslik   = "Serap KOÇAK Web Sitesi Bilgilendirme"
        Mesaj    = f"""Sayın: {User[0]["UserAdiSoyadi"].strip()}\n\n
                    Serap KOÇAK Web Sitesi'nde Cihaz Bilgileriniz Resetlenmiştir.\n\n\n\n
                    Serap KOÇAK Web Sitesine Erişiminiz İçin Site Giriş Bilgileriniz Aşağıda Sunulmuştur...\n\n\n
                    Adınız Soyadınız: {User[0]["UserAdiSoyadi"].strip()}\n
                    Mail Adresiniz: { User[0]["UserMailAdress"].strip()}\n
                    Şifreniz: { Sifreleme.SifreyiCoz(User[0]["PassWord"].strip()) }\n
                    Onay Kodunuz: {User[0]["VerifyMailCode"]}\n\n\n
                    İlk Giriş Yaptığınızda Kullandığınız Cihaz Bilgileri Sistemimizde Kayıt Edilecek Olup, 
                    Tekrar sisteme başka bir cihazla giriş yaparsanız üyeliğinizin iptal edileceğini, 
                    SİTE KULLANIM KURALLARI gereğince önemle hatırlatırız."""
        DurumMail = mail_sender.MailGonderme(MailKime, Baslik, Mesaj)
        if not(DurumMail):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üye Cihaz Resetlemesi Başarıyla Yapıldı. Ancak Kullanıcıya Bilgilendirilme eMail'i Gönderilemedi."
            current_app.config['Mesaj3'] = "pyAdminKullanicilar-305"
            return redirect("/SanalStop")
        
        return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-399 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route('/AdmSonrakiSayfa', methods=["POST"])
def ADM_KULLANICILAR_04():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-401"
            return redirect("/SanalYetkisiz")
        
        SayfaAdim                = int(session.get("SayfaAdim"))
        IlkSatirIndis            = int(session.get("IlkSatirIndis"))
        IlkSatirIndis            = IlkSatirIndis + SayfaAdim 
        session['IlkSatirIndis'] = str(IlkSatirIndis)
        return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-499 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route('/AdmOncekiSayfa', methods=["POST"])
def ADM_KULLANICILAR_05():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminKullanicilar-501"
            return redirect("/SanalYetkisiz")
        
        IlkSatirIndis            = session.get("IlkSatirIndis")
        SayfaAdim                = int(session.get("SayfaAdim"))
        IlkSatirIndis            = int(IlkSatirIndis) - SayfaAdim
        session['IlkSatirIndis'] = str(IlkSatirIndis)
        return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-599 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route('/AdmUsersFiltre/<string:DurumID>', methods=["POST"])
def ADM_KULLANICILAR_06(DurumID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-601"
            return redirect("/SanalYetkisiz")
        
        if not DurumID or DurumID is None:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-602"
            return redirect("/SanalYetkisiz")
        
        DurumID = int(DurumID)
        if DurumID <= 0:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-603"
            return redirect("/SanalYetkisiz")
        
        session["DurumFiltreID"]    = DurumID
        return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-699 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route('/AdmUsersFitreReset', methods=["POST"])
def ADM_KULLANICILAR_07():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-701"
            return redirect("/SanalYetkisiz")
        
        session["DurumFiltreID"]    = "0"
        session["AdSoyadFiltre"]    = ""
        session["IlkSatirIndis"]    = "0"
        return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-799 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route('/AdmUserNameFiltre/<string:AdSoyadTxt>', methods=["POST"])
def ADM_KULLANICILAR_08(AdSoyadTxt):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-801"
            return redirect("/SanalYetkisiz")
        
        if not AdSoyadTxt or AdSoyadTxt == "":
            current_app.config['Mesaj']    = "pyAdminKullanicilar-802"
            return redirect("/SanalYetkisiz")
        
        session["IlkSatirIndis"]    = "0"
        session["AdSoyadFiltre"]    = AdSoyadTxt
        return redirect("/AdminGoster")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-899 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route('/AdmModelAc/<string:UserID>', methods=["POST"])
def ADM_KULLANICILAR_09(UserID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-901"
            return redirect("/SanalYetkisiz")
        
        if not UserID or UserID == 0:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-902"
            return redirect("/SanalYetkisiz")
        
        session["UserID"] = UserID
        session["ModelAcKapatIlkSatir"] = "0"
        return redirect("/AdmModelAcKapat")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-999 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route(f'/AdmUyeDetay/<string:UserID>', methods=["POST"])
def ADM_KULLANICILAR_10(UserID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-A01"
            return redirect("/SanalYetkisiz")
        
        if not UserID or UserID == 0:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-A02"
            return redirect("/SanalYetkisiz")
        
        session["UserID"] = UserID
        return redirect("/AdmUserDetail")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-A99 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmKullanicilar.route(f'/AdminEtkinlikYonetimi')
def ADM_KULLANICILAR_11():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminKullanicilar-B01"
            return redirect("/SanalYetkisiz")
        
        return redirect("/AdmEtkinlikler")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminKullanicilar-B99 ({e})"
        return redirect("/SanalError")
##############################################################################################################