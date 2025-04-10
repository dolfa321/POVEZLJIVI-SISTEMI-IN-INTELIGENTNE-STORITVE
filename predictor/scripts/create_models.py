import os
import glob
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy.stats import percentileofscore


class WorkoutPercentileModel:
    def __init__(self, data_path):
        """
        Initialize the model with workout data from a CSV file.

        Args:
            data_path (str): Path to the CSV file containing workout data
        """
        # Load and prepare data
        df = pd.read_csv(data_path)
        self.features = ['HRmax', 'HR%', 'TLI', 'MET', 'WEI']
        self.workout_data = df[self.features]

        # Calculate percentiles for each workout in the dataset
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.workout_data)
        composite_scores = scaled_data.mean(axis=1)
        self.percentiles = np.array([percentileofscore(composite_scores, score)
                                     for score in composite_scores])

        # Store metrics of top 10% workouts for comparison
        top_10_threshold = np.percentile(self.percentiles, 90)
        self.top_workouts = self.workout_data[self.percentiles >= top_10_threshold]
        self.top_metrics = {
            'HRmax': self.top_workouts['HRmax'].median(),
            'HR%': self.top_workouts['HR%'].median(),
            'TLI': self.top_workouts['TLI'].median(),
            'MET': self.top_workouts['MET'].median(),
            'WEI': self.top_workouts['WEI'].median()
        }

        # Prepare data for neural network
        self.X = self.workout_data.values
        self.y = self.percentiles / 100  # Scale to 0-1 range

        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42)

        # Feature scaling
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

        # Build and train model
        self.model = self._build_model()
        self._train_model()

    def _build_model(self):
        """Build the neural network architecture"""
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

    def _train_model(self, epochs=100, batch_size=32):
        """Train the neural network"""
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True)

        self.history = self.model.fit(
            self.X_train, self.y_train,
            validation_data=(self.X_test, self.y_test),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping],
            verbose=0)

    def predict_percentile(self, new_workout):
        """
        Predict the percentile of a new workout.

        Args:
            new_workout (dict or list): New workout data containing values for:
                HRmax, HR%, TLI, MET, WEI (in order if using list)

        Returns:
            float: Percentile score (0-100)
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

    def get_improvement_recommendations(self, new_workout):
        """
        Provides recommendations to improve the workout based on comparison with top workouts.

        Args:
            new_workout (dict): Dictionary containing the workout metrics

        Returns:
            dict: Dictionary with recommendations for each metric
        """
        recommendations = {}

        # Compare each metric with top workouts
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

    def save(self, filepath):
        """
        Save the model components to files with .h5 and .pkl extensions

        Args:
            filepath (str): Base path for saving files (without extension)
        """
        # Save Keras model in .h5 format
        self.model.save(f"{filepath}.h5")

        # Save scaler and other attributes in a pickle file
        save_dict = {
            'features': self.features,
            'top_metrics': self.top_metrics,
            'scaler': self.scaler
        }
        joblib.dump(save_dict, f"{filepath}_attrs.pkl")


def create_and_save_models(data_dir="sorted_and_calculated_data",
                           model_dir="models",
                           file_pattern="*_analysis.csv"):
    """
    Process all analysis files in a directory and save trained models

    Args:
        data_dir (str): Directory containing the CSV files
        model_dir (str): Directory to save trained models
        file_pattern (str): Pattern to match analysis files
    """
    # Create models directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)

    # Find all analysis files
    analysis_files = glob.glob(os.path.join(data_dir, file_pattern))

    if not analysis_files:
        print(f"No files matching {file_pattern} found in {data_dir}")
        return

    print(f"Found {len(analysis_files)} analysis files to process...")

    for file_path in analysis_files:
        # Extract base name (e.g., "Running" from "Running_analysis.csv")
        base_name = os.path.basename(file_path).split('_')[0]
        model_base_path = os.path.join(model_dir, base_name)

        print(f"\nProcessing {base_name}...")

        try:
            # Create and train model
            model = WorkoutPercentileModel(file_path)

            # Save the model components
            model.save(model_base_path)
            print(f"Successfully saved {base_name}.h5 and {base_name}_attrs.pkl")

            # Test with a sample workout
            test_workout = {
                'HRmax': 160,
                'HR%': 75,
                'TLI': 7000,
                'MET': 6.5,
                'WEI': 1.1
            }
            percentile = model.predict_percentile(test_workout)
            print(f"  Test workout percentile: {percentile}")

            # Show some recommendations
            recs = model.get_improvement_recommendations(test_workout)
            print("  Sample recommendations:")
            for metric, rec in list(recs.items())[:2]:  # Show first 2 recommendations
                print(f"  - {metric}: {rec}")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    print("\nAll models processed!")


def load_workout_model(model_base_path):
    """
    Load a saved workout model from .h5 and .pkl files

    Args:
        model_base_path (str): Base path of the model files (without extensions)

    Returns:
        A reconstructed WorkoutPercentileModel-like object (simplified version)
    """

    # Create a dummy class to hold the loaded model
    class LoadedWorkoutModel:
        def __init__(self):
            pass

    loaded_model = LoadedWorkoutModel()

    # Load Keras model
    loaded_model.model = tf.keras.models.load_model(f"{model_base_path}.h5")

    # Load attributes
    attrs = joblib.load(f"{model_base_path}_attrs.pkl")
    for key, value in attrs.items():
        setattr(loaded_model, key, value)

    # Add the predict_percentile method
    def predict_percentile(self, new_workout):
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


if __name__ == "__main__":
    create_and_save_models()
