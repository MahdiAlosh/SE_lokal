from flask import Blueprint, redirect, render_template, request, url_for,flash
from flask_login import current_user, login_required
import wikipedia
import requests
from bs4 import BeautifulSoup
import pandas as pd


#für test hinzugefügt
#import requests
#import json
#from fake_useragent import UserAgent

try:
    from googlesearch import Search
except ImportError: 
    print("No module named 'google' found")


def get_infobox_from_url(wikipedia_url):
    try:
        # Wikipedia-Seite abrufen
        response = requests.get(wikipedia_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Suchen nach dem Infobox-Tag
        infobox = soup.find('table', {'class': 'infobox'})
        if not infobox:
            return None
        # Extrahieren der Infobox-Inhalte als Liste von Zeilen
        infobox_rows = []
        for row in infobox.find_all('tr'):
            infobox_rows.append([cell.text.strip() for cell in row.find_all(['th', 'td'])])
        return infobox_rows
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Anfrage an Wikipedia: {e}")


def InfoBox_filltern(infobox_data):

    df = pd.DataFrame(infobox_data, columns=['Attribute', 'Wert'])
    # *Daten mit None entfernen 
    df = df.dropna()
    # *Indexnummern entfernen
    df.set_index("Attribute")
    # *Entferne Zeichenfolgen in eckigen Klammern [ ]
    df = df.map(lambda x: x.split('[')[0] if isinstance(x, str) else x)
    # *Mrd, Mio bw Bio umschreiben
    # Abkürzungen ersetzen
    df = df.map(lambda x: x.replace('Mrd.', 'Milliarde ').replace('Bio.', 'Billion ').replace('Mio.', 'Million ') if isinstance(x, str) else x)
    # Doppelte Wörter (manchmal bei 'Sitz' 2mal das Land) entfernen
    df = df.map(lambda x: remove_duplicate_words(x))
    return df

# Funktion für das Entfernen von doppelten Wörtern
def remove_duplicate_words(text):
    words = text.split()
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    cleaned_text = ' '.join(unique_words)
    return cleaned_text

# Hauptmain:
box = Blueprint('box', __name__)

@box.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    try:
        # Benutzer eingabe speichern
        unternehmen_name = request.form.get('eingabe')
        if not unternehmen_name:
            return render_template('error.html', error_message='Invalid input')
        '''
        unter = 'Tele'
        print(unter)

        #test
        url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + unter

        ua = UserAgent()
        headers = {"user-agent": ua.chrome}
        response = requests.get(url, headers=headers, verify=True)

        suggestions = json.loads(response.text)
        for word in suggestions[1]:
            print(word)
        '''
        # stichwörter für unternehmenname hinzufügen
        unternehmen_name = unternehmen_name + ' Unternehmen wikipedia'

        # Sprache sitzen auf deutsch
        wikipedia.set_lang("de")
        Wikipedia_url_des_Unternehmens = wikipedia.page(unternehmen_name).url

        #Prüfen ob Wikipedia-Seite für das Unternehmen gefunden oder nicht
        if not Wikipedia_url_des_Unternehmens:
            print(f'Das Unternehmen {unternehmen_name} hat kein Wikipedia-URL-Link.')
        else:
            print(Wikipedia_url_des_Unternehmens)

        # Infobox extrahieren aus Wikipedia Seite des Unternehmens 
        infobox_data = get_infobox_from_url(Wikipedia_url_des_Unternehmens)
    
        # Infobox-Inhalte in Dataframe speichern
        if infobox_data:
            #Bevor Initialisieren zuerst bearbeiten
            df=InfoBox_filltern(infobox_data)
            flash('Result found!', category='success')
        else:
            print(f"Infobox für die URL nicht gefunden.")
            flash('No matching. Please try again.', category='error')

        # Tabelle auf Webseite anzeigen:
        #return render_template("home.html", user=current_user, infobox_data=df.to_html(classes='table table-bordered'))
        #return render_template("home.html", user=current_user, infobox_data=df.to_html(classes='table table-bordered',header=False, index=False))
        return render_template("home.html", user=current_user, infobox_data=df.to_html(classes='table table-bordered', index=False))

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        flash('An error occurred. Please try again.', category='error')
        return render_template("home.html", user=current_user)
