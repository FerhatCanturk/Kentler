import base64, Sifreleme
##############################################################################################################
def Resim(Deger):
    if not Deger:
        return []  # Deger boşsa boş bir liste döndür

    for item in Deger:
        encrypted_base64 = item.get("Picture")
        if encrypted_base64:
            try:
                Binary = encrypted_base64 
                image_base64 = base64.b64encode(Binary).decode('utf-8')
                item["Base64Pict"] = image_base64
                del item["Picture"]
            except Exception as e:
                item["Base64Pict"] = ""
        else:
            item["Base64Pict"] = ""
    
    return Deger
##############################################################################################################
def Video(Deger):
    if not Deger:
            return []  # Deger boşsa boş bir liste döndür

    for item in Deger:
        encrypted_base64 = item.get("Video")
        if encrypted_base64:
            try:
                Binary = encrypted_base64
                image_base64 = base64.b64encode(Binary).decode('utf-8')
                item["Base64Video"] = image_base64
                del item["Video"]
            except Exception as e:
                item["Base64Video"] = ""
        else:
            item["Base64Video"] = ""
    
    return Deger
##############################################################################################################