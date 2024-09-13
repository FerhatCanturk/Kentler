from flask import render_template, Blueprint, redirect, current_app, request
import SQLServer, SessionKontrolleri
##############################################################################################################
AdmUyeAtolyeleri = Blueprint('AdmUyeAtolyeleri', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@AdmUyeAtolyeleri.route("/AdmUyeAtolyeleri")
def ADM_ATOLYE_00():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminAtolye-001"
            return redirect("/SanalYetkisiz")

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = """
        SELECT *, (SELECT COUNT(*) FROM SKUsers WHERE SKUsers.AtolyeID = SKAtolye.AtolyeID) AS UyeSys 
        FROM SKAtolye ORDER BY Durum DESC, AtolyeAck"""
        Atolyeler = SQLServer.Sorgula(SQLKomut, "")

        SQLKomut = "SELECT * FROM SKUsers WHERE DurumID IN (?, ?) ORDER BY UserAdiSoyadi"
        Params   = (11, 31)
        Users     = SQLServer.Sorgula(SQLKomut, Params)

        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not SiteOwner:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyAdminAtolye-002"
            return redirect("/SanalStop")

        return render_template('AdmAtolyeIslem.html', SiteOwner = SiteOwner, 
                                            Atolyeler = Atolyeler, Users = Users)
    except Exception as e:
    # Hata yönetimi
        current_app.config['Mesaj'] = f"pyAdminAtolye-099 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmUyeAtolyeleri.route("/AtolyeyeEkleme", methods=["POST"])
def ADM_ATOLYE_01():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminAtolye-101"
            return redirect("/SanalYetkisiz")

        UserID   = request.form.get('UserID')
        AtolyeID = request.form.get('AtolyeID')
        UserID   = int(UserID)
        AtolyeID = int(AtolyeID)
        
        if UserID <= 0 or AtolyeID <= 0:
            current_app.config['Mesaj'] = "pyAdminAtolye-102"
            return redirect("/SanalYetkisiz")

        if UserID <= 0 or AtolyeID <= 0:
            current_app.config['Mesaj'] = "pyAdminAtolye-103"
            return redirect("/SanalYetkisiz")
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = "UPDATE SKUsers SET AtolyeID = ? WHERE UserID = ?"
        Params   = (AtolyeID, UserID)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üyenin Atölyeye Ekleme İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminAtolye-104"
            return redirect("/SanalStop")
        return redirect("/AdmUyeAtolyeleri")
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminAtolye-199 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmUyeAtolyeleri.route("/AtolyedenCikart/<string:AtolyeID>/<string:UserID>")
def ADM_ATOLYE_02(AtolyeID, UserID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminAtolye-201"
            return redirect("/SanalYetkisiz")

        UserID   = int(UserID)
        AtolyeID = int(AtolyeID)
        
        if UserID <= 0 or AtolyeID <= 0:
            current_app.config['Mesaj'] = "pyAdminAtolye-202"
            return redirect("/SanalYetkisiz")
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = """UPDATE SKUsers SET AtolyeID = 0 WHERE UserID = ? AND AtolyeID = ?"""
        Params   = (UserID, AtolyeID)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sitemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üyenin Atölye'den Çıkartılma İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminAtolye-203"
            return redirect("/SanalStop")
        
        return redirect("/AdmUyeAtolyeleri")

    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminAtolye-299 ({e})"
        return redirect("/SanalError")
##############################################################################################################
@AdmUyeAtolyeleri.route("/AtolyeSilme/<string:AtolyeID>", methods=["POST"])
def ADM_ATOLYE_03(AtolyeID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminAtolye-301"
            return redirect("/SanalYetkisiz")

        try:
            AtolyeID = int(AtolyeID)
        except ValueError:
            current_app.config['Mesaj'] = "pyAdminAtolye-302"
            return redirect("/SanalYetkisiz")

        if AtolyeID <= 0:
            current_app.config['Mesaj'] = "pyAdminAtolye-303"
            return redirect("/SanalYetkisiz")

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = "DELETE FROM SKAtolye WHERE AtolyeID = ?"
        SQLCevap = SQLServer.Calistir(SQLKomut, (AtolyeID,))
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Atölye Silme İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminAtolye-304"
            return redirect("/SanalStop")
        
        return redirect("/AdmUyeAtolyeleri")

    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminAtolye-399 ({e})"
        return redirect("/SanalError")  
##############################################################################################################
@AdmUyeAtolyeleri.route("/YeniAtolyeKaydi", methods=["POST"])
def ADM_ATOLYE_04():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminAtolye-401"
            return redirect("/SanalYetkisiz")

        AtolyeAck = request.form.get("AtolyeAck", "").strip().upper()
        Aciklama = request.form.get("Aciklama", "").strip().upper()
        Acilis = request.form.get("Acilis", "")
        Kapanis = request.form.get("Kapanis", "")
        
        if not AtolyeAck or not Acilis or not Kapanis:
            current_app.config['Mesaj'] = "pyAdminAtolye-402"
            return redirect("/SanalYetkisiz")
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = """INSERT INTO SKAtolye (Durum, AtolyeAck, Acilis, Kapanis, GenelAck) VALUES (?, ?, ?, ?, ?)"""
        Params   = (1, AtolyeAck, Acilis, Kapanis, Aciklama)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Üyenin Atölye'ye Ekleme İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminAtolye-403"
            return redirect("/SanalStop")
        
        return redirect("/AdmUyeAtolyeleri")

    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminAtolye-499 ({e})"
        return redirect("/SanalError")
##############################################################################################################