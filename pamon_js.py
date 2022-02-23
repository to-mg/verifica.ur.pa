GETGAINFO = """
    try {
        var gafunc = window["GoogleAnalyticsObject"] || ga;
    }
    catch(err) {
        return null;
    }
    return window[gafunc].getAll();
"""


def getgainfo(driver):
    """
    funzione che ritorna la struttura ga.q, cioè la
    coda dei comandi di google analytics come un dizionario
    con più livelli o None se la struttura non è
    definita
    """
    return driver.execute_script(GETGAINFO)


GETDATALAYERINFO = """
    try {
        return dataLayer;
    }
    catch(err) {
        return null;
    }
"""


def getdatalayerinfo(driver):
    """
    funzione che ritorna la struttura datalayer, cioè la
    coda dei comandi di google tag manager come un dizionario
    con più livelli o None se la struttura non è
    definita
    """
    # return datalayer commands
    return driver.execute_script(GETDATALAYERINFO)
