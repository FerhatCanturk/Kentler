from flask import render_template, Blueprint, redirect, current_app, session
import SQLServer, YorumAdminModelAcma, SessionKontrolleri
##############################################################################################################
AdmUserModelAcKapa = Blueprint('AdmUserModelAcKapa', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@AdmUserModelAcKapa.route("/AdmModelAcKapat", methods=["GET"])
def ADMMODELACMA00():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ClientID")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminModelYetkilendirme-001"
            return redirect("/SanalYetkisiz")
        
        SayfaAdim = int(session.get("ModelSayfaAdim"))
        UserID    = int(session.get('UserID'))
        IlkSatir  = int(session.get('ModelAcKapatIlkSatir'))
    
        ModelSys = int(session.get('ModelSys'))
        if IlkSatir > ModelSys:
                IlkSatir = IlkSatir - SayfaAdim + 1
        
        if int(IlkSatir) < 1:
            IlkSatir = 1
        SonSatir = IlkSatir + SayfaAdim - 1
        
        if int(ModelSys) < SonSatir:
            SonSatir = int(ModelSys)
        
        session['ModelAcKapatIlkSatir'] = IlkSatir
        Models = []
        Models = YorumAdminModelAcma.ModelAcma(UserID, IlkSatir, SayfaAdim) 
        User   = YorumAdminModelAcma.KullanicilarListesi(0, 10, 0, "", UserID)
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not(Models and User and SiteOwner):
            current_app.config['Mesaj']    = "pyAdminModelYetkilendirme-002"
            return redirect("/SanalError")
        
        return render_template("AdmModelAcKapat.html", SiteOwner = SiteOwner, 
                        User = User, IlkSatir = IlkSatir, ToplamModelSys = ModelSys, 
                        SonSatir = SonSatir, Models = Models)
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModelYetkilendirme-099 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmUserModelAcKapa.route('/ModelAcmaSonraki', methods=["POST"])
def ADMMODELACMA01():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ClientID, ModelAcKapatIlkSatir")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminModelYetkilendirme-101"
            return redirect("/SanalYetkisiz")
        
        SayfaAdim     = int(session.get("ModelSayfaAdim"))
        IlkSatir      = int(session.get('ModelAcKapatIlkSatir'))
        
        session["ModelAcKapatIlkSatir"] = IlkSatir + SayfaAdim 
        return redirect("/AdmModelAcKapat")
    except Exception as e:
        current_app.config['Mesaj']     = f"pyAdminModelYetkilendirme-199 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmUserModelAcKapa.route('/ModelAcmaOnceki', methods=["POST"])
def ADMMODELACMA02():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ClientID, ModelAcKapatIlkSatir")
        if SessKontrol:
            current_app.config['Mesaj']   = "pyAdminModelYetkilendirme-201"
            return redirect("/SanalYetkisiz")
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SayfaAdim   = int(session.get("ModelSayfaAdim"))
        IlkSatir    = int(session.get('ModelAcKapatIlkSatir'))
        session["ModelAcKapatIlkSatir"] = IlkSatir - SayfaAdim 
        return redirect("/AdmModelAcKapat")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModelYetkilendirme-299 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmUserModelAcKapa.route('/ModelGoster/<string:ModelID>', methods=["POST"])
def ADMMODELACMA03(ModelID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ClientID, ModelAcKapatIlkSatir")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModelYetkilendirme-301"
            return redirect("/SanalYetkisiz")
        
        if ModelID is None or int(ModelID) == 0:
            current_app.config['Mesaj']    = "pyAdminModelYetkilendirme-302"
            return redirect("/SanalYetkisiz")
        
        UserID   = int(session.get('UserID'))
        if UserID is None or int(UserID) == 0:
            current_app.config['Mesaj']    = "pyAdminModelYetkilendirme-303"
            return redirect("/SanalYetkisiz")
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = f"INSERT INTO SKMemberSingleProjects (UserID, ModelID) VALUES (?, ?)"
        Params   = (UserID, ModelID)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1']    = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2']    = "Üyeye Modelin Açılma İşlemi Yapılamadı"
            current_app.config['Mesaj3']    = "pyAdminModelYetkilendirme-304"
            return redirect("/SanalStop")
        
        return redirect("/AdmModelAcKapat")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminModelYetkilendirme-399 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmUserModelAcKapa.route('/ModelGizle/<string:ModelID>', methods=["POST"])
def ADMMODELACMA04(ModelID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ClientID, ModelAcKapatIlkSatir")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModelYetkilendirme-401"
            return redirect("/SanalYetkisiz")
        
        if ModelID is None or int(ModelID) == 0:
            current_app.config['Mesaj']    = "pyAdminModelYetkilendirme-402"
            return redirect("/SanalYetkisiz")
        
        UserID   = int(session.get('UserID'))
        if UserID is None or int(UserID) == 0:
            current_app.config['Mesaj']    = "pyAdminModelYetkilendirme-403"
            return redirect("/SanalYetkisiz")
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SQLKomut = "DELETE FROM SKMemberSingleProjects WHERE UserID = ? AND ModelID = ?"
        Params   = (UserID, ModelID)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1']    = "Beklenilmeyen Sistemsel Bir Hata Meydana Geldi"
            current_app.config['Mesaj2']    = "Üyeye Modelin Gizleme İşlemi Yapılamadı"
            current_app.config['Mesaj3']    = "pyAdminModelYetkilendirme-404"
            return redirect("/SanalStop")
        
        return redirect("/AdmModelAcKapat")
    except Exception as e:
        current_app.config['Mesaj']    = f"pyAdminModelYetkilendirme-499 ({e})"
        return redirect("/SanalError")     
##############################################################################################################