

def TarihToString(Deger, Uzun):
     Donus="-----"
     if Deger==None or Deger=="":
          Donus="-----"
     else:
          if Uzun:
               Donus=Deger.strftime("%d-%m-%Y %H:%M:%S")
          else:
               Donus=Deger.strftime("%d-%m-%Y")
     return Donus




def DictToStr(DictVeri, SutunAdi):
     if len(DictVeri) > 0:
          ModelIDListe = [str(model[SutunAdi]) for model in DictVeri]
          ModelIDListe = ",".join(ModelIDListe)
     else:
          ModelIDListe="0"
     return ModelIDListe