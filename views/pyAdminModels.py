from   flask import render_template, Blueprint, redirect, current_app, session, request
import SQLServer, YorumAdminModels, YorumAdminMediaIslemleri, SessionKontrolleri
from datetime import datetime, timedelta
##############################################################################################################
AdmModels = Blueprint('AdmModels', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@AdmModels.route("/AdmModels", methods=["GET"])
def ADMMODELS00():
    # Bu AltYordam Base.Html Tarafından Tetiklenir
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-001"
            return redirect("/SanalYetkisiz")
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        
        if "GrubFiltreID" not in session:
            session["GrubFiltreID"]     = int(SQLServer.DegerGetir("SELECT GrubID FROM SKGroups"))
        
        if "SiralamaFiltreID" not in session:
            session["SiralamaFiltreID"] = "4"

        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-099 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/AdmModelsAnaSayfasi", methods=["GET"])
def ADMMODELS01():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-101"
            return redirect("/SanalYetkisiz")
        
        GrubFiltreID     = int(session.get("GrubFiltreID"))
        SiralamaFiltreID = int(session.get("SiralamaFiltreID"))
        FGroups          = SQLServer.Sorgula("SELECT * FROM SKGroups WHERE GrubID IN (SELECT GrubID FROM SKModels) ORDER BY GrubAdi")
        Groups           = SQLServer.Sorgula("SELECT * FROM SKGroups ORDER BY GrubAdi")
        Models           = YorumAdminModels.OrguModelleriSorgusu(GrubFiltreID, SiralamaFiltreID)
        
        Bugun    = datetime.now().date()
        MaxTarih = Bugun + timedelta(days = 30)
        MinTarih = Bugun + timedelta(days = -30)

        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not SiteOwner:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyAdminModels-102"
            return redirect("/SanalStop")
        
        return render_template("AdmModels.html", SiteOwner = SiteOwner,
                            Groups = Groups, FGroups = FGroups, Models = Models,
                            GrubFiltreID = GrubFiltreID, SiralamaFiltreID = SiralamaFiltreID, 
                            MinTarih=MinTarih, Bugun=Bugun, MaxTarih = MaxTarih)
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-199 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/ModelGrubFiltre", methods=["GET", "POST"])
def ADMMODELS02():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-201"
            return redirect("/SanalYetkisiz")
        
        GrubFiltreID = request.form.get('GrubID')
        if not GrubFiltreID:
            current_app.config['Mesaj']    = "pyAdminModels-202"
            return redirect("/SanalYetkisiz")
        
        GrubFiltreID = int(GrubFiltreID)
        if GrubFiltreID < 0:
            current_app.config['Mesaj']    = "pyAdminModels-203"
            return redirect("/SanalYetkisiz")
        
        session["GrubFiltreID"] = GrubFiltreID
        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-299 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/ModelSiralamaFiltre", methods=["GET", "POST"])
def ADMMODELS03():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-301"
            return redirect("/SanalYetkisiz")
                
        SiralamaID     = request.form.get('SiralamaID')
        if not SiralamaID:
            current_app.config['Mesaj']    = "pyAdminModels-303"
            return redirect("/SanalYetkisiz")
        
        SiralamaID = int(SiralamaID)
        if SiralamaID <= 0:
            current_app.config['Mesaj']    = "pyAdminModels-304"
            return redirect("/SanalYetkisiz")
        
        session["SiralamaFiltreID"] = SiralamaID
        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-399 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/YeniModelKaydet", methods=["GET","POST"])
def ADMMODELS04():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-401"
            return redirect("/SanalYetkisiz")
        
        ModelTarih  = request.form.get('ModelTarih1')
        ModelCins   = request.form.get('ModelCins1')
        ModelGrubID = request.form.get('GrubID1')
        ModelAdi    = request.form.get('ModelAdi1').upper().strip()
        ModelFiyati = request.form.get('ModelFiyati1')

        if not all([ModelTarih, ModelCins, ModelGrubID, ModelAdi, ModelFiyati]):
            current_app.config['Mesaj']    = "pyAdminModels-402"
            return redirect("/SanalYetkisiz")

        SQLKomut    = """INSERT INTO SKModels 
                    (YayinTarihi, ModelCins, GrubID, ModelAdi, Fiyati, VerilenPuanSayisi, VerilenPuanToplami, VideoSayisi, ResimSayisi, YayinDurumu) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        Params     = (ModelTarih, ModelCins, ModelGrubID, ModelAdi, ModelFiyati, 1, 5, 0, 0, 0)
        SQLCevap   = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1']    = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2']    = "Yeni Modelin Kayıt İşlemi Yapılamadı"
            current_app.config['Mesaj3']    = "pyAdminModelYetkilendirme-403"
            return redirect("/SanalStop")
        
        session["GrubFiltreID"] = ModelGrubID
        session["SiralamaFiltreID"] = 4
        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-499 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/ModelSilme/<string:ModelID>", methods=["POST"])
def ADMMODELS05(ModelID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-501"
            return redirect("/SanalYetkisiz")
        
        ModelID = int(ModelID)
        if ModelID <= 0:
            current_app.config['Mesaj']    = "pyAdminModels-502"
            return redirect("/SanalYetkisiz")
        
        SQLKomut = "DELETE FROM SKModels WHERE ModelID = ? and ResimSayisi = 0 and VideoSayisi = 0"
        SQLCevap = SQLServer.Calistir(SQLKomut, (ModelID, ))
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Modelin Silinme İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminModelYetkilendirme-502"
            return redirect("/SanalStop")
        
        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-599 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/ModelDegistir/<string:ModelID>", methods=["POST"])
def ADMMODELS06(ModelID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-601"
            return redirect("/SanalYetkisiz")
        
        ModelTarih  = request.form.get(f'ModelTarih2_{ModelID}')
        ModelCins   = request.form.get(f'ModelCins2_{ModelID}')
        ModelGrubID = request.form.get(f'GrubID2_{ModelID}')
        ModelAdi    = request.form.get(f'ModelAdi2_{ModelID}').upper().strip()
        ModelFiyati = request.form.get(f'ModelFiyati2_{ModelID}')

        if not all([ModelTarih, ModelCins, ModelGrubID, ModelAdi, ModelFiyati]):
            current_app.config['Mesaj']    = "pyAdminModels-602"
            return redirect("/SanalYetkisiz")

        SQLKomut    = "UPDATE SKModels SET YayinTarihi = ?, ModelCins = ?, GrubID = ?, ModelAdi = ?, Fiyati = ? WHERE ModelID = ?"
        Params      = (ModelTarih, ModelCins, ModelGrubID, ModelAdi, ModelFiyati, ModelID)
        SQLCevap    = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Modelin Değiştirilme İşlemi Yapılamadı"
            current_app.config['Mesaj3'] = "pyAdminModelYetkilendirme-603"
            return redirect("/SanalStop")
        
        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-699 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/ModelYayinaGonder/<string:ModelID>", methods=["POST"])
def ADMMODELS07(ModelID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-701"
            return redirect("/SanalYetkisiz")
        
        ModelID = int(ModelID)
        if ModelID <= 0:
            current_app.config['Mesaj']    = "pyAdminModels-702"
            return redirect("/SanalYetkisiz")
        
        SQLKomut = "UPDATE SKModels SET YayinDurumu = 1 WHERE ModelID = ?"
        SQLCevap = SQLServer.Calistir(SQLKomut, (ModelID, ))
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Model Yayına Gönderilemedi"
            current_app.config['Mesaj3'] = "pyAdminModelYetkilendirme-703"
            return redirect("/SanalStop")
        
        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-799 ({e})"
        return redirect("/SanalError")    
##############################################################################################################
@AdmModels.route("/ModelYayindanCek/<string:ModelID>", methods=["POST"])
def ADMMODELS08(ModelID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj']    = "pyAdminModels-801"
            return redirect("/SanalYetkisiz")
        
        ModelID = int(ModelID)
        if ModelID <= 0:
            current_app.config['Mesaj']    = "pyAdminModels-802"
            return redirect("/SanalYetkisiz")
        
        SQLKomut = "UPDATE SKModels SET YayinDurumu = 0 WHERE ModelID = ?"
        SQLCevap = SQLServer.Calistir(SQLKomut, (ModelID, ))
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Model Yayından Çekilemedi"
            current_app.config['Mesaj3'] = "pyAdminModelYetkilendirme-803"
            return redirect("/SanalStop")
        
        return redirect("/AdmModelsAnaSayfasi")
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-899 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
@AdmModels.route("/ModelDetay/<string:ModelID>", methods=["POST"])
def ADMMODELS09(ModelID):
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("GrubFiltreID, SiralamaFiltreID")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminModels-901"
            return redirect("/SanalYetkisiz")
        
        ModelID = int(ModelID)
        if ModelID <= 0:
            current_app.config['Mesaj'] = "pyAdminModels-902"
            return redirect("/SanalYetkisiz")
        
        YorumAdminMediaIslemleri.SKDatabaseGuncelle()
        session["ModelID"] = str(ModelID)
        return redirect("/AdmModelDetay")
                
    except Exception as e:
        current_app.config['Mesaj']   = f"pyAdminModels-999 ({e})"
        return redirect("/SanalError")    
##############################################################################################################
