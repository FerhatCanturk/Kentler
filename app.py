###############################################################################################################    
import time, os, SQLServer, SiteSabit
from flask import Flask, session
###############################################################################################################    
from views                                import Index
from views.pyIndexKK                      import IndexKK
from views.pyIndexSosyal                  import IndexSosyal
from views.pyIndexSatis                   import IndexSatis
from views.pyIndexSatisDetay              import IndexSepetIcerik
from views.pyMesajlar                     import Messages
from views.pyIndexUyeGiris                import UyeGiris
from views.pyIndexUyeOlun                 import UyeOlun
from views.pyAdminKullanicilar            import AdmKullanicilar
from views.pyAdminModelAcma               import AdmUserModelAcKapa
from views.pyAdminKullaniciZamanCizelgesi import AdmUserDetaySayfasi
from views.pyAdminAtolyeIslem             import AdmUyeAtolyeleri
from views.pyAdminModels                  import AdmModels
from views.pyAdminModelDetails            import AdmModelDetails
from views.pyAdminMediaIslemleri          import Media
from views.pyAdminEtkinlikIslem           import Etkinlik
from views.pyAdminMessages                import AdmMessages
from views.pyAdminWEBSettings             import AdmSettings
from views.pyLocalStorage                 import LocalStorage
# ##############################################################################################################
# # Blueprint'leri kaydet
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_PERMANENT']        = False
app.config['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
app.config['UPLOAD_FOLDER']                   = 'static/images'
###############################################################################################################
app.register_blueprint(Index)
app.register_blueprint(IndexKK)
app.register_blueprint(IndexSosyal)
app.register_blueprint(IndexSatis)
app.register_blueprint(IndexSepetIcerik)
app.register_blueprint(Messages)
app.register_blueprint(UyeGiris)
app.register_blueprint(UyeOlun)
app.register_blueprint(AdmKullanicilar)
app.register_blueprint(AdmUserModelAcKapa)
app.register_blueprint(AdmUserDetaySayfasi)
app.register_blueprint(AdmUyeAtolyeleri)
app.register_blueprint(AdmModels)
app.register_blueprint(AdmModelDetails)
app.register_blueprint(Media)
app.register_blueprint(Etkinlik)
app.register_blueprint(AdmMessages)
app.register_blueprint(AdmSettings)
app.register_blueprint(LocalStorage)
# ##############################################################################################################
app.config['BaseSabitler'] = SiteSabit.Sabitler()
# ##############################################################################################################
@app.before_request
def SessionSuresiSinirlama():
    if 'SonHareketZamani' in session:
        if time.time() - session['SonHareket'] > 30 * 60:  # 30 dakika
            # session.pop('SessionID',  None)
            # session.pop('SonHareket', None)
            # session.pop('AdminMail',  None)
            session.clear()
        else:
            #session['SessionID']  = str(random.randint(100000, 999999))
            #session['SonHareket'] = time.time()
            session['AdminMail']  = SQLServer.DegerGetir("SELECT Sutun08 FROM SKWebSabitler").strip()
###############################################################################################################    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
    #ngrok http 5000
###############################################################################################################    


