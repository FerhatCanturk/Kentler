from flask import render_template, Blueprint, redirect, current_app, session, request
import SQLServer, SQLToBase64, YorumAdminMediaIslemleri, SessionKontrolleri
##############################################################################################################
Media = Blueprint('Media', __name__, template_folder='templates')
##############################################################################################################
@Media.route('/VideoGoster/<string:id>', methods=["POST", "GET"])
def MEDIA00(id):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ModelID")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyMediaIslem-001"
            return redirect("/SanalYetkisiz")
    
        if not(id) and id==None:
            current_app.config['Mesaj'] = "pyMediaIslem-002"
            return redirect("/SanalYetkisiz")
    
        ModelID  = session.get("ModelID") 
        SQLSorgu = "SELECT VideoSayisi FROM SKModels WHERE ModelID = ?"
        VideoMax = SQLServer.DegerGetir(SQLSorgu, (ModelID, ))

        if not(VideoMax):
            current_app.config['Mesaj'] = "pyMediaIslem-003"
            return redirect("/SanalYetkisiz")

        if int(VideoMax) < int(id) or int(id) <= 0:
            current_app.config['Mesaj'] = "pyMediaIslem-004"
            return redirect("/SanalYetkisiz")
        
        SQLSorgu = "SELECT BinaryDosya AS Video FROM SKVideos WHERE ModelID = ? AND Sira = ?"
        Params   = (ModelID, id)
        Video    = SQLServer.Sorgula(SQLSorgu, Params)
        Video    = SQLToBase64.Video(Video)
        
        if not(Video):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyMediaIslem-005"
            return redirect("/SanalStop") 
        
        KapatmaDurumu = "/AdmModelDetay"
        return render_template("MediaVideoPlayer.html", 
                               Video = Video, VS = f"Video-No: {id}", KapatmaDurumu = KapatmaDurumu)    
    except Exception as e:
        current_app.config['Mesaj'] = f"pyMediaIslem-099 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@Media.route('/VideoGonder', methods=['POST', "GET"])
def MEDIA01():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ModelID")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyMediaIslem-101"
            return redirect("/SanalYetkisiz")
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        ModelID  = session.get("ModelID")
        SQLKomut = "SELECT COALESCE(MAX(Sira),0) FROM SKVideos WHERE ModelID = ?"
        
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        Sira = request.form.get("VideoSira")
        if not(Sira):
            Sira=0
        Sira = int(Sira)
        SQLKomut  = "SELECT COUNT(*) FROM SKVideos WHERE ModelID = ? AND Sira = ?"
        SQLParams = (ModelID, Sira)
        SQLCevap  = SQLServer.DegerGetir(SQLKomut, SQLParams)
        if SQLCevap:
            SQLCevap = int(SQLCevap)
            if SQLCevap > 0:
                current_app.config['Mesaj1'] = "Video Sıra Numarası Kullanılmıştır"
                current_app.config['Mesaj2'] = "Video Kaydınız Yapılamadı"
                current_app.config['Mesaj3'] = "pyMediaIslem-102"
                return redirect("/SanalStop")

        VIDEO_EXTENSIONS = {
                'video/mp4',          # MP4 formatı
                'video/webm',         # WebM formatı
                'video/x-msvideo',    # AVI formatı
                'video/x-matroska',   # MKV formatı
                'video/quicktime',    # MOV formatı
                'video/x-flv',        # FLV formatı
                'video/mpeg',         # MPEG formatı
                'video/3gpp',         # 3GP formatı
                'video/x-m4v',        # M4V formatı (MP4 varyasyonu)
                'video/x-dv',         # DV formatı (Digital Video)
            }
        VideoKontrol = file.content_type in VIDEO_EXTENSIONS
        if (not VideoKontrol) or Sira <= 0:
            current_app.config['Mesaj1'] = "Video Dosyası Seçmelisiniz..."
            current_app.config['Mesaj2'] = "Video Kaydınız Yapılamadı"
            current_app.config['Mesaj3'] = "pyMediaIslem-103"
            return redirect("/SanalStop")

        file_data = file.read()
        
        SQLKomut = "INSERT INTO SKVideos (ModelID, Sira, BinaryDosya) VALUES (?, ?, ?)"
        Params   = (ModelID, Sira, file_data)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Video Kaydınız Yapılamamıştır"
            current_app.config['Mesaj3'] = "pyMediaIslem-104"
            return redirect("/SanalStop")     
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        return redirect("/AdmModelDetay")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyMediaIslem-199 {e}"
        return redirect("/SanalError")     
