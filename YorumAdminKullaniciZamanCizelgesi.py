import Formatlama, SQLServer, Sifreleme, datetime
##############################################################################################################
##############################################################################################################
def KullaniciSorgusu(UserID):
     Sql   =  f""" SELECT (SELECT BaslamaTarihi from SKMemberDates WHERE SKMemberDates.ID=SKUsers.SQLMemberDateID) AS BaslamaTarihi,
            (SELECT SonlanmaTarihi from SKMemberDates WHERE SKMemberDates.ID=SKUsers.SQLMemberDateID) AS SonlanmaTarihi,
            (select count(*) from SKPuanlar WHERE SKPuanlar.UserID=SKUsers.UserID) as PuanSys,
            COALESCE((select FORMAT(SUM(VerilenPuan)*1.0 / COUNT(*),'0.00') from SKPuanlar WHERE SKPuanlar.UserID=SKUsers.UserID),'---') AS PuanOrt,
            CASE WHEN SKUsers.PaketID=11 THEN 0 ELSE (SELECT COUNT(*) FROM SKMemberSingleProjects WHERE SKMemberSingleProjects.UserID = SKUsers.UserID) END AS AcikSingle,
            CASE WHEN SKUsers.PaketID=11 then (SELECT COUNT(*) FROM SKModels) WHEN SKUsers.PaketID=12 then 0 ELSE (SELECT COUNT(*) FROM SKModels WHERE ModelCins = 'MODEL-1' AND 
            ModelID NOT IN (SELECT ModelID FROM SKMemberSingleProjects WHERE SKMemberSingleProjects.UserID = SKUsers.UserID)  AND EXISTS (SELECT 1 FROM SKMemberDates WHERE SKModels.YayinTarihi 
            BETWEEN SKMemberDates.BaslamaTarihi  AND COALESCE(SKMemberDates.SonlanmaTarihi, '2222-12-31')  GROUP BY SKMemberDates.BaslamaTarihi, SKMemberDates.SonlanmaTarihi)) END AS ModelCount,
            SKDurumlar.Durumu AS DRM, SKPaketler.Kisa, SKPaketler.PaketAdi, SKDurumlar.UyeDetay, SKDurumlar.Aktifle, SKDurumlar.Red, SKDurumlar.Pasifle, SKDurumlar.ModelAc, SKDurumlar.CihazReset,
            COALESCE((SELECT AtolyeAck FROM SKAtolye WHERE SKAtolye.AtolyeID=SKUsers.AtolyeID),'----') AS AtolyeAck, SKUsers.* 
            FROM SKUsers, SKDurumlar, SKPaketler  WHERE SKUsers.DurumID = SKDurumlar.DurumID and SKUsers.PaketID = SKPaketler.PaketID
            AND SKUsers.UserID = {UserID}"""
     Users = []; Users = SQLServer.Sorgula(Sql)
     if len(Users) > 0:
          for User in Users:
               UserID               = User["UserID"]
               UTalep               = Formatlama.TarihToString(User["UyelikTalepTarihi"], False)
               UBaslama             = Formatlama.TarihToString(User["BaslamaTarihi"], False)
               UAyrilma             = Formatlama.TarihToString(User["SonlanmaTarihi"], False)
               UBloke               = Formatlama.TarihToString(User["BlockTarihi"], False)
               User["UTalep"]       = UTalep
               User["UBaslama"]     = UBaslama
               User["UAyrilma"]     = UAyrilma
               User["UBloke"]       = UBloke
     return Users
##############################################################################################################
def AboneSorgusu(UserID):
    Yil = datetime.datetime.now().year
    AboneTarihDetails = []
    for SanalYil in range(Yil, Yil-5, -1):
        for SanalAy in range(1,13):
            SanalAy = "0" + str(SanalAy)
            SanalAy = SanalAy[-2:]
            Tarih = str(SanalYil) + "-" +  str(SanalAy)
            
            SQLSorgu = f"""SELECT * FROM SKMemberDates, SKPaketler WHERE SKMemberDates.PaketID=SKPaketler.PaketID 
                        AND UserID={UserID} AND LEFT(CONVERT(nvarchar,BaslamaTarihi), 7)<='{Tarih}' AND 
                        CASE WHEN SonlanmaTarihi IS NULL THEN '2222-12' ELSE LEFT(CONVERT(nvarchar,SonlanmaTarihi), 7) END>='{Tarih}'"""
            Durum = SQLServer.Sorgula(SQLSorgu)     
            if Durum:
                AboneTarihDetails.append({'Baslik':Tarih[:4], 'Tarih': Tarih, 'Durum': Durum[0]["PaketID"],'PaketKisa': Durum[0]["Kisa"]})
            else:
                AboneTarihDetails.append({'Baslik':Tarih[:4], 'Tarih': Tarih, 'Durum': 0,'PaketKisa': "---"})
    return AboneTarihDetails
##############################################################################################################