
Database Module
Handles all MySQL database operations for the Inventory Management System


import mysql.connector
from mysql.connector import Error
from datetime import datetime


class Database:
    """MySQL Database connection and operations class"""
    
    def __init__(self, host="localhost", user="root", password="password", database="inventory_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    # ==================== PRODUCT OPERATIONS ====================
    
    def get_all_products(self, search_term=None, category=None):
        """Get all products with optional filtering"""
        try:
            query = """
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE 1=1
            """
            params = []
            
            if search_term:
                query += " AND (p.name LIKE %s OR p.sku LIKE %s OR p.description LIKE %s)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern])
            
            if category:
                query += " AND p.category_id = %s"
                params.append(category)
            
            query += " ORDER BY p.created_at DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching products: {e}")
            return []
    
    def get_product_by_id(self, product_id):
        """Get a single product by ID"""
        try:
            query = """
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.id = %s
            """
            self.cursor.execute(query, (product_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching product: {e}")
            return None
    
    def add_product(self, name, sku, description, category_id, quantity, price, min_stock=10):
        """Add a new product"""
        try:
            query = """
                INSERT INTO products (name, sku, description, category_id, quantity, price, min_stock_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, sku, description, category_id, quantity, price, min_stock))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error adding product: {e}")
            return None
    
    def update_product(self, product_id, name, sku, description, category_id, quantity, price, min_stock):
        """Update an existing product"""
        try:
            query = """
                UPDATE products 
                SET name = %s, sku = %s, description = %s, category_id = %s, 
                    quantity = %s, price = %s, min_stock_level = %s, updated_at = %s
                WHERE id = %s
            """
            self.cursor.execute(query, (name, sku, description, category_id, quantity, price, min_stock, datetime.now(), product_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating product: {e}")
            return False
    
    def delete_product(self, product_id):
        """Delete a product"""
        try:
            query = "DELETE FROM products WHERE id = %s"
            self.cursor.execute(query, (product_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting product: {e}")
            return False
    
    def update_stock(self, product_id, quantity_change):
        """Update product stock quantity"""
        try:
            query = """
                UPDATE products 
                SET quantity = quantity + %s, updated_at = %s
                WHERE id = %s
            """
            self.cursor.execute(query, (quantity_change, datetime.now(), product_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating stock: {e}")
            return False
    
    def get_low_stock_products(self):
        """Get products with stock below minimum level"""
        try:
            query = """
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.quantity <= p.min_stock_level
                ORDER BY p.quantity ASC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching low stock products: {e}")
            return []
    
  ===== CATEGORY OPERATIONS ===
    
    def get_all_categories(self):
        """Get all categories"""
        try:
            query = "SELECT * FROM categories ORDER BY name"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching categories: {e}")
            return []
    
    def add_category(self, name, description=""):
        """Add a new category"""
        try:
            query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
            self.cursor.execute(query, (name, description))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error adding category: {e}")
            return None
    
    def update_category(self, category_id, name, description):
        """Update a category"""
        try:
            query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
            self.cursor.execute(query, (name, description, category_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating category: {e}")
            return False
    
    def delete_category(self, category_id):
        """Delete a category"""
        try:
            query = "DELETE FROM categories WHERE id = %s"
            self.cursor.execute(query, (category_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting category: {e}")
            return False
    
    # ===== TRANSACTION OPERATIONS ======
    
    def add_transaction(self, product_id, transaction_type, quantity, notes="", user="Admin"):
        """Add a stock transaction (in/out)"""
        try:
            query = """
                INSERT INTO transactions (product_id, transaction_type, quantity, notes, user)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (product_id, transaction_type, quantity, notes, user))
            self.connection.commit()
            
            # Update product quantity
            if transaction_type == "IN":
                self.update_stock(product_id, quantity)
            elif transaction_type == "OUT":
                self.update_stock(product_id, -quantity)
            
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error adding transaction: {e}")
            return None
    
    def get_transactions(self, product_id=None, limit=100):
        """Get transaction history"""
        try:
            query = """
                SELECT t.*, p.name as product_name, p.sku
                FROM transactions t
                JOIN products p ON t.product_id = p.id
            """
            params = []
            
            if product_id:
                query += " WHERE t.product_id = %s"
                params.append(product_id)
            
            query += " ORDER BY t.created_at DESC LIMIT %s"
            params.append(limit)
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    # ====== DASHBOARD STATS =======
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        try:
            stats = {}
            
            # Total products
            self.cursor.execute("SELECT COUNT(*) as count FROM products")
            stats['total_products'] = self.cursor.fetchone()['count']
            
            # Total categories
            self.cursor.execute("SELECT COUNT(*) as count FROM categories")
            stats['total_categories'] = self.cursor.fetchone()['count']
            
            # Total stock value
            self.cursor.execute("""
                SELECT SUM(quantity * price) as total_value 
                FROM products
            """)
            result = self.cursor.fetchone()
            stats['stock_value'] = result['total_value'] or 0
            
            # Low stock count
            self.cursor.execute("""
                SELECT COUNT(*) as count 
                FROM products 
                WHERE quantity <= min_stock_level
            """)
            stats['low_stock_count'] = self.cursor.fetchone()['count']
            
            # Total transactions today
            self.cursor.execute("""
                SELECT COUNT(*) as count 
                FROM transactions 
                WHERE DATE(created_at) = CURDATE()
            """)
            stats['today_transactions'] = self.cursor.fetchone()['count']
            
            return stats
        except Error as e:
            print(f"Error fetching dashboard stats: {e}")
            return {}
