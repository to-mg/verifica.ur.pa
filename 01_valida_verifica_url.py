"""
Modulo per validare e se possibile sistemare gli url nella tabella
degli enti pubblici scaricati da
https://indicepa.gov.it/ipa-dati/dataset/enti e salvati nel file locale:
d09adf99-dc10-4349-8c53-27b1e5aa97b6.csv

Gli url sono divisi secondo le categorie nella
tabella che specifica i codici_categoria degli enti pubblici
https://indicepa.gov.it/ipa-dati/dataset/categorie-enti


La validazione è fatta in due passaggi:

1) verifica formale degli url e tentativo di correzione
2) verifica di connettività usando requests.get() con la gestione di alcuni
   dei codici di errore

### verifica formale degli url e tentativo di correzione
si lancia il programma con queste opzioni
python3 01_valida_verifica_url.py -a

Questo è una passaggio molto rapido

Per ogni url in d09adf99-dc10-4349-8c53-27b1e5aa97b6.csv è eseguita la funzione
analisi che:
- valida l'url
Gli url sono validati usando una versione leggermente modificata di
https://github.com/kvesteri/validators/blob/master/validators/url.py

- se nel'url manca il protocollo, aggiunge in testa http, sperando che
   i siti con https abbiano il reindirizzamento da http
- verifica la presenza di ".gov" nell'url che è:
   - mantenuto per le categorie in cui è giusto ci sia, cioè
     ["C1", "C10", "C11", "C3", "L46", "L17", "L35", "L47"]
   - è rimpiazzato con .edu per gli enti scolastici (L33)
   - rimosso per le altre categorie
- opera altre correzioni minori

Il programma genera:
- un file per gli url di ogni categoria nella cartella per.categorie
- il file enti.csv con tutti gli url

Nel file risultante sono presenti sia la colonna "url" con
l'url ottenuto da questa elaborazione e sia la colonna "Sito_istituzionale"
con l'url originale

Sono rimossi le righe con url duplicati e con url mancante

### verifica di connettività usando requests.get() con la gestione di alcuni
   dei codici di errore

Questo passaggio è molto più lento, ma visto che il carico di CPU è basso
si può lanciare in parallelo sui diversi file per categoria

si lancia il programma con queste opzioni
python3 01_valida_verifica_url.py -v -t TEMPO_ATTESA
  -u {n,e}
  -i IFILE


TEMPO_ATTESA è il tempo in secondo per ricevere la risposta del web server
-u serve per specificare quai url verificare:
   n  si verificano gli url non testati
   e  si verificano solo gli url per i quali in tentativi precedenti
      si è riscontrato un errore

IFILE è il file (per categoria e con tutti gli url) con gli url da verificare

questo passaggio aggiunge 3 colonne ai file degli url
- http_ok           url valido o _NV_ per url non valido
codice_risposta     200 in caso di successo o messaggio di errore altrimenti
test_timeout        il tempo di attesa usato per il test


Ho lanciato il programma in con le opzioni -v e -n
(validazione di tutti gli url)
con tempo_attesa 5 secondi e in circa tre ore
ha esaminato tutti gli url
girando su TV box con Celeron J3455 (CPU che più entry level non si può)
con ubuntu.

In un secondo giro con timeout 20 e con verifica dei soli url
errati nel giro precedente sono saltati fuori circa 3800 siti
andati in errore con tiemout 5 secondi
"""
import argparse
import locale
import os
import re
import signal
import sys
import pandas as pd
import numpy as np
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from validate_url import validate
from dati_comuni import CARTELLA_CSV, URL_NON_VALIDO

STATISTICHE = "statistiche.categorie.csv"


"""
1) nodo down
Server non disponibile
Exception type <class 'requests.exceptions.ConnectionError'>
Exception instance HTTPConnectionPool(host='192.168.1.190', port=80):
Max retries exceeded with url:
/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection
object at 0x7f0322197130>:
Failed to establish a new connection: [Errno 113] No route to host'))

2) nodo up no server
Server non disponibile
Exception type <class 'requests.exceptions.ConnectionError'>
Exception instance HTTPConnectionPool(host='192.168.1.177', port=80):
Max retries exceeded with url: /
(Caused by NewConnectionError('<urllib3.connection.HTTPConnection
object at 0x7f0322197970>:
Failed to establish a new connection: [Errno 111] Connection refused'))

3) timeout
Nodo raggiungibile, server attivo, ma problemi in risposta.
    Se https allora provare http
Exception type <class 'requests.exceptions.ConnectTimeout'>
Exception instance HTTPSConnectionPool(host='commissario.ospedale.siracusa.it',
port=443): Max retries exceeded with url: /
(Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection
object at 0x7f032216eeb0>,
'Connection to commissario.ospedale.siracusa.it timed out.
(connect timeout=5)'))

4) https a nodo senza SSL
Nodo raggiungibile, server attivo, problemi https.
    Se https allora provare http
Exception type <class 'requests.exceptions.SSLError'>
Exception instance "HTTPSConnectionPool(host='192.168.1.178',
port=8000): Max retries exceeded with url: /
(Caused by NewConnectionError('<urllib3.connection.HTTPSConnection
object at 0x7f032217b0a0>:
Failed to establish a new connection: [Errno 113] No route to host'))"

5) errore dns
Nome nodo errato
Exception type  <class 'requests.exceptions.ConnectionError'>
Exception instance HTTPConnectionPool(host='www.nomesenzasenso.it', port=80):
Max retries exceeded with url: /
(Caused by NewConnectionError('<urllib3.connection.HTTPConnection
object at 0x7fb4ff15f3d0>:
Failed to establish a new connection: [Errno -2] Name or service not known'))

"""

