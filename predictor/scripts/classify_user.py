import os
import pandas as pd
from predictor.scripts.fit_to_csv import parse_fit_file
from predictor.scripts.test_for_hardcoded_user_data import \
    load_workout_model


def izracunaj_formule(df):
    df['HRmax'] = 208 - 0.7 * df['Starost']
    df['HR%'] = (df['Srčni utrip (bpm)'] / df['HRmax']) * 100
    df['TLI'] = df['Srčni utrip (bpm)'] * df['Trajanje vadbe (min)']
    df['MET'] = (df['Srčni utrip (bpm)'] / df['Počivalni srčni utrip (bpm)']) * 3.5
    df['WEI'] = (df['HR%'] * df['Razdalja (km)']) / df['Trajanje vadbe (min)']
    return df


def pridobi_najnovejse_podatke_o_vadbi(df):
    """Predpostavlja, da zadnja vrstica predstavlja najnovejše podatke o vadbi"""
    zadnja = df.iloc[-1]
    return {
        'HRmax': zadnja['HRmax'],
        'HR%': zadnja['HR%'],
        'TLI': zadnja['TLI'],
        'MET': zadnja['MET'],
        'WEI': zadnja['WEI']
    }


def razvrsti_uporabnika(pot, tip_vadbe, starost):
    parse_fit_file(pot, pot + ".csv", starost, tip_vadbe)
    print(f"✅ Podatki iz datoteke 'teon' so bili analizirani in shranjeni v 'output.csv'")

    df = pd.read_csv(pot + ".csv")
    df = izracunaj_formule(df)
    df.to_csv(pot + "class.csv", index=False)

    pot_modela = f"../models/{tip_vadbe}"

    model = load_workout_model(pot_modela)
    if model is None:
        print(f"❌ Ni uspelo naložiti modela za {tip_vadbe}")
        return

    podatki_o_vadbi = pridobi_najnovejse_podatke_o_vadbi(df)
    print(f"📊 Najnovejši podatki o vadbi: {podatki_o_vadbi}")

    percentil = model.predict_percentile(podatki_o_vadbi)
    priporocila = model.get_improvement_recommendations(podatki_o_vadbi)

    print(f"\n📊 Vaša vadba je v {percentil}. percentilu.\n")
    print("💡 Priporočila:")
    for kljuc, vrednost in priporocila.items():
        print(f"- {kljuc}: {vrednost}")
    return percentil, priporocila


def test():
    parse_fit_file("../teon2.fit", "output.csv")
    print(f"✅ Podatki iz datoteke 'teon' so bili analizirani in shranjeni v 'output.csv'")

    df = pd.read_csv("output.csv")
    df = izracunaj_formule(df)
    df.to_csv("leon_class.csv", index=False)

    # Trdo kodiran tip vadbe in pot modela
    tip_vadbe = "Tek"
    pot_modela = f"../models/{tip_vadbe}"

    # Naloži model
    model = load_workout_model(pot_modela)
    if model is None:
        print(f"❌ Ni uspelo naložiti modela za {tip_vadbe}")
        return

    # Pridobi metrike za napoved
    podatki_o_vadbi = pridobi_najnovejse_podatke_o_vadbi(df)
    print(f"📊 Najnovejši podatki o vadbi: {podatki_o_vadbi}")

    # Napoved percentila in izpis priporočil
    percentil = model.predict_percentile(podatki_o_vadbi)
    priporocila = model.get_improvement_recommendations(podatki_o_vadbi)

    print(f"\n📊 Vaša vadba je v {percentil}. percentilu.\n")
    print("💡 Priporočila:")
    for kljuc, vrednost in priporocila.items():
        print(f"- {kljuc}: {vrednost}")


if __name__ == "__main__":
    test()