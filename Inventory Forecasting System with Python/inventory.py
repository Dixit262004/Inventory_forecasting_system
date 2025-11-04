import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class InventoryManager:
    def __init__(self):
        self.products_file = 'data/inventory_data.csv'
        self.sales_file = 'data/sales_data.csv'
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs('data', exist_ok=True)
        
    def load_sample_data(self):
        """Generate sample data for demonstration"""
        # Sample products
        products_data = {
            'product_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
            'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
            'current_stock': [45, 120, 85, 30, 95],
            'reorder_level': [50, 100, 80, 25, 90],
            'cost_price': [800.0, 25.0, 45.0, 300.0, 75.0]
        }
        
        products_df = pd.DataFrame(products_data)
        products_df.to_csv(self.products_file, index=False)
        
        # Generate sample sales data (2 years of daily data)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)
        
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        sales_data = []
        
        # Different sales patterns for each product
        patterns = {
            'P001': {'base': 2, 'trend': 0.001, 'seasonality': 0.5},
            'P002': {'base': 5, 'trend': 0.002, 'seasonality': 0.3},
            'P003': {'base': 3, 'trend': 0.0015, 'seasonality': 0.4},
            'P004': {'base': 1, 'trend': 0.0005, 'seasonality': 0.6},
            'P005': {'base': 4, 'trend': 0.002, 'seasonality': 0.2}
        }
        
        for date in dates:
            for product_id, pattern in patterns.items():
                # Generate realistic sales with trend, seasonality, and noise
                trend = pattern['trend'] * (date - start_date).days
                seasonality = pattern['seasonality'] * np.sin(2 * np.pi * date.dayofyear / 365)
                noise = np.random.normal(0, 0.2)
                
                sales = max(0, int(
                    pattern['base'] + trend + seasonality + noise + np.random.poisson(1)
                ))
                
                sales_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'product_id': product_id,
                    'quantity_sold': sales
                })
        
        sales_df = pd.DataFrame(sales_data)
        sales_df.to_csv(self.sales_file, index=False)
        
    def get_all_products(self):
        """Get all products from CSV"""
        try:
            df = pd.read_csv(self.products_file)
            return df.to_dict('records')
        except FileNotFoundError:
            return []
            
    def add_product(self, product_data):
        """Add new product"""
        df = pd.read_csv(self.products_file)
        
        # Check if product already exists
        if product_data['product_id'] in df['product_id'].values:
            raise ValueError("Product ID already exists!")
            
        new_df = pd.DataFrame([product_data])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(self.products_file, index=False)
        
    def update_product(self, product_id, product_data):
        """Update existing product"""
        df = pd.read_csv(self.products_file)
        
        if product_id not in df['product_id'].values:
            raise ValueError("Product not found!")
            
        # Update the product
        mask = df['product_id'] == product_id
        for key, value in product_data.items():
            df.loc[mask, key] = value
            
        df.to_csv(self.products_file, index=False)
        
    def delete_product(self, product_id):
        """Delete product"""
        df = pd.read_csv(self.products_file)
        
        if product_id not in df['product_id'].values:
            raise ValueError("Product not found!")
            
        df = df[df['product_id'] != product_id]
        df.to_csv(self.products_file, index=False)
        
    def get_sales_data(self, product_id):
        """Get sales data for a specific product"""
        try:
            sales_df = pd.read_csv(self.sales_file)
            product_sales = sales_df[sales_df['product_id'] == product_id].copy()
            product_sales['date'] = pd.to_datetime(product_sales['date'])
            product_sales = product_sales.sort_values('date')
            return product_sales
        except FileNotFoundError:
            raise ValueError("Sales data not found!")
            
    def generate_reorder_suggestions(self):
        """Generate reorder suggestions based on current stock and trends"""
        products = self.get_all_products()
        suggestions = []
        
        for product in products:
            current_stock = product['current_stock']
            reorder_level = product['reorder_level']
            
            if current_stock <= reorder_level:
                # Calculate suggested order quantity
                deficit = reorder_level - current_stock
                safety_stock = reorder_level * 0.5  # 50% safety stock
                suggested_order = int(deficit + safety_stock)
                
                # Determine urgency
                stock_ratio = current_stock / reorder_level
                if stock_ratio <= 0.5:
                    urgency = "HIGH"
                elif stock_ratio <= 0.8:
                    urgency = "MEDIUM"
                else:
                    urgency = "LOW"
                    
                suggestions.append({
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'current_stock': current_stock,
                    'reorder_level': reorder_level,
                    'suggested_order': suggested_order,
                    'urgency': urgency
                })
                
        return suggestions
