from flask import render_template, Blueprint, redirect, current_app, session, session
import SQLServer, YorumIndexSatisDetay, stripe, SessionKontrolleri
##############################################################################################################
IndexSepetIcerik = Blueprint('IndexSepet', __name__, template_folder='templates')
##############################################################################################################
##############################################################################################################
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'  # Test anahtarınızı buraya ekleyin

@IndexSepetIcerik.route("/IndexSepetGoster")
def SEPETDETAY00():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSepetDetay-001"
            return redirect("/SanalYetkisiz")
        
        SepetRows = YorumIndexSatisDetay.SepetIcerikDetaylari()
        SepetTotal = YorumIndexSatisDetay.SepetToplami()
        Siparis = session.get("SessionID")
        SiteOwner   = current_app.config.get('BaseSabitler', {})
        if not(SiteOwner):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyIndexSepetDetay-002"
            return redirect("/SanalStop")
        
        if not(SepetRows):
            return redirect("/IndexSatislar")
        
        return render_template('IndexSepet.html', SiteOwner = SiteOwner, 
                                SepetRows = SepetRows, SepetTotal = SepetTotal, Siparis = Siparis)
    except Exception as e:
          current_app.config['Mesaj']  = "pyIndexSepetDetay-099"
          return redirect("/SanalError")
##############################################################################################################
@IndexSepetIcerik.route("/SepetBosalt")
def SEPETDETAY01():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSepetDetay-101"
            return redirect("/SanalYetkisiz")
        
        SessionID = session.get("SessionID")
        CihazKodu = str(session.get("LocalStorage"))
        UserID    = 0
        if 'ClientID' in session:
            UserID = session.get("ClientID")
        
        SQLKomut = f"DELETE FROM SKAlisVeris WHERE (UserID = ? AND ? > 0) OR SessionID = ? OR CihazKodu = ?"
        Params   = (UserID, UserID, SessionID, CihazKodu)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sepeti Boşaltma İşlemi Başarısız Oldu"
            current_app.config['Mesaj3'] = "pyIndexSepetDetay-102"
            return redirect("/SanalStop")
        
        return redirect("/IndexSepetGoster")
    except Exception as e:
        current_app.config['Mesaj']  = "pyIndexSepetDetay-199"
        return redirect("/SanalError")
##############################################################################################################
@IndexSepetIcerik.route("/SepetSatirSil/<string:ModelID>", methods=['POST'])
def SEPETDETAY02(ModelID):
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSepetDetay-201"
            return redirect("/SanalYetkisiz")
        
        SessionID = session.get("SessionID")
        CihazKodu = str(session.get("LocalStorage"))
        UserID    = 0
        if 'ClientID' in session:
            UserID = session.get("ClientID")
        
        SQLKomut = """DELETE FROM SKAlisVeris WHERE ModelID = ? AND ((UserID = ? or ? > 0) OR SessionID = ? OR CihazKodu = ?)"""
        Params   = (ModelID, UserID, UserID, SessionID, CihazKodu)
        SQLCevap = SQLServer.Calistir(SQLKomut, Params)
        if SQLCevap:
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sepetten Silme İşlemi Başarısız Oldu"
            current_app.config['Mesaj3'] = "pyIndexSepetDetay-202"
            return redirect("/SanalStop")
        
        return redirect("/IndexSepetGoster")
    except Exception as e:
        current_app.config['Mesaj']  = "pyIndexSepetDetay-299"
        return redirect("/SanalError")
##############################################################################################################
@IndexSepetIcerik.route("/SendPay", methods=['POST'])
def SEPETDETAY03():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSepetDetay-301"
            return redirect("/SanalYetkisiz")
        
        SepetTotal  = YorumIndexSatisDetay.SepetToplami()
        SiteOwner   = current_app.config.get('BaseSabitler', {})
        if not(SiteOwner):
            current_app.config['Mesaj1'] = "Beklenilmeyen Sistemsel Hata Meydana Geldi"
            current_app.config['Mesaj2'] = "Sayfa Yükleme Hatası"
            current_app.config['Mesaj3'] = "pyIndexSepetDetay-302"
            return redirect("/SanalStop")
        
        return render_template("/Pay.html", SiteOwner = SiteOwner, 
                               SepetTotal = SepetTotal)
    except Exception as e:
        current_app.config['Mesaj']  = "pyIndexSepetDetay-399"
        return redirect("/SanalError")
##############################################################################################################
@IndexSepetIcerik.route("/OdemeSorgulari", methods=['POST'])
def SEPETDETAY04():
    try:
        if SessionKontrolleri.IndexSessionKontrolu(""):
            current_app.config['Mesaj'] = "pyIndexSepetDetay-401"
            return redirect("/SanalYetkisiz")
        
        card_number = "4242424242424242"  # Stripe test kart numarası
        card_name = "FERHAT CANTÜRK"
        expiry_date = "06/25"
        cvv = "611"
        
        # Kart bilgilerini Stripe Token'ına dönüştürmek için Stripe API'sini kullanın
        try:
            token = stripe.Token.create(
                card={
                    "number": card_number,
                    "exp_month": int(expiry_date.split('/')[0]),
                    "exp_year": int(expiry_date.split('/')[1]),
                    "cvc": cvv,
                    "name": card_name
                }
            )
            
            # Stripe ödemesi oluşturun
            charge = stripe.Charge.create(
                amount=5000,  # Ödeme miktarını kuruş cinsinden belirtin (örneğin, 50.00 USD için 5000)
                currency='usd',
                description='Ödeme Açıklaması',
                source=token.id
            )
            current_app.config['Mesaj1']       = "Teşekkür Ederiz"
            current_app.config['Mesaj2']       = "Ödemenizi Aldık"
            return redirect("/SanalOK")    
        except stripe.error.CardError as e:
            current_app.config['Mesaj1']    = "Ödeme Esnasında Hata Oluştu"
            current_app.config['Mesaj2']    = "Bilgilerinizi Kontrol Ederek Tekrar Deneyiniz"
            current_app.config['Mesaj3']    = "pyIndexSepetDetay-402"
            return redirect("/SanalStop")
    except Exception as e:
        current_app.config['Mesaj']  = "pyIndexSepetDetay-499"
        return redirect("/SanalError")
##############################################################################################################