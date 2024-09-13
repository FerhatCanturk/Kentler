from flask import render_template, Blueprint, redirect, current_app, request, session
import mail_sender, datetime, SQLServer, uuid, SessionKontrolleri, uuid, Sifreleme
##############################################################################################################
UyeGiris = Blueprint('UyeGiris', __name__, template_folder='templates')
##############################################################################################################
@UyeGiris.route('/IndexUyeGirisAnaliz')
def IndexuyeGiris00():
    # Bu Metod Sadece Base.Html Sayfası Butonundan Tetiklenir
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj']  = "PyIndexUyeGiris-001"
            return redirect("/SanalYetkisiz")
        
        LocalStorage = session.get("LocalStorage","").strip()
        SiteOwner    = current_app.config.get('BaseSabitler', {})
        # ?????????????????????????????????????????????????????????????????????????????????????????????
        SQLSorgu = "SELECT * FROM SKUsers WHERE SqlCihazKodu = ?"
        UserSorgu = SQLServer.Sorgula(SQLSorgu, (LocalStorage, ))
        # ?????????????????????????????????????????????????????????????????????????????????????????????
        if not(UserSorgu):
            if not(SiteOwner):
                current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
                current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
                current_app.config['Mesaj3'] = "PyIndexUyeGiris-002"
                return redirect("/SanalStop")
            return render_template("IndexUyeUyari.html", SiteOwner = SiteOwner)
        
        session['ClientID'] = str(UserSorgu[0]['UserID'])
        return redirect("/UyeSayfasi") 
    except Exception as e:
        current_app.config['Mesaj']    = f"pyIndexUyeGiris-099 ({e})"
        return redirect("/SanalError")
#######################################################################################################################################################
@UyeGiris.route("/BtnIndexUyeUyariHTML")
def IndexuyeGiris01():
    # Bu Metod IndexUyeUyari.html Dosyası Butonundan Tetiklenir
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj']  = "PyIndexUyeGiris-101"
            return redirect("/SanalYetkisiz")
        
        SiteOwner     = current_app.config.get('BaseSabitler', {})
        if not(SiteOwner):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "PyIndexUyeGiris-102"
            return redirect("/SanalStop")
        
        return render_template("IndexUyeGiris.html", SiteOwner = SiteOwner)
    except Exception as e:
        current_app.config['Mesaj']    = f"pyIndexUyeGiris-199 ({e})"
        return redirect("/SanalError")
#######################################################################################################################################################  
@UyeGiris.route('/BtnUyeGirisSonKontrollerHTML', methods=["POST"])
def IndexuyeGiris02():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj']  = "PyIndexUyeGiris-001"
            return redirect("/SanalYetkisiz")
        
        FormMailAdres = request.form.get("MailAdres").strip().lower()
        FormUserName  = request.form.get("UserName").strip()
        FormUserPass  = request.form.get("PassWord").strip()
        FormOnayKodu  = request.form.get("OnayKodu").strip()
        FormDurum     = FormMailAdres is not None
        FormDurum     = FormDurum and FormUserName is not None
        FormDurum     = FormDurum and FormUserPass is not None
        FormDurum     = FormDurum and FormOnayKodu is not None
        if not FormDurum:
            current_app.config['Mesaj1']    = "Bütün Alanları Doldurmalısınız"
            current_app.config['Mesaj1']    = "Aksi Halde Giriş Yapamazsınız"
            return redirect("/SanalMesaj")
            
        FormUserPass = Sifreleme.Sifrele(FormUserPass)
        print(FormUserPass)
        SQLKomut     = "SELECT * FROM SKUsers WHERE UserName = ? AND UserMailAdress = ? AND VerifyMailCode = ? AND PassWord = ?"
        SQLParams    = (FormUserName, FormMailAdres, FormOnayKodu, FormUserPass)
        PWKontrol    = SQLServer.Sorgula(SQLKomut, SQLParams)
        if not(PWKontrol):
            # Kullanıcı Adı ve Şifresi Uyuşmadı
            current_app.config['Mesaj1']    = "Ooooops !!!!!"
            current_app.config['Mesaj2']   = "eMail, KullanıcıAdı, Şifre ve OnayKodu Uyuşmamıştır"
            current_app.config['Mesaj3']   = "pyIndexUyeGiris-203"
            return redirect("/SanalStop")
        
        # Kullanıcı Adı ve Şifresi Uyuştu
        PUserID              = int(PWKontrol[0]["UserID"]) 
        PMailAdr             = PWKontrol[0]["UserMailAdress"]
        SqlCihazKodu         = PWKontrol[0]["SqlCihazKodu"]
        GCihazKodu           = session.get('LocalStorage')
        YazilacakDeger       = GCihazKodu
        BlokajKonulacak      = False 
        LocalStorageKayit    = False
        SQLKayitYap          = False

        if SqlCihazKodu == None or SqlCihazKodu == "Tanımsız":
            SqlCihazKodu = ""

        if SqlCihazKodu > "" and GCihazKodu != "":
            # Her ikiside Kayıtlı Durumda Cihaz Kontrolü Yap
            LocalStorageKayit   = False
            BlokajKonulacak     = SqlCihazKodu != GCihazKodu
            SQLKayitYap         = False
        elif SqlCihazKodu == "" and GCihazKodu != "":
            # Bunun Olması Zor Biraz (SQL'de Yok Bilgisayarda Var. Bu Kodu SQL'e Yazalım...)
            BlokajKonulacak     = False
            LocalStorageKayit   = False
            SQLKayitYap         = True
            YazilacakDeger      = GCihazKodu
        elif SqlCihazKodu > "" and GCihazKodu == "":
            # SQL'de Var Bilgisayarda YOK Başka Makine'den Zorlanıyoooooooooooooor
            BlokajKonulacak     = True
            SQLKayitYap         = False
            LocalStorageKayit   = False
        elif SqlCihazKodu == "" and GCihazKodu == "":
            # İlk Giriş Denemesi
            BlokajKonulacak     = False
            LocalStorageKayit   = True
            SQLKayitYap         = True
            YazilacakDeger      = str(uuid.uuid4()).upper().replace("-", "")
            
        if BlokajKonulacak:
            KullaniciyaBlokajAtama(PUserID, PMailAdr)
            session.clear()
            return render_template("IndexBlocked.html")
            
        if SQLKayitYap:
            SQLKomut  = "UPDATE SKUsers SET SqlCihazKodu = ? WHERE UserID = ?"
            SQLParams = (YazilacakDeger, PUserID)
            SQLServer.Calistir(SQLKomut, SQLParams)
        
        if LocalStorageKayit:
            Page = "/UyeSayfasi"
            return render_template("LocalDegerKayit.html", Veri = YazilacakDeger, Page = Page)
        
        session['ClientID'] = PUserID
        return redirect("/UyeSayfasi")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyIndexUyeGiris-299 ({e})"
        return redirect("/SanalError")
