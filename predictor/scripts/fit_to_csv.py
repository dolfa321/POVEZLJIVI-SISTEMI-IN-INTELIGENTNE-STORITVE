import csv
from fitparse import FitFile


def parse_fit_file(fit_path, csv_output_path, age=23, workout_type="Running"):
    fitfile = FitFile(fit_path)

    data = {
        "User ID": "N/A",
        "Age": "N/A",
        "Gender": "N/A",
        "Height (cm)": "N/A",
        "Weight (kg)": "N/A",
        "Workout Type": "N/A",
        "Workout Duration (mins)": 0,
        "Calories Burned": 0,
        "Heart Rate (bpm)": 0,
        "Steps Taken": 0,
        "Distance (km)": 0,
        "Workout Intensity": "N/A",
        "Sleep Hours": "N/A",
        "Water Intake (liters)": "N/A",
        "Daily Calories Intake": "N/A",
        "Resting Heart Rate (bpm)": "N/A",
        "VO2 Max": "N/A",
        "Body Fat (%)": "N/A",
        "Mood Before Workout": "N/A",
        "Mood After Workout": "N/A",
        "HRmax": "N/A",
        "HR%": "", "TLI": "", "MET": "", "WEI": ""
    }

    heart_rates = []
    total_steps = 0
    total_distance = 0.1
    start_time = None
    end_time = None

    for record in fitfile.get_messages("record"):
        values = {field.name: field.value for field in record}
        if "heart_rate" in values:
            heart_rates.append(values["heart_rate"])
        if "steps" in values:
            total_steps += values["steps"]
        if "distance" in values:
            total_distance += values["distance"] / 1000  # meters to km
        if "timestamp" in values:
            if not start_time:
                start_time = values["timestamp"]
            end_time = values["timestamp"]

    if start_time and end_time:
        duration_minutes = (end_time - start_time).total_seconds() / 60
        data["Workout Duration (mins)"] = round(duration_minutes, 2)

    if heart_rates:
        data["Heart Rate (bpm)"] = round(sum(heart_rates) / len(heart_rates), 2)
        data["Resting Heart Rate (bpm)"] = min(heart_rates)

    data["Steps Taken"] = total_steps
    data["Distance (km)"] = round(total_distance, 2)
    data["Age"] = age
    data["Workout Type"] = workout_type

    for msg in fitfile.get_messages():
        if msg.name in ("session", "activity", "file_id", "user_profile"):
            for field in msg:
                if field.name == "total_calories":
                    data["Calories Burned"] = field.value
                elif field.name == "gender":
                    data["Gender"] = field.value.title()
                elif field.name == "age":
                    data["Age"] = field.value
                elif field.name == "weight":
                    data["Weight (kg)"] = round(field.value, 2)
                elif field.name == "height":
                    data["Height (cm)"] = round(field.value * 100, 1)

    with open(csv_output_path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)
