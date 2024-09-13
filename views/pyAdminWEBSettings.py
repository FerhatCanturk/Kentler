from flask import render_template, Blueprint, redirect, current_app, session, request, flash
import YorumWebSettings, SQLServer, os, SessionKontrolleri
##############################################################################################################
AdmSettings = Blueprint('AdmSettings', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@AdmSettings.route("/WebSiteSettings")
def WebSettings00():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminWebSettings-001"
            return redirect("/SanalYetkisiz")
        
        WebSabitler = YorumWebSettings.WEBSabitleriSorgulari()
        Pockets     = YorumWebSettings.AbonelikPaketiSorgulari()
        Groups      = YorumWebSettings.GrubSorgulari()
        
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not SiteOwner or not WebSabitler:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyAdminWebSettings-002"
            return redirect("/SanalStop")
        
        return render_template("AdmWebAyar.html", SiteOwner = SiteOwner, 
                            WebSabitler = WebSabitler, Pockets = Pockets, Groups = Groups)
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminWebSettings-099 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmSettings.route('/WebSiteSabitKayıt1', methods=["POST"])
def WebSettings01():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminWebSettings-101"
            return redirect("/SanalYetkisiz")
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            file = request.files['file']
            if file:
                filename = 'BackGround.jpg'
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if filename.lower().endswith('.jpg'):
                    if os.path.exists(file_path):
                        os.remove(file_path)

                    IMAGE_EXTENSIONS = {
                        'image/png',                   # PNG formatı
                        'image/jpeg',                  # JPEG formatı
                        'image/gif',                   # GIF formatı
                        'image/bmp',                   # BMP formatı
                        'image/tiff',                  # TIFF formatı
                        'image/webp',                  # WEBP formatı
                        'image/jp2',                   # JPEG 2000 formatı
                    }
                    ResimKontrol = file.content_type in IMAGE_EXTENSIONS
                    if not ResimKontrol: 
                        current_app.config['Mesaj1'] = "Resim Dosyası Seçmelisiniz..."
                        current_app.config['Mesaj2'] = "Seçtiğiniz Arka Plan Resmi Kayıt Edilemedi"
                        current_app.config['Mesaj3'] = "pyAdminWebSettings-102"
                        return redirect("/SanalStop")
                    file.save(file_path)
        except Exception as e:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Seçtiğiniz Arka Plan Resmi Kayıt Edilemedi"
            current_app.config['Mesaj3'] = "pyAdminWebSettings-103"
            return redirect("/SanalStop")
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        Sutun01  = request.form.get('WS01').strip(); Sutun02 = request.form.get('WS02').strip(); Sutun03 = request.form.get('WS03').strip(); Sutun04 = request.form.get('WS04').strip() 
        Sutun05  = request.form.get('WS05').strip(); Sutun06 = request.form.get('WS06').strip(); Sutun07 = request.form.get('WS07').strip(); Sutun08 = request.form.get('WS08').strip() 
        Sutun09  = request.form.get('WS09').strip(); Sutun10 = request.form.get('WS10').strip(); Sutun11 = request.form.get('WS11').strip(); Sutun12 = request.form.get('WS12').strip()
        Sutun14  = request.form.get('WS14').strip(); Sutun15 = request.form.get('WS15').strip(); Sutun16 = request.form.get('WS16').strip()

        SQLKomut = """UPDATE SkWebSabitler SET 
                    Sutun01 = ?, Sutun02 = ?, Sutun03 = ?, Sutun04 = ?, Sutun05 = ?, 
                    Sutun06 = ?, Sutun07 = ?, Sutun08 = ?, Sutun09 = ?, Sutun10 = ?,
                    Sutun11 = ?, Sutun12 = ?, Sutun14 = ?, Sutun15 = ?, Sutun16 = ?
                    WHERE HTMLSayfaAdi LIKE 'Index%' """
        Params   = (Sutun01, Sutun02, Sutun03, Sutun04, Sutun05, Sutun06, Sutun07, Sutun08, Sutun09, Sutun10, Sutun11, Sutun12, Sutun14, Sutun15, Sutun16)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Web Sitesi Sabitleri Güncellemeleriniz Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminWebSettings-104"
            return redirect("/SanalStop")
        
        return redirect("/WebSiteSettings")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminWebSettings-199 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmSettings.route('/WebSiteSabitKayıt2', methods=["POST"])
def WebSettings02():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminWebSettings-201"
            return redirect("/SanalYetkisiz")
        
        Pockets    = YorumWebSettings.AbonelikPaketiSorgulari()
        for Pocket in Pockets:
            Pid = Pocket["PaketID"]
            PK1 = request.form.get(f'PK1_{Pid}'); PK2 = request.form.get(f'PK2_{Pid}'); PK3 = request.form.get(f'PK3_{Pid}'); PK4 = request.form.get(f'PK4_{Pid}') 
            PK5 = request.form.get(f'PK5_{Pid}'); PK6 = request.form.get(f'PK6_{Pid}'); PK7 = request.form.get(f'PK7_{Pid}'); PK8 = request.form.get(f'PK8_{Pid}') 
            SQLKomut = "UPDATE SKPaketler SET Kisa = ?, PaketAdi = ?, Sutun1 = ?, Sutun2 = ?, Sutun3 = ?, Sutun4 = ?, SutunFiyat = ?, Kurallar = ?  WHERE PaketID = ?"
            Params   = (PK1, PK2, PK3, PK4, PK5, PK6, PK7, PK8, Pid)
            SQLCevap = SQLServer.Calistir(SQLKomut, Params)
            if SQLCevap:
                current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
                current_app.config['Mesaj2'] = f"Abone Paketleri Güncellemeleriniz Yapılamadı (PaketID:{Pid})"
                current_app.config['Mesaj3'] = "pyAdminWebSettings-202"
                return redirect("/SanalStop")
            
        return redirect("/WebSiteSettings")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminWebSettings-299 ({e})"
        return redirect("/SanalError") 
##############################################################################################################
@AdmSettings.route('/WebGrubDegistir/<string:GrubID>', methods=["POST", 'GET'])
def AdmWEBKaydet3(GrubID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminWebSettings-301"
            return redirect("/SanalYetkisiz")

        if GrubID is None:
            current_app.config['Mesaj']    = "pyAdminWebSettings-302"
            return redirect("/SanalYetkisiz")
        
        GrubID = int(GrubID)
        if GrubID <= 0:
            current_app.config['Mesaj']    = "pyAdminWebSettings-303"
            return redirect("/SanalYetkisiz")
        
        if request.method == "POST":
            file = request.files.get(f'EskiFile{GrubID}')
            if file:
                filename = f'Grub{GrubID}.jpg'
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if filename.lower().endswith('.jpg'):
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    file.save(file_path)
                else:
                    current_app.config['Mesaj1'] = "Grup Demo Resimlerinde (*.jpg) Uzantılı Dosya Seçmelisiniz"
                    current_app.config['Mesaj2'] = "Grup Resmi Güncellemeleriniz Yapılamadı"
                    current_app.config['Mesaj3'] = "pyAdminWebSettings-302"
                    return redirect("/SanalStop")

            GrubAdi = request.form.get(f'GrubAdi{GrubID}')
            if GrubAdi:  
                SQLKomut = f"UPDATE SKGroups SET GrubAdi = ? WHERE GrubID = ?"
                Params   = (GrubAdi, GrubID)
                SQLCevap = SQLServer.Calistir(SQLKomut, Params)
                if SQLCevap:
                    current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
                    current_app.config['Mesaj2'] = "GrubAdı Güncellemeleriniz Yapılamadı"
                    current_app.config['Mesaj3'] = "pyAdminWebSettings-303"
                    return redirect("/SanalStop")
            
            return redirect("/WebSiteSettings")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminWebSettings-399 ({e})"
        return redirect("/SanalError") 
##############################################################################################################
@AdmSettings.route('/WebGrubSilme/<string:GrubID>', methods=["POST"])
def AdmWEBKaydet4(GrubID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminWebSettings-401"
            return redirect("/SanalYetkisiz")
        
        if GrubID is None:
            current_app.config['Mesaj']    = "pyAdminWebSettings-402"
            return redirect("/SanalYetkisiz")
        
        GrubID = int(GrubID)
        if GrubID <= 0:
            current_app.config['Mesaj']    = "pyAdminWebSettings-403"
            return redirect("/SanalYetkisiz")

        filename = f'Grub{GrubID}.jpg'
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        SQLKomut = f"DELETE FROM SKGroups WHERE GrubID = ? AND GrubID NOT IN (SELECT GrubID FROM SKModels)"
        SQLCevap = SQLServer.Calistir(SQLKomut, (GrubID, ))
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Grub Silme İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminWebSettings-404"
            return redirect("/SanalStop")
        
        return redirect("/WebSiteSettings")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminWebSettings-499 ({e})"
        return redirect("/SanalError") 
##############################################################################################################
@AdmSettings.route('/WebYeniGrubKayit', methods=['POST'])
def AdmWEBKaydet5():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminWebSettings-501"
            return redirect("/SanalYetkisiz")
        
        GrubID = SQLServer.DegerGetir("SELECT COALESCE(MAX(GrubID), 0) + 1 FROM SKGroups")   

        if GrubID <=0:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "VeriTabanınızda Yapısal Hata Oluştu."
            current_app.config['Mesaj3'] = "pyAdminWebSettings-502"
            return redirect("/SanalStop")
        
        file = request.files['fileYeni']
        if file:
            if file.filename.lower().endswith('.jpg'):
                filename = f'Grub{GrubID}.jpg'
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                file.save(file_path)
            else:
                current_app.config['Mesaj1'] = "Grup Demo Resimlerinde (*.jpg) Uzantılı Dosya Seçmelisiniz"
                current_app.config['Mesaj2'] = "Grup Resmi Güncellemeleriniz Yapılamadı"
                current_app.config['Mesaj3'] = "pyAdminWebSettings-503"
                return redirect("/SanalStop")
        
        YeniGrubAdi = request.form.get('YeniGrubAdi').strip().upper()
        SQLKomut = f"INSERT INTO SKGroups (GrubID, GrubAdi) VALUES (?, ?)"
        Params   = (GrubID, YeniGrubAdi)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Grub Kayıt İşleminiz Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminWebSettings-504"
            return redirect("/SanalStop")
        return redirect("/WebSiteSettings")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminWebSettings-599 ({e})"
        return redirect("/SanalError") 
##############################################################################################################