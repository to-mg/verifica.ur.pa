"""
Versione aggiornata ricerca bottone consenso:

1) per il testo dei bottoni la ricerca è fatta su questa stringhe:
"accett", "ho capito", "consent"

2) per i tag <a> sono selezionati quelli associati a una classe
   il cui nome contiene una delle stringhe indicati nel path
   XPath che segue
    "//a["
    "contains(@class, 'btn') or "
    "contains(@class, 'enable') or "
    "contains(@class, 'button') or "
    "contains(@class, 'allow') or "
    "contains(@class, 'cookie') or "
    "contains(@class, 'wordpress-gdpr-popup-agree') or "
    "contains(@class, 'accept') or "
    "not(@class)"
    "]"
negli elementi selezionati si verifica se il testo contiene una di queste
stringhe:
"accetto", "accetta", "ho capito", "acconsent", "consenti"

Inoltre si verifica che il link non inizi con http, portando quindi
potenzialmente su un altro sito.

Per intercettare il caso in cui il click sul bottone o sul link porti
a un altro nodo (ad esempio via javascript), si verifica che il nodo
prima e dopo il click sia lo stesso.
In caso di diversità, si torna all'url di prima del click
"""

import sys
from urllib.parse import urlparse

# testi per esprimere consenso
TESTI_CONSENSO = ["accetto", "accetta", "ho capito", "acconsent", "consenti"]

# classi di tag <a> associati a testi consenso
XPATH_LINK = (
    "//a["
    "contains(@class, 'btn') or "
    "contains(@class, 'enable') or "
    "contains(@class, 'button') or "
    "contains(@class, 'allow') or "
    "contains(@class, 'cookie') or "
    "contains(@class, 'wordpress-gdpr-popup-agree') or "
    "contains(@class, 'accept') or "
    "not(@class)"
    "]"
)


def _cerca_bottone(driver, url):

    # cerca bottoni con testo Accett* o ok
    bottone_consenso = ""
    bottoni = driver.find_elements_by_xpath("//button")
    # controllo su bottoni
    for bottone in bottoni:
        try:
            testo = (
                driver.execute_script(
                    "return(arguments[0].textContent);", bottone
                )
                .strip()
                .lower()
            )
        except Exception:
            print("Errore ricerca testo a", flush=True)
            continue

        if testo == "ok" or any(
            consenso in testo for consenso in TESTI_CONSENSO
        ):
            bottone_consenso = bottone
            print((f"Trovato bottone consenso > {testo}"))
            break
    return bottone_consenso


def _cerca_link(driver, url):
    # controllo su link usato come bottoni
    bottone_consenso = ""
    bottoni = driver.find_elements_by_xpath(XPATH_LINK)
    for bottone in bottoni:
        try:
            testo = (
                driver.execute_script(
                    "return(arguments[0].textContent);", bottone
                )
                .strip()
                .lower()
            )
        except Exception:
            continue
        if testo == "ok" or any(
            consenso in testo for consenso in TESTI_CONSENSO
        ):
            # controlla se il link punta a qualche sito
            href = bottone.get_attribute("href")
            if href and href.startswith("http"):
                continue
            bottone_consenso = bottone
            print((f"Trovato link consenso > {testo}"))
            break
    return bottone_consenso


def click_bottone_consenso(driver):
    url_pre_click = driver.current_url
    nodo_pre_click = urlparse(driver.current_url).netloc
    # cerca bottone per accettazione di tutti i cookies
    bottone_consenso = None
    esito_click = 0
    try:
        bottone_consenso = _cerca_bottone(driver, url_pre_click)
        if not bottone_consenso:
            bottone_consenso = _cerca_link(driver, url_pre_click)
    except Exception:
        print(("Errore in ricerca bottone consenso"))
        errore = str(sys.exc_info()[1]).split("\n")[0]
        print(errore)
        esito_click = 0

    # click su bottone se trovato
    if bottone_consenso:
        try:
            driver.execute_script("arguments[0].click();", bottone_consenso)
            esito_click = 1
        except Exception:
            print(("Errore in click su bottone consenso"))
            errore = str(sys.exc_info()[1]).split("\n")[0]
            print(errore)
            esito_click = 0
        nodo_post_click = urlparse(driver.current_url).netloc
    # selezionato bottone o link sbagliato e si è finiti su
    # un altro nodo. Quindi si fa marcia indietro e si torna
    # all'url precedente
    if nodo_pre_click != nodo_post_click:
        driver.get(url_pre_click)
        esito_click = 0
    return esito_click
