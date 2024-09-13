
from flask import Blueprint, redirect, request, session
##############################################################################################################
LocalStorage = Blueprint('LocalStorage', __name__, template_folder='templates')
##############################################################################################################
@LocalStorage.route('/Const', methods=['POST'])
def process_session():
    # Bu Metod LocalDegerOku.html sayfası tarafından çalıştırılır....
    LS = request.form.get('Const')
    if LS:
        session["LocalStorage"] = LS
    else:
        session["LocalStorage"] = ""
    return redirect("IndexSayfasi")
##############################################################################################################


