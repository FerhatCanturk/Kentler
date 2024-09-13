import Sifreleme, SQLServer
##############################################################################################################
def AdSoyadFiltreSorgusu(HamMetin):
     SqlEk=""
     if len(HamMetin) > 0:
          SqlEk=f"AND SKUsers.UserAdiSoyadi LIKE '{HamMetin}%'"
     return SqlEk
     
##############################################################################################################
def KullanicilarListesi(Start, SayfaAdim, DurumFiltre, AdSoyadFiltre, UserID):
    Sql =  f"""
    SELECT

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

        (SELECT BaslamaTarihi  FROM SKMemberDates WHERE SKUsers.SQLMemberDateID = SKMemberDates.ID AND SKUsers.UserID = SKMemberDates.UserID) AS BaslamaTarihi,
        (SELECT SonlanmaTarihi FROM SKMemberDates WHERE SKUsers.SQLMemberDateID = SKMemberDates.ID AND SKUsers.UserID = SKMemberDates.UserID) AS SonlanmaTarihi,
        (SELECT COUNT(*)       FROM SKPuanlar     WHERE SKUsers.UserID = SKPuanlar.UserID) as PuanSys,
        COALESCE((select FORMAT(SUM(VerilenPuan)*1.0 / COUNT(*),'0.00') from SKPuanlar WHERE SKPuanlar.UserID=SKUsers.UserID),'---') AS PuanOrt,
        SKDurumlar.Durumu AS DRM, SKPaketler.Kisa, SKPaketler.PaketAdi, SKDurumlar.UyeDetay, SKDurumlar.Aktifle, SKDurumlar.Red, SKDurumlar.Pasifle, SKDurumlar.ModelAc, SKDurumlar.CihazReset,
        COALESCE((SELECT AtolyeAck FROM SKAtolye WHERE SKAtolye.AtolyeID=SKUsers.AtolyeID),'----') AS AtolyeAck, SKUsers.* 

        FROM SKUsers, SKPaketler, SKDurumlar
        WHERE SKUsers.PaketID = SKPaketler.PaketID AND SKUsers.DurumID = SKDurumlar.DurumID
        AND (SKDurumlar.DurumID = {DurumFiltre} OR {DurumFiltre} = 0) AND ({UserID}=0 OR SKUsers.UserID={UserID}) {AdSoyadFiltreSorgusu(AdSoyadFiltre)}
        ORDER BY UserAdiSoyadi
        OFFSET {Start} ROWS FETCH NEXT {SayfaAdim} ROWS ONLY"""

    Users = []; Users = SQLServer.Sorgula(Sql)
    for User in Users:
        SifreliPass = User.get("PassWord")
        if SifreliPass:
            try:
                Binary = SifreliPass
                image_base64 = Sifreleme.SifreyiCoz(SifreliPass)
                User["SifresizPass"] = image_base64
            except Exception as e:
                Users["PassWord"] = "Okunamadı"
        else:
            Users["PassWord"] = "Okunamadı"
    return Users
##############################################################################################################
def KullaniciSayisi(DurumFiltre):
     Sql  = "SELECT COALESCE(COUNT(*),0) AS Sys FROM SKUsers "
     Sql += f" WHERE ({DurumFiltre} = 0 or DurumID = {DurumFiltre})"
     UserSys =int(SQLServer.DegerGetir(Sql))
     return UserSys

##############################################################################################################
def AboneBasliklari():
     SQLSorgusu  = "SELECT left(UserAdiSoyadi,1) AS Baslik, COUNT(*) AS Sys  FROM SKUsers GROUP BY left(UserAdiSoyadi,1) order by left(UserAdiSoyadi,1)"
     Users       = SQLServer.Sorgula(SQLSorgusu)
     return Users
##############################################################################################################
def AbonelikPaketiSorgulari():
     APaket = SQLServer.Sorgula("SELECT * FROM SKPaketler WHERE PaketID > 11")
     return APaket
##############################################################################################################
def SKDatabaseGuncelle():
    SQLModels ="""
    UPDATE SKModels SET
    VerilenPuanSayisi = COALESCE((SELECT count(*) FROM SKPuanlar SP WHERE SP.ModelID = SKModels.ModelID), 0) + 1,
    VerilenPuanToplami = COALESCE((SELECT sum(VerilenPuan) FROM SKPuanlar SP WHERE SP.ModelID = SKModels.ModelID), 0) + 5,
    ResimSayisi = COALESCE((SELECT count(*) FROM SKPictures SPict WHERE SPict.ModelID = SKModels.ModelID), 0),
    VideoSayisi = COALESCE((SELECT count(*) FROM SKVideos SVid WHERE SVid.ModelID = SKModels.ModelID), 0),
    YayinDurumu = CASE
        WHEN YayinDurumu = 1 
            THEN 
                CASE 
                    WHEN COALESCE((SELECT COUNT(*) FROM SKPictures WHERE SKPictures.ModelID = SKModels.ModelID), 0) > 0 
                    THEN 1 
                    ELSE 0 
            END
        ELSE 0 
    END
        """
    SQLServer.Calistir(SQLModels)
##############################################################################################################