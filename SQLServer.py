import pyodbc, re
import Sifreleme, datetime, random
from DataBaseConfig import DATABASE_CONFIG
# Bağlantı parametreleri
Server   = DATABASE_CONFIG.get('Server', {})
DataBase = DATABASE_CONFIG.get('DataBase', {})
UserName = DATABASE_CONFIG.get('UserName', {})
PassWord = DATABASE_CONFIG.get('PassWord', {})
# Provider Stringi
Provider = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={Server};DATABASE={DataBase};UID={UserName};PWD={PassWord}'
##########################################################################################################################
def Sorgula(SQLSorgusu, params = None):
    Results = []
    connection = None
    cursor = None
    try:
        connection = pyodbc.connect(Provider)
        cursor = connection.cursor()
        if params:
            cursor.execute(SQLSorgusu, params)
        else:
            cursor.execute(SQLSorgusu)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            Results.append(dict(zip(columns, row)))
    except Exception as e:
        print(f"Hatanız: {e}")
        Results = []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    for result in Results:
        for key, value in result.items():
            if isinstance(value, str):       # Eğer değer metin ise
                result[key] = value.strip()  # Hem sağ hem sol boşlukları kaldır
            
    return Results
##########################################################################################################################
def Calistir(SQLKomutu, params = None):
    Result = True
    connection = None
    cursor = None
    try:
        # Bağlantıyı aç (Varsa connection_string kullanılır, yoksa global Provider değişkeni)
        connection = pyodbc.connect(Provider)
        cursor = connection.cursor()
        
        # SQL komutunu çalıştır
        if params:
            cursor.execute(SQLKomutu, params)
        else:
            cursor.execute(SQLKomutu)
        
        # Değişiklikleri kaydet
        connection.commit()
    except Exception as e:
        # Hata durumunda Result değerini False yap
        print(f"Hatanız: {e}")
        Result = False
    finally:
        # Kaynakları serbest bırak
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    Result = not(Result)
    #True: Hatalı
    #False: Çalıştı
    return Result
##########################################################################################################################  
def IdentityCalistir(SQLKomutu, params = None):
    Result = 0
    connection = None
    cursor = None
    try:
        # Bağlantıyı aç (Varsa connection_string kullanılır, yoksa global Provider değişkeni)
        connection = pyodbc.connect(Provider)
        cursor = connection.cursor()
        
        # SQL komutunu çalıştır
        if params:
            cursor.execute(SQLKomutu, params)
        else:
            cursor.execute(SQLKomutu)
        
        # Değişiklikleri kaydet
        connection.commit()
        
        # Son eklenen ID'yi al
        cursor.execute("SELECT @@IDENTITY AS LastID")
        row = cursor.fetchone()
        
        # ID'yi al ve döndür
        if row:
            Result = row[0]  # Son eklenen ID'yi al
    except Exception as e:
        # Hata durumunda Result değerini 0 yap
        print(f"Hatanız: {e}")
        Result = 0
    finally:
        # Kaynakları serbest bırak
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    return Result
##########################################################################################################################  
def DegerGetir(SQLSorgusu, params = None):
    Results = ""
    connection = None
    cursor = None
    try:
        # Bağlantıyı aç (Varsa connection_string kullanılır, yoksa global Provider değişkeni)
        connection = pyodbc.connect(Provider)
        cursor = connection.cursor()
        
        # SQL sorgusunu çalıştır
        if params:
            cursor.execute(SQLSorgusu, params)
        else:
            cursor.execute(SQLSorgusu)
        
        # Sonuçları al
        row = cursor.fetchone()
        if row:
            Results = row[0]  # İlk sütunu al
        
    except Exception as e:
        # Hata durumunda boş bir string döndür
        print(f"Hatanız: {e}")
        Results = ""
    
    finally:
        # Kaynakları serbest bırak
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    return Results
##########################################################################################################################  
