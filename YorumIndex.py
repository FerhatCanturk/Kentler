import SQLServer, random, SQLToBase64
##############################################################################################################
def ToplamModel():
    SQLSorgu = """SELECT COUNT(*) AS MS, 
                SUM(ResimSayisi) AS RS, 
                SUM(VideoSayisi) AS VS FROM SKModels
                """
    ToplamModel = SQLServer.Sorgula(SQLSorgu)
    return ToplamModel
##############################################################################################################
def RastgeleSecim():
    TMS = int(SQLServer.DegerGetir("SELECT COALESCE(COUNT(*), 0) + 1 FROM SKModels WHERE YayinDurumu=1 AND ResimSayisi > 0 AND (ModelCins LIKE 'MODEL%' OR ModelCins LIKE 'EXTRA%')"))
    print(TMS)
    if int(TMS) >= 5:
        RMS = random.sample(range(1, int(TMS) + 1), 3)
        RMS = [str(num) for num in RMS]
        RMS = ", ".join(RMS)
        RMS = f"AND row_num IN ({ RMS })"
    else:
        RMS = ""
    
    SQLSorgu =  f"""SELECT *, CASE WHEN VerilenPuanSayisi>0 THEN FORMAT(ROUND(CAST(VerilenPuanToplami AS FLOAT) / VerilenPuanSayisi, 2),'0.00') ELSE '0.00' END AS OrtPuan,  
                (SELECT BinaryDosya FROM SKPictures where SKPictures.ModelID=SKModels2.ModelID and Sira = 1) AS Picture 
                FROM (SELECT *, ROW_NUMBER() OVER (ORDER BY [ModelID]) AS row_num FROM SKModels where YayinDurumu=1) AS SKModels2 
                WHERE YayinDurumu=1 {RMS} AND ResimSayisi > 0 AND (ModelCins LIKE 'MODEL%' OR ModelCins LIKE 'EXTRA%') ORDER BY ModelAdi """
    Rastgele = SQLServer.Sorgula(SQLSorgu)
    Rastgele = SQLToBase64.Resim(Rastgele)
    return Rastgele
##############################################################################################################
def SonProjeSorgulari():
    SQLSorgu   ="""SELECT TOP 1 *, ResimSayisi AS PictSys, VideoSayisi AS VideoSys,  
                CASE WHEN VerilenPuanSayisi>0 THEN FORMAT(ROUND(CAST(VerilenPuanToplami AS FLOAT) / VerilenPuanSayisi, 2),'0.00') ELSE '0.00' END AS OrtPuan,  
                (SELECT BinaryDosya FROM SKPictures where SKPictures.ModelID=SKModels.ModelID AND Sira = 1) AS Picture 
                FROM SKModels WHERE YayinDurumu = 1 AND ResimSayisi > 0 AND GrubID<500 ORDER BY YayinTarihi DESC """
    SonProje = SQLServer.Sorgula(SQLSorgu)
    SonProje = SQLToBase64.Resim(SonProje)
    return SonProje
##############################################################################################################
def ModelSorgusu(GrubFiltre, SiralamaFiltre):
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
##############################################################################################################
def AbonelikPaketiSorgulari():
     APaket = SQLServer.Sorgula("SELECT * FROM SKPaketler WHERE PaketID > 11")
     return APaket
##############################################################################################################
def WEBSabitleriSorgulari():
     WSabit = SQLServer.Sorgula("SELECT * FROM SKWebSabitler WHERE HTMLSayfaAdi='Index'")
     return WSabit


