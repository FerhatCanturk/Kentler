import SQLServer
import SQLToBase64
import Formatlama 
import Sifreleme

def OrguModelleriSorgusu(GrubFiltre, SiralamaFiltre):
    SiralamaFiltre = int(SiralamaFiltre)
    if SiralamaFiltre<2:
        SiralamaFiltre="ORDER BY ModelAdi"
    elif SiralamaFiltre==2:
        SiralamaFiltre="ORDER BY ModelAdi DESC"
    elif SiralamaFiltre==3:
        SiralamaFiltre="ORDER BY YayinTarihi"
    elif SiralamaFiltre==4:
        SiralamaFiltre="ORDER BY YayinTarihi DESC"
    elif SiralamaFiltre==5:
        SiralamaFiltre="ORDER BY Fiyati"
    elif SiralamaFiltre==6:
        SiralamaFiltre="ORDER BY Fiyati DESC"
    else: 
        SiralamaFiltre = ""

    Models = f"""
            SELECT *,  
            CASE WHEN VerilenPuanSayisi>0 THEN FORMAT(ROUND(CAST(VerilenPuanToplami AS FLOAT) / (VerilenPuanSayisi), 2),'0.00') ELSE '0.00' END AS OrtPuan,
            (SELECT COUNT(*) FROM SKUsers WHERE DurumID<91 and DurumID>=11 and 
            UserID IN (SELECT UserID FROM SKMemberDates WHERE SKModels.YayinDurumu=1 AND SKModels.YayinTarihi BETWEEN BaslamaTarihi 
            AND COALESCE(SonlanmaTarihi, '2222-12-31'))) AS GorenUserSys,
            (SELECT BinaryDosya FROM SKPictures where SKPictures.ModelID=SKModels.ModelID and Sira = 1) as Picture, 
            (SELECT COUNT(*) FROM SKMemberSingleProjects WHERE SKModels.ModelID=SKMemberSingleProjects.ModelID) as SingleSatis
            FROM SKModels, SKGroups WHERE SKModels.GrubID=SKGroups.GrubID
            AND (SKModels.GrubID={GrubFiltre} or {GrubFiltre}=0) {SiralamaFiltre}
"""
    Models = SQLServer.Sorgula(Models)
    Models = SQLToBase64.Resim(Models)
    return Models




def ModelAcma(UserID, IlkSatir, SayfaAdim):
    ModelID  =   "SELECT ModelID FROM (SELECT *, ROW_NUMBER() OVER (ORDER BY [YayinTarihi] DESC) AS SatirNumarasi FROM SKModels) AS SKModels2"
    ModelID += f" WHERE YayinDurumu=1 AND SatirNumarasi>={IlkSatir} AND SatirNumarasi<={IlkSatir+SayfaAdim} AND ResimSayisi > 0 ORDER BY YayinTarihi DESC"
    ModelID = SQLServer.Sorgula(ModelID)
    ModelID = Formatlama.DictToStr(ModelID, "ModelID")
    

    sql_query = F"""
        SELECT *, FORMAT(VerilenPuanToplami * 1.0 / VerilenPuanSayisi, '0.00') AS OrtPuan, 
        COALESCE((SELECT FORMAT(SUM(VerilenPuan) * 1.0 / COUNT(*), '0.00') FROM SKPuanlar WHERE SKPuanlar.UserID = {UserID}), '---') AS VerilenPuan, 
        (SELECT BinaryDosya FROM SKPictures WHERE SKPictures.ModelID = SKModels.ModelID AND Sira = 1) AS Picture, 
            CASE
                WHEN (SELECT DurumID FROM SKUsers WHERE UserID = {UserID}) = 91
                THEN 'BLOKE'  
                WHEN (SELECT PaketID FROM SKUsers WHERE UserID = {UserID}) = 11 
                THEN 'ADMIN' 
                WHEN (SELECT COUNT(*) FROM SKMemberSingleProjects WHERE SKMemberSingleProjects.UserID = {UserID} AND SKMemberSingleProjects.ModelID = SKModels.ModelID) > 0 
                THEN 'SINGLE' 
                WHEN ModelID IN (SELECT Models.ModelID FROM SKModels AS Models CROSS APPLY (SELECT BaslamaTarihi, SonlanmaTarihi FROM SKMemberDates AS SMD WHERE SMD.UserID = {UserID} AND SMD.PaketID>12 AND Models.YayinTarihi BETWEEN SMD.BaslamaTarihi AND ISNULL(SMD.SonlanmaTarihi, '2222-12-31')) AS D) 
                THEN 'ABONE' 
                ELSE 'KAPALI' 
            END AS AcikKapali 
        FROM SKModels 
        WHERE ModelID IN ({ModelID}) AND (SKModels.ModelCins LIKE 'MODEL%' OR SKModels.ModelCins LIKE 'EXTRA%')
        ORDER BY YayinTarihi DESC;
"""
    Models = SQLServer.Sorgula(sql_query)
    Models = SQLToBase64.Resim(Models)
    return Models
