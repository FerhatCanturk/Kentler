from flask import render_template, Blueprint, redirect, current_app, session
import SQLServer, YorumAdminModelDetails, SessionKontrolleri
##############################################################################################################
AdmModelDetails = Blueprint('AdmModelDetails', __name__, template_folder='templates')
##############################################################################################################
@AdmModelDetails.route("/AdmModelDetay", methods=["GET"])
def AnaSayfa():
    try:
        SessKontrol = SessionKontrolleri.AdminSessionKontrolu("ClientID, ModelID")
        if SessKontrol:
            current_app.config['Mesaj'] = "pyAdminModelDetay-101"
            return redirect("/SanalYetkisiz")
        
        YorumAdminModelDetails.SKDatabaseGuncelle()
        ModelID     = int(session.get("ModelID"))
        if ModelID <= 0:
            current_app.config['Mesaj'] = "pyAdminModelDetay-102"
            return redirect("/SanalYetkisiz")
        
        ModelPictures  = YorumAdminModelDetails.ModelResimler(ModelID)
        SQLKomut       = "SELECT ModelID, Sira FROM SKVideos WHERE ModelID = ? ORDER BY Sira"
        ModelVideos    = SQLServer.Sorgula(SQLKomut, (ModelID, ))

        SQLKomut      = "SELECT * FROM SKModels WHERE ModelID = ?"
        ModelAck      = SQLServer.Sorgula(SQLKomut, (ModelID, ))

        VideoKabul = 0; ResimKabul = 0
        if ModelAck[0]['ModelCins'].strip()[:6] == "ONLINE":
            if not ModelPictures:
                ResimKabul = 1
        else:
            VideoKabul = 1
            ResimKabul = 1
        Vmax = SQLServer.DegerGetir(f"SELECT COALESCE(MAX(Sira),0)+1 FROM SKVideos   WHERE ModelID = {ModelID}")
        Pmax = SQLServer.DegerGetir(f"SELECT COALESCE(MAX(Sira),0)+1 FROM SKPictures WHERE ModelID = {ModelID}")
        SiteOwner = current_app.config.get('BaseSabitler', {})
        if not(SiteOwner and ModelAck):
            current_app.config['Mesaj'] = F"pyAdminModelDetay-103"
            return redirect("/SanalError")
        
        return render_template("AdmModelDetails.html", SiteOwner = SiteOwner,
                    ModelAck = ModelAck, ModelPictures = ModelPictures, ModelVideos = ModelVideos, 
                    VideoKabul = VideoKabul, ResimKabul = ResimKabul, 
                    Vmax = Vmax, Pmax = Pmax)
    except Exception as e:
        current_app.config['Mesaj'] = f"pyAdminModelDetay-199 ({e})"
        return redirect("/SanalError")     
##############################################################################################################
