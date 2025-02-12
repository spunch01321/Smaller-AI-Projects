import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.ensemble import IsolationForest
import pandas as pd

class PredictiveMaintenance:
    def __init__(self, sequence_length=30, n_features=10):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.lstm_model = self._build_lstm_model()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        
    def _build_lstm_model(self):
        model = Sequential([
            LSTM(64, activation='relu', input_shape=(self.sequence_length, self.n_features), 
                 return_sequences=True),
            Dropout(0.2),
            LSTM(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def preprocess_data(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare time series data for LSTM input"""
        sequences = []
        for i in range(len(data) - self.sequence_length):
            sequences.append(data[i:i + self.sequence_length].values)
        return np.array(sequences)
    
    def train_model(self, X_train, y_train, epochs=50, batch_size=32):
        """Train the LSTM model"""
        history = self.lstm_model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=1
        )
        return history
    
    def detect_anomalies(self, data: np.ndarray) -> np.ndarray:
        """Detect anomalies using Isolation Forest"""
        return self.anomaly_detector.fit_predict(data)
    
    def predict_failure_probability(self, sequence: np.ndarray) -> float:
        """Predict probability of equipment failure"""
        if sequence.shape != (self.sequence_length, self.n_features):
            raise ValueError("Invalid sequence shape")
        sequence = np.expand_dims(sequence, axis=0)
        return self.lstm_model.predict(sequence)[0][0]
    
    def calculate_health_score(self, sequence: np.ndarray) -> float:
        """Calculate equipment health score"""
        failure_prob = self.predict_failure_probability(sequence)
        anomaly_score = self.anomaly_detector.score_samples([sequence.flatten()])[0]
        # Combine both scores for final health score
        health_score = (1 - failure_prob) * (1 + anomaly_score) / 2
        return max(0, min(100, health_score * 100))  # Scale to 0-100

    def generate_maintenance_schedule(self, health_scores: list, threshold: float = 70):
        """Generate maintenance schedule based on health scores"""
        maintenance_schedule = []
        for i, score in enumerate(health_scores):
            if score < threshold:
                maintenance_schedule.append({
                    'equipment_id': i,
                    'health_score': score,
                    'priority': 'High' if score < 50 else 'Medium',
                    'recommended_date': f'Within {max(1, int((score/threshold) * 7))} days'
                })
        return maintenance_schedule

# Example usage
if __name__ == "__main__":
    # Initialize the system
    pm_system = PredictiveMaintenance()
    
    # Generate sample data
    sample_data = pd.DataFrame(np.random.random((1000, 10)))
    sequences = pm_system.preprocess_data(sample_data)
    
    # Train the model
    y = np.random.randint(0, 2, size=(len(sequences),))
    pm_system.train_model(sequences, y)
    
    # Generate predictions
    sequence = sequences[0]
    health_score = pm_system.calculate_health_score(sequence)
    print(f"Equipment Health Score: {health_score:.2f}")
