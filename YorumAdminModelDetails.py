import SQLServer, SQLToBase64
def ModelResimler(ModelID):
    Models = f"""
        SELECT SKModels.*, SKGroups.*, SKPictures.Sira, SKPictures.BinaryDosya AS Picture
        FROM SKModels, SKGroups, SKPictures WHERE 
		SKModels.GrubID=SKGroups.GrubID AND SKModels.ModelID = {ModelID} and SKPictures.ModelID=SKModels.ModelID 
        ORDER BY Sira"""
    Models = SQLServer.Sorgula(Models)
    Models = SQLToBase64.Resim(Models)
    return Models
##############################################################################################################
def ModelVideolar(ModelID):
    Models = f"""
    SELECT SKModels.*, SKGroups.*, SKVideos.Sira                                    
    FROM SKModels, SKGroups, SKVideos WHERE 
    SKModels.GrubID=SKGroups.GrubID AND SKModels.ModelID = {ModelID} and SKVideos.ModelID=SKModels.ModelID 
    ORDER BY Sira
"""
    Models = SQLServer.Sorgula(Models)
    return Models
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
def AbonelikPaketiSorgulari():
     APaket = SQLServer.Sorgula("SELECT * FROM SKPaketler WHERE PaketID > 11")
     return APaket
##############################################################################################################