##############################################################################################################
@Media.route('/VideoSil/<string:id>', methods=['POST'])
def MEDIA02(id):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ModelID")
        if SessKontrol:
            current_app.config['Mesaj'] = "Model-Detay-201"
            return redirect("/SanalYetkisiz")
        
        if not(id) and id==None:
            current_app.config['Mesaj'] = "pyMediaIslem-202"
            return redirect("/SanalYetkisiz")
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        ModelID  = session.get("ModelID")    # Bunun 0'dan Büyük Olma Şartı Session Kontrolünde Geçmişti.
        SQLKomut = "SELECT COALESCE(VideoSayisi, 0) FROM SKModels WHERE ModelID = ?"
        Params   = (ModelID, )
        VideoMax = SQLServer.DegerGetir(SQLKomut, Params)
        
        if not(VideoMax):
            current_app.config['Mesaj']    = "pyMediaIslem-203"
            return redirect("/SanalYetkisiz")
        
        if int(id) == 0 or VideoMax <= 0:
            current_app.config['Mesaj']    = "pyMediaIslem-204"
            return redirect("/SanalYetkisiz")
        
        SQLKomut = "DELETE FROM SKVideos WHERE Sira = ? AND ModelID = ?"
        Params   = (id, ModelID)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Video Silme İşleminiz Yapılamamıştır."
            current_app.config['Mesaj3'] = "pyMediaIslem-205"
            return redirect("/SanalStop")
         
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        return redirect("/AdmModelDetay")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyMediaIslem-299 {e}"
        return redirect("/SanalError")     
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
@Media.route('/ResimGonder', methods=['POST',"GET"])
def MEDIA03():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ModelID")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyMediaIslem-301"
            return redirect("/SanalYetkisiz")
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        ModelID  = session.get("ModelID")
        SQLKomut = "SELECT COALESCE(ResimSayisi, 0) FROM SKModels WHERE ModelID = ?"
        
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        Sira = request.form.get("PictSira")
        if not (Sira):
            Sira=0

        Sira = int(Sira)
        SQLKomut  = "SELECT COUNT(*) AS Sys FROM SKPictures WHERE ModelID = ? AND Sira = ?"
        SQLParams = (ModelID, Sira)
        SQLCevap  = SQLServer.DegerGetir(SQLKomut, SQLParams)
        if SQLCevap:
            SQLCevap = int(SQLCevap)
            if SQLCevap > 0:
                current_app.config['Mesaj1'] = "Resim Sıra Numarası Kullanılmıştır"
                current_app.config['Mesaj2'] = "Resim Kaydınız Yapılamadı"
                current_app.config['Mesaj3'] = "pyMediaIslem-302"
                return redirect("/SanalStop")
            
        IMAGE_EXTENSIONS = {
                'image/png',                   # PNG formatı
                'image/jpeg',                  # JPEG formatı
                'image/gif',                   # GIF formatı
                'image/bmp',                   # BMP formatı
                'image/tiff',                  # TIFF formatı
                'image/webp',                  # WEBP formatı
                'image/jp2',                   # JPEG 2000 formatı
                'image/jpg',                   # JPEG 2000 formatı
            }
        ResimKontrol = file.content_type in IMAGE_EXTENSIONS
        if (not ResimKontrol) or Sira <= 0: 
            current_app.config['Mesaj1'] = "Resim Dosyası Seçmelisiniz..."
            current_app.config['Mesaj2'] = "Resim Kaydınız Yapılamamıştır"
            current_app.config['Mesaj3'] = "pyMediaIslem-303"
            return redirect("/SanalStop")
        
        file_data = file.read()
        
        SQLKomut = "INSERT INTO SKPictures (ModelID, Sira, BinaryDosya) VALUES (?, ?, ?)"
        Params   = (ModelID, Sira, file_data)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Resim Kaydınız Yapılamamıştır"
            current_app.config['Mesaj3'] = "pyMediaIslem-304"
            return redirect("/SanalStop") 
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        return redirect("/AdmModelDetay")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyMediaIslem-399 ({e})"
        return redirect("/SanalError")    
##############################################################################################################
@Media.route('/ResimSil/<string:id>', methods=['POST'])
def MEDIA04(id):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ModelID")
        if SessKontrol:
            current_app.config['Mesaj'] = "Model-Detay-401"
            return redirect("/SanalYetkisiz")
        
        if not(id) and id==None:
            current_app.config['Mesaj'] = "pyMediaIslem-402"
            return redirect("/SanalYetkisiz")
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        ModelID  = session.get("ModelID")
        SQLSorgu = "SELECT COALESCE(ResimSayisi,0) FROM SKModels WHERE ModelID = ?"
        ResimMax = SQLServer.DegerGetir(SQLSorgu, (ModelID, ))

        if not(ResimMax):
            current_app.config['Mesaj'] = "pyMediaIslem-403"
            return redirect("/SanalYetkisiz")
        
        if int(id) == 0 or ResimMax <= 0:
            current_app.config['Mesaj'] = "pyMediaIslem-404"
            return redirect("/SanalYetkisiz")
        
        SQLKomut = "DELETE FROM SKPictures WHERE Sira = ? AND ModelID = ?"
        Params   = (id, ModelID)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Video Silme İşleminiz Yapılamamıştır."
            current_app.config['Mesaj3'] = "pyMediaIslem-405"
            return redirect("/SanalStop")
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        return redirect("/AdmModelDetay")

    except Exception as e:
        current_app.config['Mesaj'] = f"Model-Detay-499 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
