import SQLServer
import SQLToBase64

def OrguModelleriSorgusu(GrubFiltre, SiralamaFiltre):
    SiralamaFiltre = int(SiralamaFiltre)
    if SiralamaFiltre<2:
        SiralamaFiltre="ORDER BY YayinDurumu*SIGN(ResimSayisi)*SIGN(ResimSayisi), SModelAdi"
    elif SiralamaFiltre==2:
        SiralamaFiltre="ORDER BY YayinDurumu*SIGN(ResimSayisi)*SIGN(ResimSayisi), ModelAdi DESC"
    elif SiralamaFiltre==3:
        SiralamaFiltre="ORDER BY YayinDurumu*SIGN(ResimSayisi)*SIGN(ResimSayisi), YayinTarihi"
    elif SiralamaFiltre==4:
        SiralamaFiltre="ORDER BY YayinDurumu*SIGN(ResimSayisi)*SIGN(ResimSayisi), YayinTarihi DESC"
    elif SiralamaFiltre==5:
        SiralamaFiltre="ORDER BY YayinDurumu*SIGN(ResimSayisi)*SIGN(ResimSayisi), Fiyati"
    elif SiralamaFiltre==6:
        SiralamaFiltre="ORDER BY YayinDurumu*SIGN(ResimSayisi)*SIGN(ResimSayisi), Fiyati DESC"
    else: 
        SiralamaFiltre = ""

    Models = f"""
            SELECT *,  
            CASE WHEN VerilenPuanSayisi>0 THEN FORMAT(ROUND(CAST(VerilenPuanToplami AS FLOAT) / (VerilenPuanSayisi), 2),'0.00') ELSE '0.00' END AS OrtPuan
            ,

            CASE WHEN (SKModels.ModelCins LIKE 'EXTRA%' OR SKModels.ModelCins LIKE 'ONLINE%') OR SKModels.YayinDurumu = 0 THEN 0
            ELSE
            (SELECT COUNT(*) FROM SKUsers, SKMemberDates
            WHERE SKUsers.UserID=SKMemberDates.UserID 
            AND SKUsers.DurumID > 21 AND SKUsers.DurumID < 81
            AND SKModels.YayinTarihi BETWEEN SKMemberDates.BaslamaTarihi AND COALESCE(SKMemberDates.SonlanmaTarihi,'2222-12-31')) END AS GorenUserSys
            ,

            (SELECT BinaryDosya FROM SKPictures WHERE Sira=1 AND SKPictures.ModelID = SKModels.ModelID) AS Picture,

            CASE WHEN SKModels.ModelCins LIKE 'ONLINE%' OR SKModels.YayinDurumu = 0 THEN 0
            ELSE (SELECT COUNT(*) FROM SKUsers, SKMemberDates, SKMemberSingleProjects            
            WHERE SKUsers.UserID=SKMemberDates.UserID 
            AND SKMemberSingleProjects.ModelID = SKModels.ModelID
            AND SKMemberSingleProjects.UserID = SKUsers.UserID AND SKUsers.DurumID > 21 AND SKUsers.DurumID < 81) END AS SingleSatis
            FROM SKModels, SKGroups WHERE SKModels.GrubID=SKGroups.GrubID
            AND (SKModels.GrubID={GrubFiltre} or {GrubFiltre}=0) {SiralamaFiltre}
"""
    Models = SQLServer.Sorgula(Models)
    Models = SQLToBase64.Resim(Models)
    return Models


