import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from inventory import InventoryManager
from forecasting import DemandForecaster
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
warnings.filterwarnings('ignore')

class InventoryForecastingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Industry-Grade Inventory & Demand Forecasting")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.inventory_manager = InventoryManager()
        self.forecaster = DemandForecaster()
        
        self.setup_ui()
        self.load_sample_data()
        
    def setup_ui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Inventory Management Tab
        self.inventory_frame = ttk.Frame(notebook)
        notebook.add(self.inventory_frame, text="Inventory Management")
        self.setup_inventory_tab()
        
        # Forecasting Tab
        self.forecast_frame = ttk.Frame(notebook)
        notebook.add(self.forecast_frame, text="Demand Forecasting")
        self.setup_forecast_tab()
        
        # Reorder Suggestions Tab
        self.reorder_frame = ttk.Frame(notebook)
        notebook.add(self.reorder_frame, text="Reorder Suggestions")
        self.setup_reorder_tab()
        
    def setup_inventory_tab(self):
        # Left frame for CRUD operations
        left_frame = ttk.LabelFrame(self.inventory_frame, text="Product Management", padding=10)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Product form
        ttk.Label(left_frame, text="Product ID:").grid(row=0, column=0, sticky='w', pady=2)
        self.product_id = ttk.Entry(left_frame)
        self.product_id.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(left_frame, text="Product Name:").grid(row=1, column=0, sticky='w', pady=2)
        self.product_name = ttk.Entry(left_frame)
        self.product_name.grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(left_frame, text="Current Stock:").grid(row=2, column=0, sticky='w', pady=2)
        self.current_stock = ttk.Entry(left_frame)
        self.current_stock.grid(row=2, column=1, pady=2, padx=5)
        
        ttk.Label(left_frame, text="Reorder Level:").grid(row=3, column=0, sticky='w', pady=2)
        self.reorder_level = ttk.Entry(left_frame)
        self.reorder_level.grid(row=3, column=1, pady=2, padx=5)
        
        ttk.Label(left_frame, text="Cost Price:").grid(row=4, column=0, sticky='w', pady=2)
        self.cost_price = ttk.Entry(left_frame)
        self.cost_price.grid(row=4, column=1, pady=2, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Product", command=self.add_product).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Update Product", command=self.update_product).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Delete Product", command=self.delete_product).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side='left', padx=2)
        
        # Right frame for product list
        right_frame = ttk.LabelFrame(self.inventory_frame, text="Product List", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Treeview for products
        columns = ('ID', 'Name', 'Stock', 'Reorder Level', 'Cost Price')
        self.product_tree = ttk.Treeview(right_frame, columns=columns, show='headings')
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=100)
        
        self.product_tree.pack(fill='both', expand=True)
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Load data button
        ttk.Button(right_frame, text="Refresh Data", command=self.load_inventory_data).pack(pady=5)
        
    def setup_forecast_tab(self):
        # Left frame for controls
        left_frame = ttk.LabelFrame(self.forecast_frame, text="Forecasting Controls", padding=10)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Product selection
        ttk.Label(left_frame, text="Select Product:").pack(anchor='w', pady=2)
        self.forecast_product = ttk.Combobox(left_frame, state='readonly')
        self.forecast_product.pack(fill='x', pady=5)
        
        # Model selection
        ttk.Label(left_frame, text="Select Model:").pack(anchor='w', pady=2)
        self.model_var = tk.StringVar(value="ARIMA")
        ttk.Radiobutton(left_frame, text="ARIMA", variable=self.model_var, value="ARIMA").pack(anchor='w')
        ttk.Radiobutton(left_frame, text="LSTM", variable=self.model_var, value="LSTM").pack(anchor='w')
        
        # Forecast button
        ttk.Button(left_frame, text="Generate Forecast", command=self.generate_forecast).pack(pady=10)
        
        # Right frame for results
        self.forecast_result_frame = ttk.LabelFrame(self.forecast_frame, text="Forecast Results", padding=10)
        self.forecast_result_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
    def setup_reorder_tab(self):
        main_frame = ttk.Frame(self.reorder_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for reorder suggestions
        columns = ('Product ID', 'Product Name', 'Current Stock', 'Reorder Level', 'Suggested Order', 'Urgency')
        self.reorder_tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        for col in columns:
            self.reorder_tree.heading(col, text=col)
            self.reorder_tree.column(col, width=120)
        
        self.reorder_tree.pack(fill='both', expand=True)
        
        # Generate suggestions button
        ttk.Button(main_frame, text="Generate Reorder Suggestions", 
                  command=self.generate_reorder_suggestions).pack(pady=10)
        
    def load_sample_data(self):
        """Load sample data for demonstration"""
        try:
            self.inventory_manager.load_sample_data()
            self.load_inventory_data()
            self.update_product_combobox()
            messagebox.showinfo("Success", "Sample data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sample data: {str(e)}")
            
    def load_inventory_data(self):
        """Load inventory data into treeview"""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        products = self.inventory_manager.get_all_products()
        for product in products:
            self.product_tree.insert('', 'end', values=(
                product['product_id'],
                product['product_name'],
                product['current_stock'],
                product['reorder_level'],
                f"${product['cost_price']:.2f}"
            ))
            
    def update_product_combobox(self):
        """Update product combobox in forecast tab"""
        products = self.inventory_manager.get_all_products()
        product_names = [f"{p['product_id']} - {p['product_name']}" for p in products]
        self.forecast_product['values'] = product_names
        if product_names:
            self.forecast_product.set(product_names[0])
            
    def on_product_select(self, event):
        """Load selected product data into form"""
        selection = self.product_tree.selection()
        if selection:
            item = self.product_tree.item(selection[0])
            values = item['values']
            
            self.product_id.delete(0, tk.END)
            self.product_id.insert(0, values[0])
            
            self.product_name.delete(0, tk.END)
            self.product_name.insert(0, values[1])
            
            self.current_stock.delete(0, tk.END)
            self.current_stock.insert(0, values[2])
            
            self.reorder_level.delete(0, tk.END)
            self.reorder_level.insert(0, values[3])
            
            # Remove $ symbol if present
            cost_price = str(values[4]).replace('$', '')
            self.cost_price.delete(0, tk.END)
            self.cost_price.insert(0, cost_price)
            
    def add_product(self):
        """Add new product"""
        try:
            product_data = {
                'product_id': self.product_id.get(),
                'product_name': self.product_name.get(),
                'current_stock': int(self.current_stock.get()),
                'reorder_level': int(self.reorder_level.get()),
                'cost_price': float(self.cost_price.get())
            }
            
            self.inventory_manager.add_product(product_data)
            self.load_inventory_data()
            self.update_product_combobox()
            self.clear_form()
            messagebox.showinfo("Success", "Product added successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please check your input values!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
            
    def update_product(self):
        """Update existing product"""
        try:
            product_data = {
                'product_id': self.product_id.get(),
                'product_name': self.product_name.get(),
                'current_stock': int(self.current_stock.get()),
                'reorder_level': int(self.reorder_level.get()),
                'cost_price': float(self.cost_price.get())
            }
            
            self.inventory_manager.update_product(self.product_id.get(), product_data)
            self.load_inventory_data()
            self.update_product_combobox()
            messagebox.showinfo("Success", "Product updated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {str(e)}")
            
    def delete_product(self):
        """Delete selected product"""
        product_id = self.product_id.get()
        if not product_id:
            messagebox.showwarning("Warning", "Please select a product to delete!")
            return
            
        if messagebox.askyesno("Confirm", f"Delete product {product_id}?"):
            try:
                self.inventory_manager.delete_product(product_id)
                self.load_inventory_data()
                self.update_product_combobox()
                self.clear_form()
                messagebox.showinfo("Success", "Product deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")
                
    def clear_form(self):
        """Clear the product form"""
        self.product_id.delete(0, tk.END)
        self.product_name.delete(0, tk.END)
        self.current_stock.delete(0, tk.END)
        self.reorder_level.delete(0, tk.END)
        self.cost_price.delete(0, tk.END)
        
    def generate_forecast(self):
        """Generate demand forecast for selected product"""
        product_selection = self.forecast_product.get()
        if not product_selection:
            messagebox.showwarning("Warning", "Please select a product!")
            return
            
        product_id = product_selection.split(' - ')[0]
        model_type = self.model_var.get()
        
        try:
            # Clear previous results
            for widget in self.forecast_result_frame.winfo_children():
                widget.destroy()
                
            # Generate forecast
            forecast_df, metrics = self.forecaster.generate_forecast(
                product_id, model_type, days=30
            )
            
            # Display metrics
            metrics_frame = ttk.Frame(self.forecast_result_frame)
            metrics_frame.pack(fill='x', pady=5)
            
            ttk.Label(metrics_frame, text=f"Model: {model_type}", font=('Arial', 10, 'bold')).pack()
            ttk.Label(metrics_frame, text=f"RMSE: {metrics.get('rmse', 'N/A'):.2f}").pack()
            ttk.Label(metrics_frame, text=f"MAE: {metrics.get('mae', 'N/A'):.2f}").pack()
            
            # Create plot
            fig = self.forecaster.plot_forecast(forecast_df, product_id)
            
            # Embed plot in tkinter
            canvas = FigureCanvasTkAgg(fig, self.forecast_result_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            # Display forecast table
            tree_frame = ttk.Frame(self.forecast_result_frame)
            tree_frame.pack(fill='both', expand=True)
            
            columns = ['Date', 'Predicted Demand']
            forecast_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
            
            for col in columns:
                forecast_tree.heading(col, text=col)
                forecast_tree.column(col, width=150)
                
            for _, row in forecast_df.tail(30).iterrows():
                forecast_tree.insert('', 'end', values=(
                    row['date'].strftime('%Y-%m-%d'),
                    f"{row['predicted_demand']:.1f}"
                ))
                
            forecast_tree.pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Forecast generation failed: {str(e)}")
            
    def generate_reorder_suggestions(self):
        """Generate reorder suggestions based on current stock and forecast"""
        try:
            # Clear previous suggestions
            for item in self.reorder_tree.get_children():
                self.reorder_tree.delete(item)
                
            suggestions = self.inventory_manager.generate_reorder_suggestions()
            
            for suggestion in suggestions:
                self.reorder_tree.insert('', 'end', values=(
                    suggestion['product_id'],
                    suggestion['product_name'],
                    suggestion['current_stock'],
                    suggestion['reorder_level'],
                    suggestion['suggested_order'],
                    suggestion['urgency']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate suggestions: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryForecastingApp(root)
    root.mainloop()
