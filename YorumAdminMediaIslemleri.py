import SQLServer
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
