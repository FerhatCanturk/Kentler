import SQLServer

def Sabitler():
    SiteSabitleri = SQLServer.Sorgula("SELECT * FROM SKWebSabitler")
    if not SiteSabitleri:
        # Return a dictionary with default values if no records are found
        return {
            'SiteSahibi': '',
            'Unvan': '',
            'Slogan': '',
            'AdminMail': '',
            'Adres': '',
            'Telefon': '',
            'BankaSube': '',
            'IBANNo': '',
            'PassWord': '',
            'SmtpHost': '',
            'Port': '',
            'MsgSys': ''
        }
    Sabitler={
    'SiteSahibi': SiteSabitleri[0].get("Sutun01", "").strip(),
    'Unvan':      SiteSabitleri[0].get("Sutun02","").strip(),
    'Slogan':     SiteSabitleri[0].get("Sutun03","").strip(),
    'AdminMail':  SiteSabitleri[0].get("Sutun08","").strip(),
    'Adres':      SiteSabitleri[0].get("Sutun09","").strip(),
    'Telefon':    SiteSabitleri[0].get("Sutun10","").strip(),
    'BankaSube':  SiteSabitleri[0].get("Sutun11","").strip(),
    'IBANNo':     SiteSabitleri[0].get("Sutun12","").strip(),
    'PassWord':   SiteSabitleri[0].get("Sutun14","").strip(),
    'SmtpHost':   SiteSabitleri[0].get("Sutun15","").strip(),
    'Port':       SiteSabitleri[0].get("Sutun16","").strip(),
    'MsgSys':     str(SiteSabitleri[0].get("Sutun13"),"")
    }
    return Sabitler
