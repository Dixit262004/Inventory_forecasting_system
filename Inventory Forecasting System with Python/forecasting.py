# forecasting.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models.arima_model import ARIMAForecaster
from models.simple_models import SimpleForecaster
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

class DemandForecaster:
    def __init__(self):
        self.arima_forecaster = ARIMAForecaster()
        self.simple_forecaster = SimpleForecaster()
        
    def generate_forecast(self, product_id, model_type, days=30):
        """Generate demand forecast using specified model"""
        from inventory import InventoryManager
        
        # Get sales data
        inventory_manager = InventoryManager()
        sales_data = inventory_manager.get_sales_data(product_id)
        
        if len(sales_data) < 30:
            raise ValueError("Insufficient data for forecasting")
            
        # Prepare data
        daily_sales = sales_data.groupby('date')['quantity_sold'].sum().reset_index()
        daily_sales = daily_sales.set_index('date')
        
        # Generate forecast based on model type
        if model_type == "ARIMA":
            forecast_df, metrics = self.arima_forecaster.forecast(daily_sales, days)
        else:  # Simple models as fallback
            forecast_df, metrics = self.simple_forecaster.forecast(daily_sales, days)
            
        return forecast_df, metrics
        
    def plot_forecast(self, forecast_df, product_id):
        """Create forecast visualization"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot historical data
        historical = forecast_df[forecast_df['type'] == 'historical']
        ax.plot(historical['date'], historical['quantity_sold'], 
                label='Historical Sales', color='blue', linewidth=2)
        
        # Plot forecast
        forecast = forecast_df[forecast_df['type'] == 'forecast']
        ax.plot(forecast['date'], forecast['predicted_demand'], 
                label='Forecast', color='red', linewidth=2, linestyle='--')
        
        # Plot confidence interval if available
        if 'confidence_lower' in forecast.columns and 'confidence_upper' in forecast.columns:
            ax.fill_between(forecast['date'], 
                           forecast['confidence_lower'], 
                           forecast['confidence_upper'], 
                           color='red', alpha=0.2, label='Confidence Interval')
        
        ax.set_title(f'Demand Forecast for Product {product_id}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Quantity Sold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig