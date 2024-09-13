import SQLServer
import SQLToBase64
##############################################################################################################
def GrubSorgulari():
    SQLSorgu = """
    SELECT *, (SELECT COUNT(*) FROM SKModels WHERE SKModels.GrubID=SKGroups.GrubID) AS ModelSys
    FROM SKGroups ORDER BY GrubAdi
    """
    Groups = SQLServer.Sorgula(SQLSorgu)
    return Groups
##############################################################################################################
def AbonelikPaketiSorgulari():
     APaket = SQLServer.Sorgula("SELECT * FROM SKPaketler WHERE PaketID > 11")
     return APaket
##############################################################################################################
def WEBSabitleriSorgulari():
     WSabit = SQLServer.Sorgula("SELECT * FROM SKWebSabitler WHERE HTMLSayfaAdi LIKE 'Index%'")
     return WSabit