TIMEOUT = 1
SSLERROR = 2
NODEDOWN = 3
WEBSERVERDOWN = 4
DNSERROR = 5
ALTROERRORE = 6


def _analizza_errore():
    """
    ritorna
    - un codice numerico di errore
    - la stringa che descrive l'errore"""
    classe = str(sys.exc_info()[0])
    if "ConnectTimeout" in classe:
        return TIMEOUT, "ConnectTimeout"
    if "SSLError" in classe:
        return SSLERROR, "SSLERROR"

    errore = str(sys.exc_info()[1])
    errnos = re.findall(r"Errno -?\d{1,3}", errore)
    if errnos:
        errno = errnos[0].split()[1]
        codice_errore = {
            "113": NODEDOWN,
            "111": WEBSERVERDOWN,
            "-2": DNSERROR,
        }.get(errno, ALTROERRORE)
        return [codice_errore, errnos]
    else:
        if "Read timed out" in errore:
            return TIMEOUT, "ConnectTimeout"
        else:
            return [ALTROERRORE, errore]


UA = (
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) "
    "Gecko/20100101 Firefox/97.0"
)
REQUEST_HEADERS = {"User-Agent": UA}


def _controllo_url(url, timeout):
    """
    ritorna
    - url validato con successo o URL_NON_VALIDO in caso di errore
    - codice http di successo o la stringa che descrive l'errore
    """
    try:
        resp = requests.get(
            url, allow_redirects=True, timeout=timeout, headers=REQUEST_HEADERS
        )
        res = [url, str(resp.status_code)]
        punto = "+"
    except Exception:
        errore, errore_str = _analizza_errore()
        if errore == DNSERROR:
            # prova a togliere ".gov"
            if ".gov" in url:
                url = url.replace(".gov", "")
                try:
                    resp = requests.get(
                        url, allow_redirects=True, timeout=timeout
                    )
                    res = [url, resp.status_code]
                    punto = "+"
                except Exception:
                    errore, errore_str = _analizza_errore()
                    punto = "-"
                    res = [URL_NON_VALIDO, errore_str]
            else:
                punto = "-"
                res = [URL_NON_VALIDO, errore_str]
        elif errore in (WEBSERVERDOWN, NODEDOWN):
            punto = "."
            res = [URL_NON_VALIDO, errore_str]
        elif errore in (TIMEOUT, SSLERROR):
            if url.startswith("https:"):
                url = url.replace("https:", "http:")
            else:
                if url.startswith("http:"):
                    url = url.replace("http:", "https:")
            try:
                # per alcuni siti requests ritorna
                # SSL: CERTIFICATE_VERIFY_FAILED
                # riprova disabilitando controllo certificati
                requests.packages.urllib3.disable_warnings(
                    InsecureRequestWarning
                )
                resp = requests.get(
                    url, allow_redirects=True, timeout=timeout, verify=False
                )
                res = [url, resp.status_code]
                punto = "+"
            except Exception:
                errore, errore_str = _analizza_errore()
                res = [URL_NON_VALIDO, errore_str]
                punto = "-"
        else:
            punto = "-"
            res = [URL_NON_VALIDO, errore_str]

    print(punto, end="", flush=True)
    return res


def _controllo_sito_http(riga, tempo_attesa, url_da_esaminare):
    """
    ritorna
    - url validato con successo o None in caso di errore
    - codice http di successo o la stringa che descrive l'errore
    """

    # riga già testata, controllo su righe non testate
    if url_da_esaminare == "n" and riga["codice_risposta"]:
        return riga["http_ok"], riga["codice_risposta"], riga["test_timeout"]
    # riga già testata con successo, controllo su righe testate con errore
    if url_da_esaminare == "e" and riga["http_ok"] != URL_NON_VALIDO:
        return riga["http_ok"], riga["codice_risposta"], riga["test_timeout"]

    url = riga["url"]
    # print("Url ", url)
    url_ok, codice = _controllo_url(url, tempo_attesa)
    url1 = riga["Sito_istituzionale"]
    if url_ok == URL_NON_VALIDO and url != url1 and url1.startswith("http"):
        # print("     Url ", url1)
        url1_ok, codice1_ok = _controllo_url(url1, tempo_attesa)
        if url1_ok != URL_NON_VALIDO:
            url_ok = url1_ok
            codice = codice1_ok
    return url_ok, codice, tempo_attesa


