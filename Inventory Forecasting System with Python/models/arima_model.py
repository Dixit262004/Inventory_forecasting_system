import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

class ARIMAForecaster:
    def __init__(self):
        self.model = None
        
    def forecast(self, data, days=30):
        """Generate forecast using ARIMA model"""
        # Use last 90 days for training to capture recent trends
        train_data = data['quantity_sold'].tail(90)
        
        # Fit ARIMA model
        try:
            # Try seasonal ARIMA first
            model = SARIMAX(train_data, 
                          order=(1, 1, 1), 
                          seasonal_order=(1, 1, 1, 7),
                          enforce_stationarity=False,
                          enforce_invertibility=False)
            fitted_model = model.fit(disp=False)
        except:
            # Fall back to regular ARIMA
            model = ARIMA(train_data, order=(1, 1, 1))
            fitted_model = model.fit()
        
        # Generate forecast
        forecast = fitted_model.get_forecast(steps=days)
        forecast_values = forecast.predicted_mean
        confidence_int = forecast.conf_int()
        
        # Create forecast dataframe
        last_date = data.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days)
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'predicted_demand': forecast_values,
            'confidence_lower': confidence_int.iloc[:, 0],
            'confidence_upper': confidence_int.iloc[:, 1],
            'type': 'forecast'
        })
        
        # Prepare historical data for combined dataframe
        historical_df = pd.DataFrame({
            'date': data.index,
            'quantity_sold': data['quantity_sold'],
            'predicted_demand': data['quantity_sold'],
            'type': 'historical'
        })
        
        # Combine historical and forecast data
        combined_df = pd.concat([historical_df, forecast_df], ignore_index=True)
        
        # Calculate metrics on recent data
        test_size = min(14, len(train_data) // 3)
        if test_size > 0:
            train = train_data[:-test_size]
            test = train_data[-test_size:]
            
            # Fit model on training portion
            try:
                model_temp = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
                fitted_temp = model_temp.fit(disp=False)
            except:
                model_temp = ARIMA(train, order=(1, 1, 1))
                fitted_temp = model_temp.fit()
                
            test_forecast = fitted_temp.get_forecast(steps=test_size)
            test_pred = test_forecast.predicted_mean
            
            metrics = {
                'rmse': np.sqrt(mean_squared_error(test, test_pred)),
                'mae': mean_absolute_error(test, test_pred)
            }
        else:
            metrics = {'rmse': 0, 'mae': 0}
            
        return combined_df, metrics
