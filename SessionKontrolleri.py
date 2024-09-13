from flask import session
##############################################################################################################
##############################################################################################################
def AdminSessionKontrolu(IlaveSess):
     try:
          required_keys = [
               'SessionID', 'LocalStorage', 'ClientID', 'ClientName', 'AdminUlasim',
               'UserUlasim', 'SonHareket', 'ZiyaretciID', 'AdminMail', 'ModelSys',
               'SayfaAdim', 'DurumFiltreID', 'AdSoyadFiltre', 'IlkSatirIndis'
          ]
          if IlaveSess is None or IlaveSess == "":
               IlaveSess = []
          elif isinstance(IlaveSess, str):
               IlaveSess = [key.strip() for key in IlaveSess.split(',')]  # Convert string to list and strip spaces
          else:
               IlaveSess = [key.strip() for key in IlaveSess]             # Ensure it's a list of strings and strip spaces
          Kontrol = all(key in session for key in required_keys)
          
          if Kontrol and IlaveSess:
               Kontrol = all(key in session for key in IlaveSess)
          
          if Kontrol:
               Kontrol = (
                    int(session.get("AdminUlasim", 0)) == 1 and
                    int(session.get("UserUlasim", 0)) == 0 and
                    int(session.get("ClientID", 0)) > 0
               )
               for key in IlaveSess:
                    Kontrol = Kontrol and int(session.get(key, 0)) > 0

     except Exception:
          Kontrol = False
     finally:
          return not Kontrol
##############################################################################################################
def IndexSessionKontrolu(IlaveSess):
     try:
          required_keys = ['SessionID', 'LocalStorage', 'SonHareket', 'ZiyaretciID', 'AdminMail']
          if IlaveSess is None or IlaveSess == "":
               IlaveSess = []
          elif isinstance(IlaveSess, str):
               IlaveSess = [key.strip() for key in IlaveSess.split(',')]  # Convert string to list and strip spaces
          else:
               IlaveSess = [key.strip() for key in IlaveSess]             # Ensure it's a list of strings and strip spaces
          Kontrol = all(key in session for key in required_keys)
          
          if Kontrol and IlaveSess:
               Kontrol = all(key in session for key in IlaveSess)
          
     except Exception:
          Kontrol = False
     finally:
          return not Kontrol
##############################################################################################################