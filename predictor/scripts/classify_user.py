import os
import pandas as pd
from predictor.scripts.fit_to_csv import parse_fit_file
from predictor.scripts.create_models import \
    load_workout_model


def calculate_formulas(df):
    df['HRmax'] = 208 - 0.7 * df['Age']
    df['HR%'] = (df['Heart Rate (bpm)'] / df['HRmax']) * 100
    df['TLI'] = df['Heart Rate (bpm)'] * df['Workout Duration (mins)']
    df['MET'] = (df['Heart Rate (bpm)'] / df['Resting Heart Rate (bpm)']) * 3.5
    df['WEI'] = (df['HR%'] * df['Distance (km)']) / df['Workout Duration (mins)']
    return df


def extract_latest_workout_metrics(df):
    """Assumes latest row represents the latest workout data"""
    last = df.iloc[-1]
    return {
        'HRmax': last['HRmax'],
        'HR%': last['HR%'],
        'TLI': last['TLI'],
        'MET': last['MET'],
        'WEI': last['WEI']
    }


def classify_user(path, workout_type, age):
    parse_fit_file(path, path + ".csv", age, workout_type)
    print(f"✅ Parsed data from 'teon' and saved to 'output.csv'")

    df = pd.read_csv(path + ".csv")
    df = calculate_formulas(df)
    df.to_csv(path + "class.csv", index=False)

    model_path = f"../models/{workout_type}"

    model = load_workout_model(model_path)
    if model is None:
        print(f"❌ Failed to load model for {workout_type}")
        return

    workout_data = extract_latest_workout_metrics(df)
    print(f"📊 Latest workout data extracted: {workout_data}")

    percentile = model.predict_percentile(workout_data)
    recommendations = model.get_improvement_recommendations(workout_data)

    print(f"\n📊 Your workout is in the {percentile}th percentile.\n")
    print("💡 Recommendations:")
    for key, value in recommendations.items():
        print(f"- {key}: {value}")
    return percentile, recommendations


def test():
    parse_fit_file("../teon2.fit", "output.csv")
    print(f"✅ Parsed data from 'teon' and saved to 'output.csv'")

    df = pd.read_csv("output.csv")
    df = calculate_formulas(df)
    df.to_csv("leon_class.csv", index=False)

    # Hardcoded workout type and model path
    workout_type = "Running"
    model_path = f"../models/{workout_type}"

    # Load the model
    model = load_workout_model(model_path)
    if model is None:
        print(f"❌ Failed to load model for {workout_type}")
        return

    # Extract metrics for prediction
    workout_data = extract_latest_workout_metrics(df)
    print(f"📊 Latest workout data extracted: {workout_data}")

    # Predict percentile and print recommendations
    percentile = model.predict_percentile(workout_data)
    recommendations = model.get_improvement_recommendations(workout_data)

    print(f"\n📊 Your workout is in the {percentile}th percentile.\n")
    print("💡 Recommendations:")
    for key, value in recommendations.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    test()
