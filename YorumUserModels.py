import SQLServer
##############################################################################################################
def AcikModellerListesi(UserID):
    SQLKomut = """
        SELECT SKModels.ModelAdi FROM SKModels
            WHERE SKModels.ModelCins NOT LIKE 'ONLINE%' AND SKModels.YayinDurumu = 1
            AND 
            (
            COALESCE((SELECT COUNT(*) FROM SKMemberSingleProjects WHERE SKMemberSingleProjects.UserID = ? AND SKMemberSingleProjects.ModelID=SKModels.ModelID), 0) > 0
            OR
            COALESCE((SELECT COUNT(*) FROM SKMemberDates WHERE SKMemberDates.PaketID > 12 AND SKModels.YayinTarihi BETWEEN BaslamaTarihi AND COALESCE(SonlanmaTarihi,'2222-12-31')), 0) > 0
            ) 
            AND (SELECT COUNT(*) FROM SKUsers WHERE UserID = ? and PaketID > 12 and DurumID > 21 AND DurumID < 81) = 1 ORDER BY ModelAdi"""
    AcikModels = SQLServer.Sorgula(SQLKomut, (UserID, UserID, ))
    return AcikModels
##############################################################################################################
def KapaliModellerListesi(UserID):
    SQLKomut = """
        SELECT SKModels.ModelAdi FROM SKModels
            WHERE SKModels.ModelCins NOT LIKE 'ONLINE%' AND SKModels.YayinDurumu = 1
            AND COALESCE((SELECT COUNT(*) FROM SKMemberSingleProjects WHERE SKMemberSingleProjects.UserID = ? AND SKMemberSingleProjects.ModelID = SKModels.ModelID), 0) = 0
            AND COALESCE((SELECT COUNT(*) FROM SKMemberDates WHERE SKMemberDates.PaketID > 12 AND SKModels.YayinTarihi BETWEEN BaslamaTarihi AND COALESCE(SonlanmaTarihi,'2222-12-31')), 0) = 0
            AND (SELECT COUNT(*) FROM SKUsers WHERE UserID = ? and PaketID > 12 and DurumID > 21 AND DurumID < 81) = 1 ORDER BY ModelAdi"""
    KapaliModels = SQLServer.Sorgula(SQLKomut, (UserID, UserID, ))
    return KapaliModels
##############################################################################################################