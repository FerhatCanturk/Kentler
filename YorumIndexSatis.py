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
def ModelSorgula(GrubID):
    SQLModeller  = f"""
    SELECT SKModels.*, SKGroups.GrubAdi, 
    FORMAT(ROUND(VerilenPuanToplami * 1.0 / VerilenPuanSayisi, 2), '0.00') AS OrtPuan, 
    (SELECT COALESCE(BinaryDosya, NULL) FROM SKPictures WHERE SKPictures.ModelID=SKModels.ModelID AND Sira = 1) AS Picture 
    FROM SKModels, SKGroups WHERE YayinDurumu = 1 AND SKModels.GrubID=SKGroups.GrubID AND SKModels.GrubID={GrubID} 
    AND ModelID IN (SELECT ModelID FROM SKPictures WHERE SKPictures.ModelID=SKModels.ModelID AND Sira = 1)
    ORDER BY ModelAdi
    """
    Modeller = SQLToBase64.Resim(SQLServer.Sorgula(SQLModeller))
    return Modeller
##############################################################################################################
def GrubSorgulari():
    SQLSorgu = """
    SELECT *, (SELECT COUNT(*) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID AND YayinDurumu = 1) AS ModelSys
    , COALESCE(ROUND(CAST((SELECT SUM(VerilenPuanToplami) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID) AS FLOAT) 
    / (SELECT SUM(VerilenPuanSayisi) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID), 2), 0) AS ModelOrt
    FROM SKGroups WHERE GrubID IN (SELECT GrubID FROM SKModels) ORDER BY GrubAdi
    """
    Groups = SQLServer.Sorgula(SQLSorgu)
    return Groups