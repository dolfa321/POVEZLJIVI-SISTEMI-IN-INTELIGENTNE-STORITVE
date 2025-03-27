# Specifikacija kode: Analiza trening podatkov

## 1. Zahtevane vhodne datoteke
- Vhodna datoteka: `workout_fitness_tracker_data.csv`
- Zahtevani stolpci:
  - 'Workout Type' (kategorizacija)
  - 'Age' (številčna vrednost)
  - 'Heart Rate (bpm)' (številčna vrednost)
  - 'Resting Heart Rate (bpm)' (številčna vrednost)
  - 'Workout Duration (mins)' (številčna vrednost)
  - 'Distance (km)' (številčna vrednost)

## 2. Funkcije za obdelavo podatkov

### `calculate_formulas(df: pd.DataFrame) -> pd.DataFrame`
**Parametri:**
- `df`: Vhodni DataFrame s podatki o treningih

**Izračunane metrike:**
1. **HRmax** (Maksimalni srčni utrip)
   - Formula: `208 - 0.7 * Age`
   - Namen: Ocena najvišjega možnega srčnega utripa glede na starost

2. **HR%** (Odstotek maksimalnega srčnega utripa)
   - Formula: `(Heart Rate / HRmax) * 100`
   - Izhod: Odstotek doseženega maksimalnega utripa

3. **TLI** (Indeks obremenitve treninga)
   - Formula: `Heart Rate * Workout Duration`
   - Enote: bpm·min
   - Namen: Kvantificira skupno obremenitev srca

4. **MET** (Metabolični ekvivalent)
   - Formula: `(Heart Rate / Resting Heart Rate) * 3.5`
   - Namen: Meri intenzivnost vadbe glede na mirovanje

5. **WEI** (Indeks učinkovitosti treninga)
   - Formula: `(HR% * Distance) / Workout Duration`
   - Enote: %·km/min
   - Namen: Ocenjuje učinkovitost treninga

**Vrača:**
- Spremenjen DataFrame s 5 novimi izračunanimi stolpci

## 3. Logika obdelave

1. **Razdelitev podatkov:**
   - Identificira unikatne tipe treningov z `df['Workout Type'].unique()`
   - Obdeluje vsak tip treninga posebej