#######################################################################################################################################################
@UyeGiris.route('/UyeSayfasi')
def IndexuyeGiris03():
    # Bu Metod Sadece Python'dan Gerekli Olduğunda Tetiklenir....
    try:
        if SessionKontrolleri.IndexSessionKontrolu("ClientID"):
            current_app.config['Mesaj']  = "PyIndexUyeGiris-301"
            return redirect("/SanalYetkisiz")
        
        ClientID  = session.get('ClientID')
        if int(ClientID) == 0:
            current_app.config['Mesaj']    = "pyIndexUyeGiris-302"
            return redirect("/SanalYetkisiz") 
        
        SQLSorgu = f"SELECT * FROM SKUsers WHERE UserID = {ClientID}"     
        SonSorgu = SQLServer.Sorgula(SQLSorgu)
        DurumID  = int(SonSorgu[0]["DurumID"])
        PaketID  = int(SonSorgu[0]["PaketID"])
        if DurumID == 91:
            current_app.config['Mesaj1'] = "Ooooops !!!!!"
            current_app.config['Mesaj2'] = "Blokelisiniz, Giriş Yapamazsınız"
            current_app.config['Mesaj3'] = "pyIndexUyeGiris-303"
            session.clear()
            return redirect("/SanalStop")
        elif PaketID == 11 and DurumID == 11:
            session['ClientID']        = str(ClientID)
            session['ClientName']      = SonSorgu[0]["UserAdiSoyadi"].strip()
            session['DurumFiltreID']   = "0"
            session['AdSoyadFiltre']   = ""
            session["IlkSatirIndis"]   = "0"
            session['AdminUlasim']     = "1"
            session['UserUlasim']      = "0"
            return redirect("/AdminGoster")
        elif PaketID > 11 and (DurumID == 31 or DurumID == 41):
            session['ClientID']        = str(ClientID)
            session['ClientName']      = SonSorgu[0]["UserAdiSoyadi"].strip()
            session['AdminUlasim']     = "0"
            session['UserUlasim']      = "1"
            return redirect("/UserGoster")
        else:
            Durum_Mesajları(DurumID, PaketID, "US", "9")
            current_app.config['Mesaj']    = "pyIndexUyeGiris-304"
            return redirect("/SanalError")
    except Exception as e:
            current_app.config['Mesaj']    =f"pyIndexUyeGiris-399 ({e})"
            return redirect("/SanalError")
