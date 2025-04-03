from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def hjem():
    logg_fil = "transaksjonslogg_v7_zen.csv"
    if os.path.exists(logg_fil):
        df = pd.read_csv(logg_fil)
        tabell = df.to_html(index=False, classes="tabell")
    else:
        tabell = "<p>Ingen transaksjoner er registrert enda.</p>"

    html = f"""
    <html>
    <head>
        <title>Min AI-portefølje</title>
        <style>
            body {{
                font-family: Helvetica, sans-serif;
                background-color: #f7f7f7;
                padding: 40px;
                color: #333;
            }}
            h1 {{
                color: #003366;
            }}
            .tabell {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }}
            .tabell th, .tabell td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
            .tabell th {{
                background-color: #e6f2ff;
                text-align: left;
            }}
            .tabell tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>📈 Min AI-portefølje</h1>
        <p>Velkommen, Patrick. Her er siste oppdateringer fra OlavBot™:</p>
        {tabell}
        <p style="margin-top: 30px; font-size: 0.9em;">Oppdateres automatisk etter hver kjøring.</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)

