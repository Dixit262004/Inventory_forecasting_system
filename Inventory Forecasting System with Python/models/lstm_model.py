import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

try:
    # Try importing TensorFlow with compatibility
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TENSORFLOW_AVAILABLE = True
except ImportError as e:
    print(f"TensorFlow not available: {e}")
    TENSORFLOW_AVAILABLE = False

class LSTMForecasterFixed:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.lookback = 30
        
    def create_dataset(self, data, lookback=30):
        """Create dataset for LSTM training"""
        X, y = [], []
        for i in range(lookback, len(data)):
            X.append(data[i-lookback:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)
        
    def forecast(self, data, days=30):
        """Generate forecast using LSTM model"""
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is not available. Please install tensorflow==2.10.0")
            
        # Prepare data
        values = data['quantity_sold'].values.reshape(-1, 1)
        scaled_values = self.scaler.fit_transform(values)
        
        # Use recent data for training
        train_size = min(180, len(scaled_values))
        train_data = scaled_values[-train_size:]
        
        # Create training datasets
        X_train, y_train = self.create_dataset(train_data, self.lookback)
        
        if len(X_train) == 0:
            raise ValueError("Insufficient data for LSTM training")
            
        # Reshape data for LSTM [samples, time steps, features]
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        
        # Build simpler LSTM model for compatibility
        self.model = Sequential([
            LSTM(32, return_sequences=True, input_shape=(self.lookback, 1)),
            Dropout(0.1),
            LSTM(32, return_sequences=False),
            Dropout(0.1),
            Dense(16),
            Dense(1)
        ])
        
        self.model.compile(optimizer='adam', loss='mse')
        
        # Train with fewer epochs for speed
        self.model.fit(X_train, y_train, 
                      batch_size=16, 
                      epochs=30, 
                      verbose=0,
                      validation_split=0.1)
        
        # Generate forecast
        last_sequence = train_data[-self.lookback:]
        forecasts = []
        
        for _ in range(days):
            X_pred = last_sequence.reshape(1, self.lookback, 1)
            pred = self.model.predict(X_pred, verbose=0)
            forecasts.append(pred[0, 0])
            last_sequence = np.append(last_sequence[1:], pred)
            
        # Inverse transform forecasts
        forecasts = np.array(forecasts).reshape(-1, 1)
        forecast_values = self.scaler.inverse_transform(forecasts).flatten()
        
        # Create forecast dataframe
        last_date = data.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days)
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'predicted_demand': forecast_values,
            'type': 'forecast'
        })
        
        # Prepare historical data
        historical_df = pd.DataFrame({
            'date': data.index,
            'quantity_sold': data['quantity_sold'],
            'predicted_demand': data['quantity_sold'],
            'type': 'historical'
        })
        
        # Combine data
        combined_df = pd.concat([historical_df, forecast_df], ignore_index=True)
        
        # Calculate metrics
        metrics = self.calculate_metrics(X_train, y_train)
            
        return combined_df, metrics
    
    def calculate_metrics(self, X_train, y_train):
        """Calculate training metrics"""
        try:
            train_pred = self.model.predict(X_train, verbose=0)
            train_pred = self.scaler.inverse_transform(train_pred.reshape(-1, 1)).flatten()
            train_actual = self.scaler.inverse_transform(y_train.reshape(-1, 1)).flatten()
            
            return {
                'rmse': np.sqrt(mean_squared_error(train_actual, train_pred)),
                'mae': mean_absolute_error(train_actual, train_pred)
            }
        except:
            return {'rmse': 0, 'mae': 0}