##############################################################################################################
def AdSoyadFiltreSorgusu(HamMetin):
     SqlEk=""
     if len(HamMetin)>1:
          Ad1 = HamMetin[:2]
          Ad2 = HamMetin[3:]
          SqlEk=f"AND ( LEFT(SKUsers.UserAdiSoyadi,2)>='{Ad1}' AND LEFT(SKUsers.UserAdiSoyadi,2)<='{Ad2}' )"
     return SqlEk
##############################################################################################################
def KullanicilarListesi(Start, SayfaAdim, DurumFiltre, AdSoyadFiltre, UserID):
     Sql   =  f""" 
     SELECT (SELECT BaslamaTarihi from SKMemberDates WHERE SKMemberDates.ID=SKUsers.SQLMemberDateID) AS BaslamaTarihi,
     (SELECT SonlanmaTarihi from SKMemberDates WHERE SKMemberDates.ID=SKUsers.SQLMemberDateID) AS SonlanmaTarihi,
     (select count(*) from SKPuanlar WHERE SKPuanlar.UserID=SKUsers.UserID) as PuanSys,
     COALESCE((select FORMAT(SUM(VerilenPuan)*1.0 / COUNT(*),'0.00') from SKPuanlar WHERE SKPuanlar.UserID=SKUsers.UserID),'---') AS PuanOrt,
     
     CASE WHEN SKUsers.DurumID > 21 AND SKUsers.DurumID < 81 THEN 
            (SELECT COUNT(*) FROM SKModels, SKMemberSingleProjects
            WHERE SKUsers.DurumID > 21 AND SKUsers.DurumID < 81 
            AND SKUsers.UserID = SKMemberSingleProjects.UserID
            AND SKMemberSingleProjects.ModelID = SKModels.ModelID
            AND SKModels.YayinDurumu = 1 
            AND SKModels.ModelCins NOT LIKE 'ONLINE%')
        ELSE 0 END AS AcikSingle,
     
     CASE WHEN SKUsers.DurumID > 21 AND SKUsers.DurumID < 81 THEN 
            (SELECT COUNT(*) FROM SKModels 
            WHERE SKUsers.DurumID > 21 AND SKUsers.DurumID < 81 AND SKModels.ModelCins NOT LIKE 'ONLINE%' AND SKModels.YayinDurumu = 1
            AND (select count(*) FROM SKMemberDates WHERE 
            SKMemberDates.PaketID > 12 
            AND SKMemberDates.UserID = SKUsers.UserID
            AND SKModels.YayinTarihi BETWEEN SKMemberDates.BaslamaTarihi AND COALESCE(SKMemberDates.SonlanmaTarihi,'2222-12-31')) > 0)
        ELSE 0 END AS ModelCount,
     
     SKDurumlar.Durumu AS DRM, SKPaketler.Kisa, SKPaketler.PaketAdi, SKDurumlar.UyeDetay, SKDurumlar.Aktifle, SKDurumlar.Red, SKDurumlar.Pasifle, SKDurumlar.ModelAc, SKDurumlar.CihazReset,
     COALESCE((SELECT AtolyeAck FROM SKAtolye WHERE SKAtolye.AtolyeID=SKUsers.AtolyeID),'----') AS AtolyeAck, SKUsers.* 
     FROM SKUsers, SKDurumlar, SKPaketler  WHERE SKUsers.DurumID = SKDurumlar.DurumID and SKUsers.PaketID = SKPaketler.PaketID
     AND (SKDurumlar.DurumID = {DurumFiltre} OR {DurumFiltre} = 0) AND ({UserID}=0 OR SKUsers.UserID={UserID}) {AdSoyadFiltreSorgusu(AdSoyadFiltre)}
     ORDER BY UserAdiSoyadi
     OFFSET {Start} ROWS FETCH NEXT {SayfaAdim} ROWS ONLY"""

     Users = []; Users = SQLServer.Sorgula(Sql)
     if len(Users) > 0:
          for User in Users:
               UserID               = User["UserID"]
               UTalep               = Formatlama.TarihToString(User["UyelikTalepTarihi"], False)
               UBaslama             = Formatlama.TarihToString(User["BaslamaTarihi"], False)
               UAyrilma             = Formatlama.TarihToString(User["SonlanmaTarihi"], False)
               UBloke               = Formatlama.TarihToString(User["BlockTarihi"], False)
               UPassWord            = Sifreleme.SifreyiCoz(User["PassWord"])
               User["UPassWord"]    = UPassWord
               User["UTalep"]       = UTalep
               User["UBaslama"]     = UBaslama
               User["UAyrilma"]     = UAyrilma
               User["UBloke"]       = UBloke
               VPS                  = "0"
               User["PuanSayisi"]   = "0"
               User["OrtPuan"]      = "5"
               
     return Users
##############################################################################################################