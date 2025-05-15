import os
import glob
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy.stats import percentileofscore


class ModelOdstotkovVadbe:
    def __init__(self, pot_do_podatkov):
        """
        Inicializiraj model z vadbenimi podatki iz CSV datoteke.

        Args:
            pot_do_podatkov (str): Pot do CSV datoteke, ki vsebuje vadbene podatke
        """
        # Naloži in pripravi podatke
        df = pd.read_csv(pot_do_podatkov)
        self.lastnosti = ['HRmax', 'HR%', 'TLI', 'MET', 'WEI']
        self.podatki_vadbe = df[self.lastnosti]

        # Izračunaj odstotke za vsako vadbo v podatkovni zbirki
        skalirnik = StandardScaler()
        skalirani_podatki = skalirnik.fit_transform(self.podatki_vadbe)
        sestavljeni_rezultati = skalirani_podatki.mean(axis=1)
        self.odstotki = np.array([percentileofscore(sestavljeni_rezultati, rezultat)
                                  for rezultat in sestavljeni_rezultati])

        # Shrani metrike za zgornjih 10% vadb za primerjavo
        prag_top_10 = np.percentile(self.odstotki, 90)
        self.najboljse_vadbe = self.podatki_vadbe[self.odstotki >= prag_top_10]
        self.najboljse_metrike = {
            'HRmax': self.najboljse_vadbe['HRmax'].median(),
            'HR%': self.najboljse_vadbe['HR%'].median(),
            'TLI': self.najboljse_vadbe['TLI'].median(),
            'MET': self.najboljse_vadbe['MET'].median(),
            'WEI': self.najboljse_vadbe['WEI'].median()
        }

        # Pripravi podatke za nevronsko mrežo
        self.X = self.podatki_vadbe.values
        self.y = self.odstotki / 100  # Prilagodi na obseg 0-1

        # Razdeli podatke
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42)

        # Skaliranje lastnosti
        self.skalirnik = StandardScaler()
        self.X_train = self.skalirnik.fit_transform(self.X_train)
        self.X_test = self.skalirnik.transform(self.X_test)

        # Zgradi in treniraj model
        self.model = self._zgradi_model()
        self._treniraj_model()

    def _zgradi_model(self):
        """Zgradi arhitekturo nevronske mreže"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(5,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer='adam',
                      loss='mse',
                      metrics=['mae'])
        return model

    def _treniraj_model(self, epohe=100, velikost_skupka=32):
        """Treniraj nevronsko mrežo"""
        zgodnje_ustavljanje = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True)

        self.zgodovina = self.model.fit(
            self.X_train, self.y_train,
            validation_data=(self.X_test, self.y_test),
            epochs=epohe,
            batch_size=velikost_skupka,
            callbacks=[zgodnje_ustavljanje],
            verbose=0)

    def napovej_odstotek(self, nova_vadba):
        """
        Napovej odstotek za novo vadbo.

        Args:
            nova_vadba (dict ali list): Podatki o novi vadbi, ki vsebujejo vrednosti za:
                HRmax, HR%, TLI, MET, WEI (v tem vrstnem redu, če uporabljate seznam)

        Returns:
            float: Odstotek (0-100)
        """
        # Pretvori vhod v numpy array
        if isinstance(nova_vadba, dict):
            vhodni_podatki = np.array([nova_vadba[lastnost] for lastnost in self.lastnosti]).reshape(1, -1)
        else:
            vhodni_podatki = np.array(nova_vadba).reshape(1, -1)

        # Skaliraj vhod
        skaliran_vhod = self.skalirnik.transform(vhodni_podatki)

        # Napovej (izhod je 0-1, zato ga pomnožimo s 100 za odstotek)
        odstotek = self.model.predict(skaliran_vhod, verbose=0)[0][0] * 100

        return round(odstotek, 2)

    def pridobi_priporocila_za_izboljsanje(self, nova_vadba):
        """
        Priskrbi priporočila za izboljšanje vadbe na podlagi primerjave z najboljšimi vadbami.

        Args:
            nova_vadba (dict): Slovar, ki vsebuje metrike vadbe

        Returns:
            dict: Slovar s priporočili za vsako metriko
        """
        priporocila = {}

        # Primerjaj vsako metriko z najboljšimi vadbami
        for metrika in self.lastnosti:
            trenutna_vrednost = nova_vadba[metrika]
            ciljna_vrednost = self.najboljse_metrike[metrika]

            if metrika == 'HRmax':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 5:
                    priporocila[
                        metrika] = f"Povečajte maksimalni srčni utrip za {razlika:.1f} bpm z bolj intenzivnimi intervali"
                elif razlika < -5:
                    priporocila[metrika] = "Vaš HRmax je nenavadno visok - razmislite o posvetu z zdravnikom"

            elif metrika == 'HR%':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 5:
                    priporocila[
                        metrika] = f"Preživite več časa v višjih območjih srčnega utripa (ciljajte na {ciljna_vrednost:.1f}% maksimalnega)"

            elif metrika == 'TLI':
                razlika = (ciljna_vrednost - trenutna_vrednost) / ciljna_vrednost
                if razlika > 0.2:
                    priporocila[
                        metrika] = f"Povečajte skupno obremenitev vadbe za {razlika * 100:.1f}% z daljšim trajanjem ali večjo intenzivnostjo"

            elif metrika == 'MET':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 0.5:
                    priporocila[metrika] = f"Izberite bolj energične aktivnosti za povečanje MET rezultata za {razlika:.1f}"

            elif metrika == 'WEI':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 0.2:
                    priporocila[metrika] = "Izboljšajte učinkovitost vadbe z izboljšanjem forme ali dodajanjem odpornosti"
                elif razlika < -0.2:
                    priporocila[metrika] = "Vaš WEI je nenavadno visok - preverite, da ne pretiravate z vadbo"

        # Splošna priporočila na podlagi odstotka
        odstotek = self.napovej_odstotek(nova_vadba)
        if odstotek < 50:
            priporocila[
                'splošno'] = "Osredotočite se na doslednost - najprej ciljajte na redne vadbe, preden povečate intenzivnost"
        elif odstotek < 75:
            priporocila['splošno'] = "Poskusite vključiti intervalni trening za izboljšanje kakovosti vadbe"
        else:
            priporocila['splošno'] = "Vzdržujte odlično vadbeno rutino z ustreznim okrevanjem"

        return priporocila

    def shrani(self, pot_datoteke):
        """
        Shrani komponente modela v datoteke z razširitvami .h5 in .pkl

        Args:
            pot_datoteke (str): Osnovna pot za shranjevanje datotek (brez razširitve)
        """
        # Shrani Keras model v .h5 formatu
        self.model.save(f"{pot_datoteke}.h5")

        # Shrani skalirnik in druge atribute v pickle datoteko
        shrani_slovar = {
            'lastnosti': self.lastnosti,
            'najboljse_metrike': self.najboljse_metrike,
            'skalirnik': self.skalirnik
        }
        joblib.dump(shrani_slovar, f"{pot_datoteke}_atributi.pkl")


def ustvari_in_shrani_modele(podatkovni_dir="sorted_and_calculated_data",
                             modelni_dir="models",
                             vzorec_datotek="*_analysis.csv"):
    """
    Obdelaj vse analitične datoteke v imeniku in shrani trenirane modele.

    Argumenti:
        podatkovni_dir (str): Imenik, ki vsebuje CSV datoteke.
        modelni_dir (str): Imenik za shranjevanje treniranih modelov.
        vzorec_datotek (str): Vzorec za iskanje analitičnih datotek.
    """
    # Ustvari imenik za modele, če ne obstaja
    os.makedirs(modelni_dir, exist_ok=True)

    # Poišči vse analitične datoteke
    analiticne_datoteke = glob.glob(os.path.join(podatkovni_dir, vzorec_datotek))

    if not analiticne_datoteke:
        print(f"Ni datotek, ki ustrezajo {vzorec_datotek} v {podatkovni_dir}")
        return

    print(f"Najdenih {len(analiticne_datoteke)} analitičnih datotek za obdelavo...")

    for pot_datoteke in analiticne_datoteke:
        # Izvleci osnovno ime (npr. "Running" iz "Running_analysis.csv")
        osnovno_ime = os.path.basename(pot_datoteke).split('_')[0]
        osnovna_pot_modela = os.path.join(modelni_dir, osnovno_ime)

        print(f"\nObdelujem {osnovno_ime}...")

        try:
            # Ustvari in treniraj model
            model = ModelOdstotkovVadbe(pot_datoteke)

            # Shrani komponente modela
            model.save(osnovna_pot_modela)
            print(f"Uspešno shranjeno {osnovno_ime}.h5 in {osnovno_ime}_attrs.pkl")

            # Testiraj z vzorčno vadbo
            testna_vadba = {
                'HRmax': 160,
                'HR%': 75,
                'TLI': 7000,
                'MET': 6.5,
                'WEI': 1.1
            }
            percentil = model.predict_percentile(testna_vadba)
            print(f"  Percentil testne vadbe: {percentil}")

            # Prikaži nekaj priporočil
            priporocila = model.get_improvement_recommendations(testna_vadba)
            print("  Vzorčna priporočila:")
            for metrika, prip in list(priporocila.items())[:2]:  # Prikaži prvi 2 priporočili
                print(f"  - {metrika}: {prip}")

        except Exception as e:
            print(f"Napaka pri obdelavi {pot_datoteke}: {str(e)}")

    print("\nVsi modeli so obdelani!")


def nalozi_model_vadbe(osnovna_pot_modela):
    """
    Naloži shranjen model vadbe iz .h5 in .pkl datotek.

    Argumenti:
        osnovna_pot_modela (str): Osnovna pot do datotek modela (brez končnic).

    Vrne:
        Rekonstruiran objekt, podoben WorkoutPercentileModel (poenostavljena različica).
    """

    # Ustvari pomožni razred za shranjevanje naloženega modela
    class NalozenModelVadbe:
        def __init__(self):
            pass

    nalozen_model = NalozenModelVadbe()

    # Naloži Keras model
    nalozen_model.model = tf.keras.models.load_model(f"{osnovna_pot_modela}.h5")

    # Naloži atribute
    atributi = joblib.load(f"{osnovna_pot_modela}_attrs.pkl")
    for kljuc, vrednost in atributi.items():
        setattr(nalozen_model, kljuc, vrednost)

    # Dodaj metodo za napovedovanje percentila
    def napovej_percentil(self, nova_vadba):
        # Pretvori vhod v numpy array
        if isinstance(nova_vadba, dict):
            vhodni_podatki = np.array([nova_vadba[lastnost] for lastnost in self.features]).reshape(1, -1)
        else:
            vhodni_podatki = np.array(nova_vadba).reshape(1, -1)

        # Skaliraj vhod
        skaliran_vhod = self.scaler.transform(vhodni_podatki)

        # Napovej (izhod je 0-1, zato ga pomnožimo s 100 za percentil)
        percentil = self.model.predict(skaliran_vhod, verbose=0)[0][0] * 100

        return round(percentil, 2)

    nalozen_model.napovej_percentil = napovej_percentil.__get__(nalozen_model)

    # Dodaj metodo za pridobivanje priporočil za izboljšanje
    def pridobi_priporocila_za_izboljsanje(self, nova_vadba):
        priporocila = {}
        for metrika in self.features:
            trenutna_vrednost = nova_vadba[metrika]
            ciljna_vrednost = self.top_metrics[metrika]

            if metrika == 'HRmax':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 5:
                    priporocila[
                        metrika] = f"Povečajte maksimalni srčni utrip za {razlika:.1f} bpm z bolj intenzivnimi intervali"
                elif razlika < -5:
                    priporocila[metrika] = "Vaš HRmax je nenavadno visok - razmislite o posvetu z zdravnikom"

            elif metrika == 'HR%':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 5:
                    priporocila[
                        metrika] = f"Preživite več časa v višjih območjih srčnega utripa (ciljajte na {ciljna_vrednost:.1f}% maksimalnega)"

            elif metrika == 'TLI':
                razlika = (ciljna_vrednost - trenutna_vrednost) / ciljna_vrednost
                if razlika > 0.2:
                    priporocila[
                        metrika] = f"Povečajte skupno obremenitev vadbe za {razlika * 100:.1f}% z daljšim trajanjem ali večjo intenzivnostjo"

            elif metrika == 'MET':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 0.5:
                    priporocila[metrika] = f"Izberite bolj energične aktivnosti za povečanje MET rezultata za {razlika:.1f}"

            elif metrika == 'WEI':
                razlika = ciljna_vrednost - trenutna_vrednost
                if razlika > 0.2:
                    priporocila[metrika] = "Izboljšajte učinkovitost vadbe z izboljšanjem forme ali dodajanjem odpornosti"
                elif razlika < -0.2:
                    priporocila[metrika] = "Vaš WEI je nenavadno visok - preverite, da ne pretiravate z vadbo"

        percentil = self.napovej_percentil(nova_vadba)
        if percentil < 50:
            priporocila[
                'splošno'] = "Osredotočite se na doslednost - najprej ciljajte na redne vadbe, preden povečate intenzivnost"
        elif percentil < 75:
            priporocila['splošno'] = "Poskusite vključiti intervalni trening za izboljšanje kakovosti vadbe"
        else:
            priporocila['splošno'] = "Vzdržujte odlično vadbeno rutino z ustreznim okrevanjem"

        return priporocila

    nalozen_model.pridobi_priporocila_za_izboljsanje = pridobi_priporocila_za_izboljsanje.__get__(nalozen_model)

    return nalozen_model


if __name__ == "__main__":
    ustvari_in_shrani_modele()