"""
salva il dataframe se ricevi SIGUSR1
non funziona
"""

file_corrente = ""
dfcv = None


def _salva_csv_corrente():
    print(" ###### Ricevuto segnale SIGUSR1")
    print(file_corrente, dfcv.shape)
    dfcv.to_csv(file_corrente, sep=";", index=False)


def verifica_url(file_categoria, tempo_attesa, url_da_esaminare):
    global file_corrente
    global dfcv
    global botout
    np.warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
    # salva il pid in un file per facilitare invio segnale
    open("pid.txt", "wt").write(str(os.getpid()))
    print("File categoria ", file_categoria)
    file_corrente = file_categoria
    dfcv = pd.read_csv(file_categoria, sep=";")

    """
    print("Controllo url")
    df["url_ok"], df["punto"] = zip(*df.apply(_controllo_sito_dns, axis=1))
    """

    # se le cose vanno per le lunghe, invia SIGUSR1
    # df è salvato con le elaborazioni compiute fino al momento"
    signal.signal(signal.SIGUSR1, _salva_csv_corrente)
    # controlla se è possibile accedere all'url
    if "http_ok" not in list(dfcv.columns):
        dfcv.loc[:, "http_ok"] = dfcv.shape[0] * ""
        dfcv.loc[:, "codice_risposta"] = dfcv.shape[0] * ""
        dfcv.loc[:, "test_timeout"] = dfcv.shape[0] * -1
    dfcv["http_ok"], dfcv["codice_risposta"], dfcv["test_timeout"] = zip(
        *dfcv.apply(
            _controllo_sito_http,
            axis=1,
            args=[tempo_attesa, url_da_esaminare],
        ),
    )
    dfcv.to_csv(
        file_categoria,
        sep=";",
        index=False,
    )


ERRORI = {
    "https:sistemaambientelucca.it": "https://sistemaambientelucca.it",
    "htpp://www.comunedilentella.it": "https://comunedilentella.it",
    "htt://www.comune.ottati.sa.it": "https://www.comune.ottati.sa.it",
    "www.comune.pescasseroli.aq.ithttp://www.indicepa.gov.it/ipa2/img/btn_postaelettronica_on.png": "http://www.comune.pescasseroli.aq.it",
    "http//:www.comune.saracinesco.rm.it": "http://www.comune.saracinesco.rm.it",
    "htt:/www.comune.magisano.cz.it": "http://www.comune.magisano.cz.it",
    "www://comune.serrata.it": "http://www.comune.serrata.rc.it",
    ".http://www.cpia10frosinone.gov.it": "http://www.cpia10frosinone.gov.it",
    "https:/www.iccapassomazzini.edu.it": "https://www.iccapassomazzini.edu.it",
    "www.http://www.ipsaameloni.edu.it": "https://www.ipsaameloni.edu.it",
    "www.https://iscsolecanta.edu.it": "https://iscsolecanta.edu.it",
    "https:www.circolodidatticoortadiatella.it": "https://www.circolodidatticoortadiatella.edu.it",
    "http/istitutoglobaleseui.it": "https://istitutoglobaleseui.it",
    "www.icviasanbiagioplatani.gov.it                .": "http://www.icviasanbiagioplatani.gov.it",
    "istsc_rmic80800e": "https://www.scuolareginamargherita.edu.it",
    "---": "https://www.bimsarca.tn.it",
}

ERRORI_INTRATTABILI = ["about:blank", "http", ".", ""]


def _fix_url(riga):
    url = riga["Sito_istituzionale"].lower().strip()
    if url in ERRORI_INTRATTABILI:
        # print(riga.Denominazione_ente, " # url=", url)
        return None
    if url.endswith("/"):
        url = url[:-1]

    # valida url
    if not validate(url):
        try:
            url1 = ERRORI[url]
        except KeyError:
            # se manca il protocollo usa http, sperando che ci sia un
            # redirect a https ove si usa https
            url1 = f"http://{url}" if not url.startswith("http") else url
        if url1.endswith("."):
            url1 = url1[:-1]
        url1 = (
            url1.replace(",", ".")
            .replace(" ", ".")
            .replace("..", ".")
            .replace("//ww.", "//www.")
            .replace("http//", "http://")
            .replace("https//", "https://")
            .replace("http.//", "http://")
            .replace("http//:", "http://")
            .replace("///", "//")
            .replace(":it", ".it")
            .replace("-", ".")
        )
        if not url1.endswith(".it"):
            url1 = f"{url1}.it"
        url = url1 if validate(url1) else None
    # mantieni solo protocollo e dominio
    if url:
        pos = url[8:].find("/")
        if pos > 0:
            url = url[: pos + 8]
    return url


