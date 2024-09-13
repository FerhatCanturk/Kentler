import SQLServer

def Sabitler():
    SiteSabitleri = SQLServer.Sorgula("SELECT * FROM SKWebSabitler")
    Sabitler={
    'SiteSahibi': SiteSabitleri[0]["Sutun01"].strip(),
    'Unvan':      SiteSabitleri[0]["Sutun02"].strip(),
    'Slogan':     SiteSabitleri[0]["Sutun03"].strip(),
    'AdminMail':  SiteSabitleri[0]["Sutun08"].strip(),
    'Adres':      SiteSabitleri[0]["Sutun09"].strip(),
    'Telefon':    SiteSabitleri[0]["Sutun10"].strip(),
    'BankaSube':  SiteSabitleri[0]["Sutun11"].strip(),
    'IBANNo':     SiteSabitleri[0]["Sutun12"].strip(),
    'PassWord':   SiteSabitleri[0]["Sutun14"].strip(),
    'SmtpHost':   SiteSabitleri[0]["Sutun15"].strip(),
    'Port':       SiteSabitleri[0]["Sutun16"].strip(),
    'MsgSys':     str(SiteSabitleri[0]["Sutun13"])
    }
    return Sabitler