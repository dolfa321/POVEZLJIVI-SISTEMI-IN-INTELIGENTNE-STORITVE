import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from keras.losses import MeanSquaredError

def load_workout_model(model_base_path):
    """
    Load a saved workout model from .h5 and .pkl files

    Args:
        model_base_path (str): Base path of the model files (without extensions)

    Returns:
        A reconstructed WorkoutPercentileModel-like object
    """

    # Create a dummy class to hold the loaded model
    class LoadedWorkoutModel:
        def __init__(self):
            pass

    loaded_model = LoadedWorkoutModel()

    try:
        # Load Keras model
        #loaded_model.model = tf.keras.models.load_model(f"{model_base_path}.h5")
        loaded_model.model = tf.keras.models.load_model(
            f"{model_base_path}.h5",
            compile=False
        )

        # Load attributes
        attrs = joblib.load(f"{model_base_path}_attrs.pkl")
        for key, value in attrs.items():
            setattr(loaded_model, key, value)

        # Add the predict_percentile method
        def predict_percentile(self, new_workout):
            """
            Predict the percentile of a new workout.
            Accepts either a dictionary or list of values in order: HRmax, HR%, TLI, MET, WEI
            """
            # Convert input to numpy array
            if isinstance(new_workout, dict):
                input_data = np.array([new_workout[feat] for feat in self.features]).reshape(1, -1)
            else:
                input_data = np.array(new_workout).reshape(1, -1)

            # Scale the input
            scaled_input = self.scaler.transform(input_data)

            # Predict (output is 0-1, so we multiply by 100 to get percentile)
            percentile = self.model.predict(scaled_input, verbose=0)[0][0] * 100

            return round(percentile, 2)

        loaded_model.predict_percentile = predict_percentile.__get__(loaded_model)

        # Add the get_improvement_recommendations method
        def get_improvement_recommendations(self, new_workout):
            """
            Provides recommendations to improve the workout based on comparison with top workouts.
            """
            if isinstance(new_workout, list):
                # Convert list to dict if needed
                new_workout = dict(zip(self.features, new_workout))

            recommendations = {}
            for metric in self.features:
                current_value = new_workout[metric]
                target_value = self.top_metrics[metric]

                if metric == 'HRmax':
                    diff = target_value - current_value
                    if diff > 5:
                        recommendations[
                            metric] = f"Increase max heart rate by {diff:.1f} bpm through more intense intervals"
                    elif diff < -5:
                        recommendations[metric] = "Your HRmax is unusually high - consider consulting a doctor"

                elif metric == 'HR%':
                    diff = target_value - current_value
                    if diff > 5:
                        recommendations[
                            metric] = f"Spend more time in higher heart rate zones (aim for {target_value:.1f}% of max)"

                elif metric == 'TLI':
                    diff = (target_value - current_value) / target_value
                    if diff > 0.2:
                        recommendations[
                            metric] = f"Increase total workout load by {diff * 100:.1f}% through longer duration or higher intensity"

                elif metric == 'MET':
                    diff = target_value - current_value
                    if diff > 0.5:
                        recommendations[metric] = f"Choose more vigorous activities to increase MET score by {diff:.1f}"

                elif metric == 'WEI':
                    diff = target_value - current_value
                    if diff > 0.2:
                        recommendations[metric] = "Increase workout efficiency by improving form or adding resistance"
                    elif diff < -0.2:
                        recommendations[metric] = "Your WEI is unusually high - ensure you're not overtraining"

            # General recommendations based on percentile
            percentile = self.predict_percentile(new_workout)
            if percentile < 50:
                recommendations[
                    'general'] = "Focus on consistency first - aim for regular workouts before increasing intensity"
            elif percentile < 75:
                recommendations['general'] = "Try incorporating interval training to boost your workout quality"
            else:
                recommendations['general'] = "Maintain your excellent workout routine with proper recovery"

            return recommendations

        loaded_model.get_improvement_recommendations = get_improvement_recommendations.__get__(loaded_model)

        return loaded_model

    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None


def test_model_with_hardcoded_data(model_path):
    """
    Test the loaded model with hardcoded workout data

    Args:
        model_path (str): Base path to the model files (without extensions)
    """
    # Load the model
    model = load_workout_model(model_path)
    if model is None:
        print("Failed to load model. Please check the path.")
        return

    print("\nWorkout Model Tester")
    print("-------------------")
    print(f"Testing model: {model_path}\n")

    # Hardcoded test workouts
    test_workouts = {
        "beginner": {
            'HRmax': 150,
            'HR%': 70,
            'TLI': 5000,
            'MET': 5,
            'WEI': 0.5
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
            'HRmax': 208,
            'HR%': 100,
            'TLI': 20800,
            'MET': 10,
            'WEI': 2
        }
    }

    # Test each workout
    for level, workout in test_workouts.items():
        percentile = model.predict_percentile(workout)
        print(f"\n{level.capitalize()} workout is in the {percentile}th percentile")

        recommendations = model.get_improvement_recommendations(workout)
        print("\nRecommendations:")
        for metric, recommendation in recommendations.items():
            print(f"- {metric}: {recommendation}")

    # Print model summary
    print("\nModel architecture:")
    model.model.summary()

def predict_user_workout_interactive(model_path):
    """
    Load model and allow user to input workout data manually via terminal.
    Predict percentile and provide recommendations.
    """
    model = load_workout_model(model_path)
    if model is None:
        print("Failed to load model. Please check the path.")
        return

    print("\nEnter your workout data to see your percentile and get personalized feedback.")

    try:
        user_workout = {
            'HRmax': float(input("Enter your max heart rate (HRmax): ")),
            'HR%': float(input("Enter your heart rate percentage (HR%): ")),
            'TLI': float(input("Enter your total load index (TLI): ")),
            'MET': float(input("Enter your MET score: ")),
            'WEI': float(input("Enter your workout efficiency index (WEI): "))
        }

        # Predict
        user_percentile = model.predict_percentile(user_workout)
        print(f"\nYour workout is in the {user_percentile}th percentile.")

        # Recommendations
        user_recommendations = model.get_improvement_recommendations(user_workout)
        print("\nPersonalized Recommendations:")
        for metric, rec in user_recommendations.items():
            print(f"- {metric}: {rec}")

    except Exception as e:
        print(f"\nInvalid input or error: {str(e)}")


if __name__ == "__main__":
    import argparse

    # Set up command line arguments
    # parser = argparse.ArgumentParser(description='Test a workout model with hardcoded data')
    # parser.add_argument('model_path', help='Base path to the model files (without extensions)')
    # args = parser.parse_args()

    # Run the tester with hardcoded data
    # test_model_with_hardcoded_data(args.model_path)
    #test_model_with_hardcoded_data('models/Running')
    #predict_user_workout_interactive('models/Running')

    print("Workout Predictor Menu")
    print("----------------------------")
    print("1. Test predefined workouts (beginner, intermediate, etc.)")
    print("2. Enter your own workout data")
    print("0. Exit")

    choice = input("Select an option (0–2): ")

    if choice == "1":
        test_model_with_hardcoded_data('../models/Running')
    elif choice == "2":
        predict_user_workout_interactive('../models/Running')
    elif choice == "0":
        print("Exiting")
    else:
        print("Invalid choice. Please select 0, 1, or 2.")