def analisi_url():
    colonne = [
        "Denominazione_ente",
        "Codice_comune_ISTAT",
        "Sito_istituzionale",
        "Codice_Categoria",
    ]

    df1 = pd.read_csv(
        "d09adf99-dc10-4349-8c53-27b1e5aa97b6.csv", usecols=colonne
    )
    df1.fillna("", inplace=True)
    # controlla la sintassi dell'url
    # scrivi url non validi in errori.csv
    # rimuovi righe con url non validi
    df1["url"] = df1.apply(_fix_url, axis=1)
    df1[pd.isnull(df1.url)].to_csv("errori.csv", sep=";", index=False)
    df1 = df1[df1.url.notna()]

    # molti enti hanno .gov nel loro nome per errore
    # scuole con .gov diventa .edu
    idx = df1[
        (df1.Codice_Categoria == "L33") & (df1.url.str.contains("gov.it"))
    ].index
    df1.loc[idx, "url"] = df1["url"].str.replace(
        r"gov.it", "edu.it", regex=True
    )
    # categorie in cui si trova giustamente .gov.it
    categorie_con_gov = set(
        ["C1", "C10", "C11", "C3", "L46", "L17", "L35", "L47"]
    )
    # categorie dal cui url va rimosso .gov
    categorie_senza_gov = (
        set(df1.Codice_Categoria.unique()) - categorie_con_gov
    )
    # rimuovi scuole già trattate prima
    categorie_senza_gov.remove("L33")
    # rimuovi .gov dagli url in cui non ci dovrebbe (ripeto dovrebbe) essere
    idx = df1[
        (df1.url.str.contains("gov.it"))
        & (df1.Codice_Categoria.isin(categorie_senza_gov))
    ].index
    df1.loc[idx, "url"] = df1["url"].str.replace(r".gov.it", ".it", regex=True)
    CARTELLA_CSV.mkdir(exist_ok=True)

    # un file per ogni categoria
    colonne = ["Codice_categoria", "Nome_categoria"]
    dfc = pd.read_csv("categorie_enti.csv", usecols=colonne)
    dfc.loc[:, "Numero_url"] = dfc.shape[0] * [0]
    for categoria in df1.Codice_Categoria.unique():
        nome_categoria = dfc[
            dfc.Codice_categoria == categoria
        ].Nome_categoria.values[0]
        dfcat = df1[df1.Codice_Categoria == categoria]
        # rimuovi righe con url duplicati
        dfcat = dfcat[dfcat.Sito_istituzionale.notna()].drop_duplicates(
            ["Sito_istituzionale"]
        )
        dfcat.to_csv(
            CARTELLA_CSV / (nome_categoria.strip() + ".csv").replace(" ", "."),
            sep=";",
            index=False,
        )
        idx = dfc[dfc.Codice_categoria == categoria].index
        dfc.loc[idx, "Numero_url"] = dfcat.shape[0]
    dfc.sort_values(by=["Numero_url"], inplace=True, ascending=False)
    dfc.to_csv("statistiche.categorie.csv", sep=";", index=False)
    df1.to_csv("enti.csv", index=False, sep=";")


def main(argv):
    locale.setlocale(locale.LC_ALL, "it_IT.utf8")
    parser = argparse.ArgumentParser()
    # analisi formale dell'url
    parser.add_argument("-a", "--analisi", action="store_true")
    # verifica connessione all'url
    parser.add_argument("-v", "--verifica", action="store_true")
    # tempo di attesa per risposta
    parser.add_argument(
        "-t",
        "--tempo_attesa",
        type=int,
        default=5,
        required="--verifica" in sys.argv or "-v" in sys.argv,
    )
    # quali sono gli url da esaminare
    #  'n' quelli non ancora testati
    #  'e' quelli con errore in test precedenti
    parser.add_argument(
        "-u",
        "--url_da_esaminare",
        type=str.lower,
        choices=("n", "e"),
        default="n",
        required="--verifica" in sys.argv or "-v" in sys.argv,
    )
    # file con url da esaminare
    parser.add_argument(
        "-i",
        "--ifile",
        type=str,
        required="--verifica" in sys.argv or "-v" in sys.argv,
    )

    argomenti = parser.parse_args()

    if argomenti.analisi:
        analisi_url()
    elif argomenti.verifica:
        verifica_url(
            argomenti.ifile, argomenti.tempo_attesa, argomenti.url_da_esaminare
        )


if __name__ == "__main__":
    main(sys.argv)
