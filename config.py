"""
Configuration File
Edit these settings to customize your Inventory Management System
"""

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",  # Change this to your MySQL password
    "database": "inventory_db"
}

# Application Settings
APP_CONFIG = {
    "title": "Inventory Management System",
    "width": 1200,
    "height": 700,
    "min_width": 1000,
    "min_height": 600,
    "theme": "clam"  # ttk theme: clam, alt, default, classic
}

# UI Colors
COLORS = {
    "primary": "#2196F3",      # Blue
    "secondary": "#FFC107",    # Amber
    "success": "#4CAF50",      # Green
    "danger": "#F44336",       # Red
    "warning": "#FF9800",      # Orange
    "info": "#00BCD4",         # Cyan
    "background": "#f5f5f5",   # Light gray
    "card_bg": "#ffffff",      # White
    "sidebar_bg": "#2c3e50",   # Dark blue-gray
    "sidebar_btn": "#34495e",  # Slightly lighter
}

# Default Values
DEFAULTS = {
    "min_stock_level": 10,
    "currency": "$",
    "date_format": "%Y-%m-%d %H:%M",
    "items_per_page": 50
}

# User Settings
USER_SETTINGS = {
    "default_user": "Admin",
    "allow_negative_stock": False,  # Set to True to allow stock to go negative
    "show_low_stock_warning": True,
}