#######################################################################################################################################################
def Durum_Mesajları(DurumID, PaketID, MesajEk, Indis):
    #Burası Index Giriş AltYordamıdır Herhangi Bir HTML'den Tetiklenmez
    Durum = True
    current_app.config['Mesaj1'] = ""
    current_app.config['Mesaj2'] = ""
    current_app.config['Mesaj3'] = ""
    PaketID = int(PaketID)
    if PaketID > 11:
        if DurumID == 21:
            current_app.config['Mesaj1'] = "Giriş Yapmak İçin Ödeme Yapmanız Beklenilmektedir"
            current_app.config['Mesaj2'] = "Dekontunuzu Paylaşmanızın Akabinde Kullanıma Açılacaksınız"
            current_app.config['Mesaj3'] = f"pyIndexUyeGiris-{Indis}51-{MesajEk}"
            Durum = False
        elif DurumID == 41:
            #Aboneliği Kapatıldı Ama Yinede Müsaade Edecez
            #Eski Modelleri Görmesi Lazım
            Durum = True
        elif DurumID == 81:
            current_app.config['Mesaj1'] = "Üyeliğiniz Red Edilmiştir"
            current_app.config['Mesaj2'] = "Ana Sayfadan İletişime Geçebilirsiniz"
            current_app.config['Mesaj3'] = f"pyIndexUyeGiris-{Indis}52-{MesajEk}"
        elif DurumID == 91:
            current_app.config['Mesaj1'] = "Ooooops !!!!!"
            current_app.config['Mesaj2'] = "Blokelisiniz, Giriş Yapamazsınız"
            current_app.config['Mesaj3'] = f"pyIndexUyeGiris-{Indis}53-{MesajEk}"
    return Durum
#######################################################################################################################################################
def KullaniciyaBlokajAtama(UserID, Mail):
    #Burası Index Giriş AltYordamıdır Herhangi Bir HTML'den Tetiklenmez
    try:
        if UserID == 0:
            current_app.config['Mesaj']    = "pyIndexUyeGiris-991"
            return redirect("/SanalYetkisiz") 
        
        SQLSorgu   = f"SELECT * FROM SKUsers WHERE UserID = {UserID}"
        Yetkisiz   = SQLServer.Sorgula(SQLSorgu)
        TarihZaman = datetime.datetime.now().date()
        #Kullanıcıya Mail Gidiyor
        #Kullanıcıya Mail Gidiyor
        #Kullanıcıya Mail Gidiyor
        MailKime  = Yetkisiz[0]["UserMailAdress"]
        Baslik    = "Yetkisiz Cihazla Giriş Algılandı..."
        Konu      = "Kayıtlı bulunan cihaz haricinde başka bir cihazla girişiniz algılandı...\n\n"
        Konu     += "Sözleşme Şartları gereğince üyeliğiniz iptal edilmiştir.\n\n"
        Konu     += F"Bloke Edildiğiniz Tarih: {TarihZaman}"
        Durum1    = mail_sender.MailGonderme(MailKime, Baslik, Konu)
        #Admin'e Mail Gidiyor
        #Admin'e Mail Gidiyor
        #Admin'e Mail Gidiyor
        Baslik    = "Kullanıcı Kaçak Girişi Algılandı ve Bloke Edildi..."
        Konu      = """Aşağıdaki Kullanıcının Kayıtlı bulunan cihaz haricinde başka bir cihazla giriş algılandı...\n\n
                Sözleşme Şartları gereğince üyeliği iptal edilerek blokaj konulmuştur.\n\n
                Bu üyenin mail adresi ve telefon numarası kara listede saklanmaya devam edecektir.\n\n\n
                Kullanıcının Adı Soyadı: {Yetkisiz[0]['UserAdiSoyadi'].strip()}\n
                Kullanıcının UserName: {Yetkisiz[0]["UserName"].strip()}\n
                Kullanıcının GSM Numarası: {Yetkisiz[0]["UserGSMNumber"].strip()}\n
                Kullanıcının Mail Adresi: {Yetkisiz[0]["UserMailAdress"].strip()}\n
                Üyenin Bloke Edildiği Tarih: {TarihZaman}\n"""
        AdminMail = session.get('AdminMail').strip()
        Durum2    = mail_sender.MailGonderme(AdminMail, Baslik, Konu)
        SQLUpdate = f"""UPDATE SKUsers SET AtolyeID = 0, DurumID = 91, BlockTarihi = '{TarihZaman}' 
                    WHERE UserID={UserID} OR RTRIM(UserMailAdress)='{Mail}'"""
        
        Durum3    = SQLServer.Calistir(SQLUpdate)
        
        if not(Durum1 and Durum2 and Durum3):
            current_app.config['Mesaj']   = "pyIndexUyeGiris-992"
            return redirect("/SanalError")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyIndexUyeGiris-993 ({e})"
        return redirect("/SanalError")
#######################################################################################################################################################
