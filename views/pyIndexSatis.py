from flask import render_template, Blueprint, redirect, current_app, session, session
import SQLServer, YorumIndexSatis, SessionKontrolleri
##############################################################################################################
IndexSatis = Blueprint('IndexSatislar', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
@IndexSatis.route("/IndexSatislar")
def SATISLAR00():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSatislar-001"
            return redirect("/SanalYetkisiz")

        if 'ShoppingGrubu' not in session:
            GrubID = "SELECT COALESCE(GrubID, 0) FROM SKGroups WHERE GrubID IN (SELECT GrubID FROM SKModels)"
            GrubID = SQLServer.DegerGetir(GrubID)
        else:
            GrubID = session.get("ShoppingGrubu")
        
        Shoppings = []
        GrubID    = int(GrubID)
        if GrubID > 0:
            Shoppings = YorumIndexSatis.ModelSorgula(GrubID)
            for Shop in Shoppings:
                OrtPuan = float(Shop.get("OrtPuan", 0))
                Shop["OrtPuani"] = int(OrtPuan)
                if "OrtPuan" in Shop:
                    del Shop["OrtPuan"]

        Groups       = YorumIndexSatis.GrubSorgulari()
        SepetToplami = YorumIndexSatis.SepetToplami()
        SiteOwner    = current_app.config.get('BaseSabitler', {})
        if not (SiteOwner):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyIndexKK-002"
            return redirect("/SanalStop")
        
        return render_template('IndexSatis.html', SiteOwner = SiteOwner, Groups = Groups, Shoppings = Shoppings, Sepet = SepetToplami)
    except Exception as e:
          current_app.config['Mesaj'] = f"pyIndexSatislar-099 ({e})"
          return redirect("/SanalError")
##############################################################################################################
@IndexSatis.route("/ModelPuanla/<string:ModelID>/<string:Point>", methods=['POST'])
def SATISLAR012(ModelID, Point):
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSatislar-101"
            return redirect("/SanalYetkisiz")
        
        if "ClientID" in session:
            UserID = session.get('ClientID').strip()
            if ClientID>1:
                
        
        return redirect("/IndexSatislar")
    except Exception as e:
          current_app.config['Mesaj'] = "pyIndexSatislar-199"
          return redirect("/SanalError")
##############################################################################################################
  
@IndexSatis.route("/Shopping/<string:GrubID>", methods=['POST'])
def SATISLAR01(GrubID):
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSatislar-101"
            return redirect("/SanalYetkisiz")
        
        session['ShoppingGrubu'] = GrubID
        return redirect("/IndexSatislar")
    except Exception as e:
          current_app.config['Mesaj'] = "pyIndexSatislar-199"
          return redirect("/SanalError")
##############################################################################################################
@IndexSatis.route("/SepeteGonder/<string:ModelID>", methods=['POST'])
def SATISLAR02(ModelID):
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSatislar-201"
            return redirect("/SanalYetkisiz")
        
        SessionID = session.get("SessionID")
        CihazKodu = str(session.get("LocalStorage"))
        UserID    = 0
        if 'ClientID' in session:
            UserID = session.get("ClientID")

        SQLKomut = "INSERT INTO SKAlisVeris (UserID, SessionID, ModelID, Miktar, CihazKodu) VALUES (?, ?, ?, ?, ?)"
        Params   = (UserID, SessionID, ModelID, 1, CihazKodu)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sepete Gönderilme İşlemi Başarısız Oldu"
            current_app.config['Mesaj3'] = "pyIndexKK-002"
            return redirect("/SanalStop")
        
        return redirect("/IndexSatislar")
    except Exception as e:
          current_app.config['Mesaj'] = "pyIndexSatislar-299"
          return redirect("/SanalError")
##############################################################################################################
@IndexSatis.route("/SepetGoruntule")
def SATISLAR03():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSatislar-301"
            return redirect("/SanalYetkisiz")
        
        return redirect("/IndexSepetGoster")
    except Exception as e:
          current_app.config['Mesaj'] = "pyIndexSatislar-399"
          return redirect("/SanalError")
##############################################################################################################