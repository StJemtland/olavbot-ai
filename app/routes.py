from flask import Blueprint, render_template
from app.utils import hent_data
import datetime

main = Blueprint('main', __name__)

@main.route("/")
def index():
    aksjer = {
        "KOG": hent_data("KOG.OL"),
        "NHY": hent_data("NHY.OL"),
        "SAAB-B.ST": hent_data("SAAB-B.ST")
    }

    krypto = {
        "XRP": hent_data("XRP-USD"),
        "ETH": hent_data("ETH-USD"),
        "BTC": hent_data("BTC-USD")
    }

    tidspunkt = datetime.datetime.now().strftime("%d.%m %H:%M")

    return render_template("index.html", aksjer=aksjer, krypto=krypto, tidspunkt=tidspunkt)