2. **Postopek obdelave:**
   ```python
   za vsak workout_type:
      1. Ustvari podmnožico: df[df['Workout Type'] == workout_type]
      2. Uporabi calculate_formulas()
      3. Izvozi v CSV


# Specifikacija kode: Model za ocenjevanje percentilov treningov

## 1. Struktura kode

### Glavni razred: `WorkoutPercentileModel`
- Glavni razred za ustvarjanje, treniranje in uporabo modelov

### Pomožne funkcije:
1. `create_and_save_models()` - Ustvari in shrani modele za vse tipe treningov
2. `load_workout_model()` - Naloži shranjen model iz datotek

## 2. Podatkovni vhodi

**Zahtevani vhodni podatki:**
- CSV datoteke s podatki o treningih (izhod iz prejšnje analize)
- Oblikovanje: `{tip_treninga}_analysis.csv`
- Zahtevani stolpci:
  - HRmax (Maksimalni srčni utrip)
  - HR% (Odstotek maksimalnega utripa)
  - TLI (Indeks obremenitve treninga)
  - MET (Metabolični ekvivalent)
  - WEI (Indeks učinkovitosti treninga)

## 3. Ključne funkcionalnosti

### Inicializacija modela (`__init__`)
1. Nalaganje podatkov iz CSV
2. Izračun percentilov za vsak trening
3. Identifikacija najboljših 10% treningov
4. Priprava podatkov za nevronsko mrežo
5. Gradnja in treniranje modela

### Metode:
1. `_build_model()` - Zgradi arhitekturo nevronske mreže
   - 3 plasti: 64, 32 in 1 nevron
   - Aktivacijske funkcije: ReLU in sigmoida
   - Optimizacija: Adam

2. `_train_model()` - Trenira model
   - Uporablja zgodnje ustavljanje (early stopping)
   - 100 epoh (privzeto)
   - Velikost serije: 32 (privzeto)

3. `predict_percentile()` - Napove percentil za nov trening
   - Vhod: slovar ali seznam vrednosti
   - Izhod: percentil (0-100)

4. `get_improvement_recommendations()` - Priporedi priporočila za izboljšavo
   - Primerja z najboljšimi treningi
   - Priporedi specifična priporočila za vsako metriko

5. `save()` - Shrani model v datoteke
   - Keras model (.h5)
   - Atributi modela (.pkl)

## 4. Procesiranje modelov

### Funkcija `create_and_save_models()`
1. Ustvari mapo za modele (če ne obstaja)
2. Poišče vse datoteke z analizami treningov
3. Za vsak tip treninga:
   - Ustvari model
   - Shrani model
   - Testira z vzorčnim treningom
   - Priporedi vzorčna priporočila

### Funkcija `load_workout_model()`
1. Naloži Keras model iz .h5 datoteke
2. Naloži atribute iz .pkl datoteke
3. Rekonstruira funkcionalnost originalnega modela

## 5. Izhodni rezultati

**Shranjene datoteke:**
- `{tip_treninga}.h5` - Keras model
- `{tip_treninga}_attrs.pkl` - Atributi modela

**Možnosti uporabe:**
1. Napovedovanje percentila za nove treninge
2. Generiranje priporočil za izboljšavo
3. Analiza učinkovitosti treningov

## 6. Odvisnosti

**Zahtevane knjižnice:**
- pandas
- numpy
- scikit-learn
- tensorflow
- scipy
- joblib

## 7. Primer uporabe

    # Ustvarjanje in shranjevanje modelov
    create_and_save_models()

    # Nalaganje obstoječega modela
    model = load_workout_model("models/Running")

    # Napoved percentila
    new_workout = {
        'HRmax': 185,
        'HR%': 82,
        'TLI': 8500,
        'MET': 8.2,
        'WEI': 1.4
    }
    percentile = model.predict_percentile(new_workout)

    # Pridobitev priporočil
    recommendations = model.get_improvement_recommendations(new_workout)

# Specifikacija kode: Testiranje modela s prednastavljenimi podatki

## 1. Namen kode
- Testiranje naloženega modela za ocenjevanje treningov
- Demonstracija delovanja s prednastavljenimi primeri
- Priprava priporočil za izboljšavo treningov

## 2. Glavne komponente

### Funkcija `load_workout_model(model_base_path)`
**Vhodni parametri:**
- `model_base_path`: Osnovna pot do modela (brez končnic)

**Funkcionalnost:**
1. Naloži Keras model iz `.h5` datoteke
2. Naloži atribute modela iz `.pkl` datoteke
3. Dodaja metode za napovedovanje in priporočila

**Izhod:**
- Objekt `LoadedWorkoutModel` z funkcionalnostjo originalnega modela

### Funkcija `test_model_with_hardcoded_data(model_path)`
**Vhodni parametri:**
- `model_path`: Pot do modela za testiranje

**Funkcionalnost:**
1. Naloži model
2. Ustvari 4 prednastavljene primere treningov:
   - Začetniški (`beginner`)
   - Srednje zahteven (`intermediate`)
   - Napreden (`advanced`)
   - Elite (`elite`)
3. Za vsak primer:
   - Izračuna percentil
   - Pripravi priporočila za izboljšavo
4. Prikaže povzetek arhitekture modela

## 3. Podatkovni modeli

### Primeri treningov:
    
    test_workouts = {
        "beginner": {
            'HRmax': 150,    # Nizek maksimalni utrip
            'HR%': 70,       # 70% maksimalnega utripa
            'TLI': 5000,     # Nizka obremenitev
            'MET': 5,        # Zmerna intenzivnost
            'WEI': 0.5       # Nizka učinkovitost
        },
        "intermediate": {
            'HRmax': 160,
            'HR%': 80,
            'TLI': 8000,
            'MET': 6,
            'WEI': 1
        },
        "advanced": {
            'HRmax': 182.8,
            'HR%': 91.9,
            'TLI': 12264,
            'MET': 8.05,
            'WEI': 1.38
        },
        "elite": {
            'HRmax': 208,    # Zelo visok maksimalni utrip
            'HR%': 100,      # 100% maksimalnega utripa
            'TLI': 20800,    # Zelo visoka obremenitev
            'MET': 10,       # Ekstremna intenzivnost
            'WEI': 2         # Izjemna učinkovitost
        }
}
