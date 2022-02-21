if [ "$#" -ne 2 ]; then 
	echo $0 " url_da_controllare (n, e) timeout " 
	exit 
fi
url=$1 
timeout=$2 
if [ "$url" != "n" ] && [ "$url" != "e" ]
then
    echo "Primo argomento deve essere n o e"
    exit
fi	

set -x
mkdir out 2>/dev/null 
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.Regionali.e.Provinciale.per.la.Rappresentanza.Negoziale.csv 2>&1 >out/Agenzie.Regionali.e.Provinciale.per.la.Rappresentanza.Negoziale.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Aziende.ed.Amministrazioni.dello.Stato.ad.Ordinamento.Autonomo.csv 2>&1 >out/Aziende.ed.Amministrazioni.dello.Stato.ad.Ordinamento.Autonomo.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Enti.di.Previdenza.ed.Assistenza.Sociale.in.Conto.Economico.Consolidato.pubblici.csv 2>&1 >out/Enti.di.Previdenza.ed.Assistenza.Sociale.in.Conto.Economico.Consolidato.pubblici.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Forze.di.Polizia.ad.Ordinamento.Civile.e.Militare.per.la.Tutela.dell'Ordine.e.della.Sicurezza.Pubblica.csv 2>&1 >Forze.di.Polizia.ad.Ordinamento.Civile.e.Militare.per.la.Tutela.dell'Ordine.e.della.Sicurezza.Pubblica.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.Fiscali.csv 2>&1 >out/Agenzie.Fiscali.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Organi.Costituzionali.e.di.Rilievo.Costituzionale.csv 2>&1 >out/Organi.Costituzionali.e.di.Rilievo.Costituzionale.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Commissari.Straordinari.Governativi.csv 2>&1 >out/Commissari.Straordinari.Governativi.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.Regionali.per.le.Erogazioni.in.Agricoltura.csv 2>&1 >out/Agenzie.Regionali.per.le.Erogazioni.in.Agricoltura.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Istituti.Zooprofilattici.Sperimentali.csv 2>&1 >out/Istituti.Zooprofilattici.Sperimentali.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Consorzi.per.l'Area.di.Sviluppo.Industriale.csv 2>&1 >out/Consorzi.per.l'Area.di.Sviluppo.Industriale.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Fondazioni.Lirico,.Sinfoniche.csv 2>&1 >out/Fondazioni.Lirico,.Sinfoniche.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.ed.Enti.Regionali.di.Sviluppo.Agricolo.csv 2>&1 >out/Agenzie.ed.Enti.Regionali.di.Sviluppo.Agricolo.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.ed.Enti.Regionali.del.Lavoro.csv 2>&1 >out/Agenzie.ed.Enti.Regionali.del.Lavoro.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Citta'.Metropolitane.csv 2>&1 >out/Citta'.Metropolitane.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.Regionali.Sanitarie.csv 2>&1 >out/Agenzie.Regionali.Sanitarie.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Autorita'.Amministrative.Indipendenti.csv 2>&1 >out/Autorita'.Amministrative.Indipendenti.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Teatri.Stabili.ad.Iniziativa.Pubblica.csv 2>&1 >out/Teatri.Stabili.ad.Iniziativa.Pubblica.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Autorita'.Portuali.csv 2>&1 >out/Autorita'.Portuali.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Autorita'.di.Bacino.csv 2>&1 >out/Autorita'.di.Bacino.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Presidenza.del.Consiglio.dei.Ministri,.Ministeri.e.Avvocatura.dello.Stato.csv 2>&1 >out/Presidenza.del.Consiglio.dei.Ministri,.Ministeri.e.Avvocatura.dello.Stato.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Enti.di.Previdenza.ed.Assistenza.Sociale.in.Conto.Economico.Consolidato.privati..csv 2>&1 >out/Enti.di.Previdenza.ed.Assistenza.Sociale.in.Conto.Economico.Consolidato.privati..$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.ed.Enti.Regionali.per.la.Formazione,.la.Ricerca.e.l'Ambiente.csv 2>&1 >out/Agenzie.ed.Enti.Regionali.per.la.Formazione,.la.Ricerca.e.l'Ambiente.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie,.Enti.e.Consorzi.Pubblici.per.il.Diritto.allo.Studio.Universitario.csv 2>&1 >out/Agenzie,.Enti.e.Consorzi.Pubblici.per.il.Diritto.allo.Studio.Universitario.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Aziende.e.Consorzi.Pubblici.Territoriali.per.l'Edilizia.Residenziale.csv 2>&1 >out/Aziende.e.Consorzi.Pubblici.Territoriali.per.l'Edilizia.Residenziale.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Agenzie.ed.Enti.per.il.Turismo.csv 2>&1 >out/Agenzie.ed.Enti.per.il.Turismo.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Consorzi.Interuniversitari.di.Ricerca.csv 2>&1 >out/Consorzi.Interuniversitari.di.Ricerca.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Enti.e.Istituzioni.di.Ricerca.Pubblici.csv 2>&1 >out/Enti.e.Istituzioni.di.Ricerca.Pubblici.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Consorzi.di.Bacino.Imbrifero.Montano.csv 2>&1 >out/Consorzi.di.Bacino.Imbrifero.Montano.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Regioni,.Province.Autonome.e.loro.Consorzi.e.Associazioni.csv 2>&1 >out/Regioni,.Province.Autonome.e.loro.Consorzi.e.Associazioni.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Stazioni.Appaltanti.csv 2>&1 >Stazioni.Appaltanti.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Stazioni.Appaltanti.Gestori.di.Pubblici.Servizi.csv 2>&1 >out/Stazioni.Appaltanti.Gestori.di.Pubblici.Servizi.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Enti.Pubblici.Non.Economici.csv 2>&1 >out/Enti.Pubblici.Non.Economici.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Universita'.e.Istituti.di.Istruzione.Universitaria.Pubblici.csv 2>&1 >out/Universita'.e.Istituti.di.Istruzione.Universitaria.Pubblici.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Enti.Pubblici.Produttori.di.Servizi.Assistenziali,.Ricreativi.e.Culturali..csv 2>&1 >out/Enti.Pubblici.Produttori.di.Servizi.Assistenziali,.Ricreativi.e.Culturali..$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Province.e.loro.Consorzi.e.Associazioni.csv 2>&1 >out/Province.e.loro.Consorzi.e.Associazioni.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Enti.di.Regolazione.dei.Servizi.Idrici.e.o.dei.Rifiuti.csv 2>&1 >out/Enti.di.Regolazione.dei.Servizi.Idrici.e.o.dei.Rifiuti.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Camere.di.Commercio,.Industria,.Artigianato.e.Agricoltura.e.loro.Unioni.Regionali.csv 2>&1 >out/Camere.di.Commercio,.Industria,.Artigianato.e.Agricoltura.e.loro.Unioni.Regionali.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Istituzioni.per.l'Alta.Formazione.Artistica,.Musicale.e.Coreutica.-.AFAM.csv 2>&1 >out/Istituzioni.per.l'Alta.Formazione.Artistica,.Musicale.e.Coreutica.-.AFAM.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Aziende.Ospedaliere,.Aziende.Ospedaliere.Universitarie,.Policlinici.e.Istituti.di.Ricovero.e.Cura.a.Carattere.Scientifico.Pubblici.csv 2>&1 >out/Aziende.Ospedaliere,.Aziende.Ospedaliere.Universitarie,.Policlinici.e.Istituti.di.Ricovero.e.Cura.a.Carattere.Scientifico.Pubblici.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Societa'.in.Conto.Economico.Consolidato.csv 2>&1 >out/Societa'.in.Conto.Economico.Consolidato.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Aziende.Sanitarie.Locali.csv 2>&1 >out/Aziende.Sanitarie.Locali.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Automobile.Club.Federati.ACI.csv 2>&1 >out/Automobile.Club.Federati.ACI.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Parchi.Nazionali,.Consorzi.e.Enti.Gestori.di.Parchi.e.Aree.Naturali.Protette.csv 2>&1 >out/Parchi.Nazionali,.Consorzi.e.Enti.Gestori.di.Parchi.e.Aree.Naturali.Protette.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Comunita'.Montane.e.loro.Consorzi.e.Associazioni.csv 2>&1 >out/Comunita'.Montane.e.loro.Consorzi.e.Associazioni.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Consorzi.tra.Amministrazioni.Locali.csv 2>&1 >out/Consorzi.tra.Amministrazioni.Locali.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Altri.Enti.Locali.csv 2>&1 >out/Altri.Enti.Locali.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Aziende.Pubbliche.di.Servizi.alla.Persona.csv 2>&1 >out/Aziende.Pubbliche.di.Servizi.alla.Persona.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Unioni.di.Comuni.e.loro.Consorzi.e.Associazioni.csv 2>&1 >out/Unioni.di.Comuni.e.loro.Consorzi.e.Associazioni.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Gestori.di.Pubblici.Servizi.csv 2>&1 >out/Gestori.di.Pubblici.Servizi.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Federazioni.Nazionali,.Ordini,.Collegi.e.Consigli.Professionali.csv 2>&1 >out/Federazioni.Nazionali,.Ordini,.Collegi.e.Consigli.Professionali.$url.out &
wait
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Comuni.e.loro.Consorzi.e.Associazioni.csv 2>&1 >out/Comuni.e.loro.Consorzi.e.Associazioni.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Istituti.di.Istruzione.Statale.di.Ogni.Ordine.e.Grado.csv 2>&1 >out/Istituti.di.Istruzione.Statale.di.Ogni.Ordine.e.Grado.$url.out &
nohup python3 01_valida_verifica_url.py -v -t $timeout -u $url -i per.categorie/Nome.categoria.csv 2>&1 >Nome.categoria.$url.out &
