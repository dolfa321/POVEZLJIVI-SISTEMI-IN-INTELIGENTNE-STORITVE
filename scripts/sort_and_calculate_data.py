import pandas as pd

df = pd.read_csv('../workout_fitness_tracker_data.csv')


def calculate_formulas(df):
    df['HRmax'] = 208 - 0.7 * df['Age']
    df['HR%'] = (df['Heart Rate (bpm)'] / df['HRmax']) * 100
    df['TLI'] = df['Heart Rate (bpm)'] * df['Workout Duration (mins)']
    df['MET'] = (df['Heart Rate (bpm)'] / df['Resting Heart Rate (bpm)']) * 3.5
    df['WEI'] = (df['HR%'] * df['Distance (km)']) / df['Workout Duration (mins)']
    return df


workout_types = df['Workout Type'].unique()
for workout in workout_types:
    workout_df = df[df['Workout Type'] == workout].copy()
    workout_df = calculate_formulas(workout_df)
    workout_df.to_csv(f'sorted_and_calculated_data/{workout}_analysis.csv', index=False)

print("Analysis complete. Files saved by workout type.")
