from flask import render_template, Blueprint, redirect, current_app, session, request
import YorumIndex, mail_sender, datetime, SQLServer, SiteSabit, SQLToBase64, time, random, SessionKontrolleri
##############################################################################################################
Index = Blueprint('index', __name__, template_folder='templates')
##############################################################################################################
@Index.route('/')
def GirisSayfasi():
    session['SonHareket']      = time.time()
    session['SessionID']       = random.randint(100000, 999999)
    session["ZiyaretciID"]     = random.randint(100000, 999999)
    session['AdminMail']       = SQLServer.DegerGetir("SELECT Sutun08 FROM SKWebSabitler").strip()
    session['ModelSys']        = SQLServer.DegerGetir("SELECT COUNT(*) FROM SKModels")
    session['SayfaAdim']       = "100"
    session['ModelSayfaAdim']  = "10"
    return render_template("LocalDegerOku.html")
##############################################################################################################
@Index.route("/IndexSayfasi")
def AnaSayfa():
    try:
        SessKontrol = SessionKontrolleri.IndexSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyIndex-001"
            return redirect("/SanalYetkisiz")          
        
        TMRSVS    = YorumIndex.ToplamModel()
        RS        = YorumIndex.RastgeleSecim()
        SP        = YorumIndex.SonProjeSorgulari()
        AP        = YorumIndex.AbonelikPaketiSorgulari()
        WS        = YorumIndex.WEBSabitleriSorgulari()
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not SiteOwner :
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyAdminModels-102"
            return redirect("/SanalStop")
        
        CK = str(session.get("LocalStorage"))
        return render_template('Index.html', SiteOwner = SiteOwner, TM = TMRSVS, RST = RS, SP = SP, APK = AP, WS = WS, CK = CK)
    except Exception as e:
        current_app.config['Mesaj']    = "pyIndex-099"
        return redirect("/SanalError")     
##############################################################################################################
@Index.route('/BtnMesajGonder', methods=["POST"])
def MesajGonder():
    try:
        SessKontrol = SessionKontrolleri.IndexSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyIndex-101"
            return redirect("/SanalYetkisiz")
           
        FormUserName  = request.form.get("AdSoyad").upper().strip()
        FormUserMail  = request.form.get("MailAdres")
        FormKonu      = request.form.get("MesajKonusu")
        FormMesaj     = request.form.get("MesajIcerik")
        if not all(FormUserName, FormUserMail, FormKonu, FormMesaj):
            current_app.config['Mesaj1'] = "Formu Boş Geçip Mesaj Göndermezsiniz"
            current_app.config['Mesaj2'] = "Lütfen Bütün Alanları Doldurup Tekrar Deneyiniz"
            current_app.config['Mesaj3'] = "pyIndex-102"
            return redirect("/SanalStop")
        
        PytGovdesi    = f"""Mesajı Gönderenin Adı Soyadı: {FormUserName}\n\nMesajı Gönderenin Mail Adresi: {FormUserMail}\n\nMesajı Gönderenin Konusu: {FormKonu}\n\n"
                        Mesaj Tarih/Saati: { datetime.datetime.now() }\n\n{"-"*80}\n\nMesaj Gövdesi:\n{FormMesaj}\n\n{"-"*80}\n\n"""
        MesajKonusu   = f"Ana Sayfadan ( {FormUserName} ) Mesaj Gönderdi..."
        AdminMail     = session.get('AdminMail').strip()
        MailDurum = mail_sender.MailGonderme(AdminMail, MesajKonusu, PytGovdesi)
        if not(MailDurum):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Mailiniz Gönderilme Aşamasında Hata Oluşmuştur"
            current_app.config['Mesaj3'] = "pyIndex-103"
            return redirect("/SanalStop")
        
        SQLKomut = "INSERT INTO SKMessage (AdSoyad, MailAdres, Konu, Icerik, MessageTarih, CevapDurum) VALUES (?, ?, ?, ?, GETDATE(), 0)"
        Params   = (FormUserName, FormUserMail, FormKonu, FormMesaj)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Mailiniz Gönderilme Aşamasında Hata Oluşmuştur"
            current_app.config['Mesaj3'] = "pyIndex-104"
            return redirect("/SanalStop")
        
        SQLUpdate = "UPDATE SkWebSabitler SET Sutun13 = COALESCE((SELECT COUNT(*) FROM SKMessage WHERE CevapDurum=0), 0)"
        SQLCevap  = SQLServer.Calistir(SQLUpdate)

        current_app.config['BaseSabitler'] = []
        current_app.config['BaseSabitler'] = SiteSabit.Sabitler()
        current_app.config['Mesaj1']       = "Teşekkür Ederiz"
        current_app.config['Mesaj2']       = "Mesajınızı Aldık"
        return redirect("/SanalOK")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyIndex-199 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@Index.route('/SonModelVideoGoster/<string:ModelID>', methods=["POST", "GET"])
def SonModelVideoGosterme(ModelID):
    try:
        SessKontrol = SessionKontrolleri.IndexSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyIndex-201"
            return redirect("/SanalYetkisiz")
        
        if not(ModelID):
            current_app.config['Mesaj']    = "pyIndex-202"
            return redirect("/SanalYetkisiz")
        
        ModelID = int(ModelID)
        if ModelID <= 0:
            current_app.config['Mesaj']    = "pyIndex-203"
            return redirect("/SanalYetkisiz")
        
        SQLSorgu = f"SELECT BinaryDosya AS Video FROM SKVideos WHERE ModelID = ? AND Sira = ?"
        Params   = (ModelID, 1)
        Video    = SQLServer.Sorgula(SQLSorgu, Params)
        if not Video:
            current_app.config['Mesaj']    = "pyIndex-204"
            return redirect("/SanalYetkisiz")
        
        Video    = SQLToBase64.Video(Video)
        KapatmaDurumu = "/"
        return render_template("MediaVideoPlayer.html", Video = Video, VS = "Model Demo Videosu", KapatmaDurumu = KapatmaDurumu)    
    except Exception as e:
        current_app.config['Mesaj']    = f"pyIndex-299 ({e})"
        return redirect("/SanalError")   
##############################################################################################################
##############################################################################################################
