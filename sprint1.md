# Opravljene naloge v tem sprintu

##  1. Priprava in analiza podatkov o treningih
- Uvoz vhodnih podatkov iz `.csv` datoteke (`workout_fitness_tracker_data.csv`)
- Preverjanje in potrjevanje prisotnosti zahtevanih stolpcev (npr. *Workout Type*, *Heart Rate*, *Workout Duration* ...)
- Razdelitev podatkov glede na tip treninga

##  2. Implementacija funkcije za izračun metrik treninga
- Implementacija funkcije `calculate_formulas()`, ki izračuna:
  - **HRmax** (maksimalni srčni utrip)
  - **HR%** (odstotek maksimalnega utripa)
  - **TLI** (indeks obremenitve treninga)
  - **MET** (metabolični ekvivalent)
  - **WEI** (indeks učinkovitosti treninga)
- Uporaba funkcije na vsakem tipu treninga posebej in shranjevanje rezultatov v ločene `.csv` datoteke

## 3. Ustvarjanje in treniranje modela za ocenjevanje treningov
- Zasnova razreda `WorkoutPercentileModel`, ki omogoča:
  - Uvoz analiziranih podatkov za vsak tip treninga
  - Izračun percentilov in identifikacijo najboljših 10 % treningov
  - Pripravo podatkov za učenje modela
  - Gradnjo nevronske mreže s 3 plastmi (64, 32, 1 nevron)
  - Uporabo ReLU in sigmoid aktivacijskih funkcij
  - Učenje z optimizatorjem Adam in uporabo zgodnjega ustavljanja

## 4. Implementacija dodatnih funkcionalnosti modela
- Implementacija metod za:
  - `predict_percentile()` – napoved percentila novega treninga
  - `get_improvement_recommendations()` – generiranje priporočil za izboljšavo treninga
  - `save()` in `load_workout_model()` – shranjevanje in nalaganje modelov (.h5 in .pkl)

## 5. Testiranje modela z vnaprej pripravljenimi podatki "hardcoded"
- Implementacija funkcije `test_model_with_hardcoded_data()`
- Ustvarjanje in uporaba štirih prednastavljenih primerov treningov:
  - *beginner*, *intermediate*, *advanced*, *elite*
- Testne napovedi percentilov in preverjanje priporočil za različne tipe uporabnikov
- Verifikacija pravilnega nalaganja in delovanja modela iz shranjenih datotek

## 6. Organizacija projektne strukture in kodne baze
- Ustvarjanje strukturirane mape za modele in izhodne datoteke
- Zagotovitev, da ima vsak tip treninga svoje ločene modele
- Dokumentiranje logike obdelave podatkov in izračunanih metrik
