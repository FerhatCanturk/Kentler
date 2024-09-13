from flask import session
import SQLServer, SQLToBase64
def SepetIcerikDetaylari():
    SessionID = session.get("SessionID")
    CK = str(session.get("LocalStorage"))
    if 'ClientID' not in session:
        UserID = 0
    else:
        UserID = session.get("ClientID")
    EkSorgu = f"(SA.SessionID = {SessionID} OR (SA.UserID = {UserID} AND {UserID} > 0) OR CihazKodu = '{CK}')"
    

    SepetRows = f"""
        SELECT SK.ModelID, SK.ModelAdi
        , (SELECT COUNT(*) FROM SKAlisVeris AS SA WHERE SA.ModelID=SK.ModelID AND 
		{EkSorgu}
		
		) AS Miktar
        , SK.Fiyati
        , (SELECT COUNT(*) FROM SKAlisVeris AS SA WHERE SA.ModelID=SK.ModelID AND 
		{EkSorgu}
		
		)*SK.Fiyati AS Tutari
		FROM SKModels AS SK WHERE ModelID IN (SELECT ModelID FROM SKAlisVeris AS SA where 
		{EkSorgu}
        )
		"""
    
    SepetRows = SQLServer.Sorgula(SepetRows)
    return SepetRows
##############################################################################################################
def SepetToplami():
    SessionID = session.get("SessionID")
    CK = str(session.get("LocalStorage"))
    if 'ClientID' not in session:
        UserID = 0
    else:
        UserID = session.get("ClientID")

    SepetTotal = f"""SELECT COALESCE(COUNT(*),0) AS SepetSys, COALESCE(SUM(Fiyati),0) AS SepetTutari FROM SKAlisVeris, SKModels 
                        WHERE SKAlisVeris.ModelID=SKModels.ModelID 
                        AND (SKAlisVeris.SessionID = {SessionID} OR (SKAlisVeris.UserID = {UserID} AND {UserID} > 0 ) OR SKAlisVeris.CihazKodu = '{CK}')"""
    SepetTotal = SQLServer.Sorgula(SepetTotal)
    return SepetTotal
##############################################################################################################
