"""
Versione aggirona ricerca bottone consenso:

1) per il testo dei bottoni la ricerca è fatta su questa stringhe:
TESTI_CONSENSO = ["accett", "ho capito", "consent"]

2) per i tag <a> sono selezionati quelli associati a una classe
   che il cui nome contiene una delle stringhe indicati nel path
   XPath che segue
    "//a["
    "contains(@class, 'btn') or "
    "contains(@class, 'enable') or "
    "contains(@class, 'button') or "
    "contains(@class, 'allow') or "
    "contains(@class, 'cookie') or "
    "contains(@class, 'accept')"
    "]"
negli elementi selezionati i verfica se il teso contiene una di queste
stringhe:
TESTI_CONSENSO = ["accett", "ho capito", "consent"]

Inoltre si verifica che il link non inizi con http, portando quindi
potenzialmente su un altro sito
"""
import sys

# testi per esprimere consenso
TESTI_CONSENSO = ["accett", "ho capito", "consent"]

# classi di tag <a> associati a testi consenso
XPATH_LINK = (
    "//a["
    "contains(@class, 'btn') or "
    "contains(@class, 'enable') or "
    "contains(@class, 'button') or "
    "contains(@class, 'allow') or "
    "contains(@class, 'cookie') or "
    "contains(@class, 'accept')"
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

    # cerca bottone per accettazione di tutti i cookies
    url = driver.current_url
    bottone_consenso = None
    esito_click = 0
    try:
        bottone_consenso = _cerca_bottone(driver, url)
        if not bottone_consenso:
            bottone_consenso = _cerca_link(driver, url)
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
    return esito_click
