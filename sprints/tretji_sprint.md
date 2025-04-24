# Poročilo o tretjem sprintu  

V tretjem sprintu smo dosegli pomembne napredke pri razvoju aplikacije za analizo fitnes dejavnosti. Glavni fokus je bil na izboljšavah čelnega in zalednega dela sistema, kar je prineslo opazne izboljšave za končne uporabnike.  

## Opravljena dela  

Na strani uporabniškega vmesnika smo implementirali podrobnejši izpis rezultatov telovadbe, ki zdaj uporabnikom omogoča pregled nad ključnimi metriki in statistikami njihovih vadbenih aktivnosti. Ta izboljšava je bistveno povečala preglednost podatkov in olajšala interpretacijo rezultatov.  

V zalednem delu sistema smo razvili napredno funkcionalnost za obdelavo podatkov. Ključna novost je parser za datoteke v formatu .FIT, ki avtomatsko ekstrahira in obdeluje podatke iz različnih fitnes naprav. Ti podatki se nato prenesejo v naš analitični model, ki na njihovi osnovi generira personalizirane vpoglede.  

Preko API klica sistem zdaj uporabnikom ponuja dve ključni funkcionalnosti:  
1. Vrne konkretne predloge za izboljšave v vadbeni rutini  
2. Podaja odstotno oceno kakovosti opravljene vadbe glede na uporabnikove zgodovinske podatke in cilje  

## Načrt za naslednji sprint  

V naslednjem sprintu se bomo osredotočili na naslednje ključne točke:  

### Optimizacija aplikacije  
- **Izboljšanje zmogljivosti**: Analiza in optimizacija počasnejših delov aplikacije, zlasti pri obdelavi velikih .FIT datotek  
- **Stabilnost API-ja**: Nadgradnja strežniške logike za bolj zanesljive odzive in obvladovanje obremenitev  
- **Optimizacija uporabniškega vmesnika**: Zmanjšanje časa nalaganja, izboljšanje odzivnosti in prilagoditev za različne naprave  

### Priprava celotnega poročila  
- **Struktura dokumentacije**: Začetek pisanja končnega poročila z razdelitvijo na tehnične in poslovne vidike projekta  
- **Zbiranje metrik**: Dokumentiranje dosežkov, izkušenj in potencialnih izboljšav za prihodnje različice  
- **Priprava prezentacije**: Oblikovanje preglednih gradiv za predstavitev rezultatov
