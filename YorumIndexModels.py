import SQLServer
import SQLToBase64
##############################################################################################################
def ModelSorgula(GrubID):
    SQLModeller  = f"""
    SELECT SKModels.*, SKGroups.GrubAdi, 
    FORMAT(ROUND(VerilenPuanToplami * 1.0 / VerilenPuanSayisi, 2), '0.00') AS OrtPuan, 
    (SELECT COALESCE(BinaryDosya, NULL) FROM SKPictures WHERE SKPictures.ModelID=SKModels.ModelID AND Sira = 1) AS Picture 
    FROM SKModels, SKGroups WHERE YayinDurumu = 1 AND SKModels.GrubID=SKGroups.GrubID AND SKModels.GrubID = ? 
    AND ModelID IN (SELECT ModelID FROM SKPictures WHERE SKPictures.ModelID=SKModels.ModelID AND Sira = 1)
    ORDER BY ModelAdi
    """
    Modeller = SQLToBase64.Resim(SQLServer.Sorgula(SQLModeller, (GrubID, )))
    return Modeller
##############################################################################################################
def GrubdakiModelRaporlari(GrubID):
    SQLModeller   = F"""
    SELECT (SELECT COUNT(*) FROM SKModels WHERE SKModels.YayinDurumu=1 AND SKModels.GrubID=SKGroups.GrubID ) AS MS
    , (SELECT SUM(ResimSayisi) FROM SKModels WHERE SKModels.YayinDurumu=1 AND SKModels.GrubID=SKGroups.GrubID) AS PS
    , (SELECT SUM(VideoSayisi) FROM SKModels WHERE SKModels.YayinDurumu=1 AND SKModels.GrubID=SKGroups.GrubID) AS VS
    , (SELECT SUM(VerilenPuanSayisi) FROM SKModels WHERE SKModels.YayinDurumu=1 AND SKModels.GrubID=SKGroups.GrubID) AS VPS
    , (SELECT SUM(VerilenPuanToplami) FROM SKModels WHERE SKModels.YayinDurumu=1 AND SKModels.GrubID=SKGroups.GrubID) AS VPT
    , ROUND(CAST((SELECT SUM(VerilenPuanToplami) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID) AS FLOAT) 
    / (SELECT SUM(VerilenPuanSayisi) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID), 2) AS VPO"
    FROM SKGroups WHERE GrubID = ?
    """
    GMR = SQLServer.Sorgula(SQLModeller, (GrubID, ))
    return GMR
##############################################################################################################
def GrubSorgulari():
    SQLSorgu = """
    SELECT *, (SELECT COUNT(*) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID AND YayinDurumu = 1) AS ModelSys
    , COALESCE(ROUND(CAST((SELECT SUM(VerilenPuanToplami) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID) AS FLOAT) 
    / (SELECT SUM(VerilenPuanSayisi) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID), 2), 0) AS ModelOrt
    FROM SKGroups WHERE GrubID IN (SELECT GrubID FROM SKModels) ORDER BY GrubAdi
    """
    Groups = SQLToBase64.Resim(SQLServer.Sorgula(SQLSorgu))
    return Groups
##############################################################################################################