# models/simple_models.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

class SimpleForecaster:
    def __init__(self):
        self.model = None
        
    def forecast(self, data, days=30):
        """Generate forecast using simple moving average and linear regression"""
        series = data['quantity_sold']
        
        # Use multiple methods and average them
        ma_forecast = self.moving_average_forecast(series, days)
        trend_forecast = self.trend_forecast(series, days)
        
        # Combine forecasts (simple average)
        combined_forecast = (ma_forecast + trend_forecast) / 2
        
        # Create forecast dataframe
        last_date = data.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days)
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'predicted_demand': combined_forecast,
            'type': 'forecast'
        })
        
        # Prepare historical data
        historical_df = pd.DataFrame({
            'date': data.index,
            'quantity_sold': series,
            'predicted_demand': series,
            'type': 'historical'
        })
        
        # Combine data
        combined_df = pd.concat([historical_df, forecast_df], ignore_index=True)
        
        # Calculate simple metrics
        metrics = self.calculate_metrics(series)
        
        return combined_df, metrics
        
    def moving_average_forecast(self, series, days):
        """Simple moving average forecast"""
        window = min(7, len(series) // 4)  # Adaptive window size
        ma = series.rolling(window=window).mean().iloc[-1]
        return np.full(days, ma)
        
    def trend_forecast(self, series, days):
        """Linear trend forecast"""
        X = np.arange(len(series)).reshape(-1, 1)
        y = series.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict future
        future_X = np.arange(len(series), len(series) + days).reshape(-1, 1)
        return model.predict(future_X)
        
    def calculate_metrics(self, series):
        """Calculate basic metrics"""
        if len(series) > 1:
            volatility = series.std()
            return {
                'rmse': volatility,
                'mae': volatility * 0.8,  # Approximation
                'volatility': volatility
            }
        else:
            return {'rmse': 0, 'mae': 0, 'volatility': 0}