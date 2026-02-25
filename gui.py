"""
GUI Module
Tkinter interface for the Inventory Management System
I used ai to modify the interface more 
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime


class InventoryGUI:
    """Main GUI class for Inventory Management System"""
    
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.current_view = "dashboard"
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_menu()
        self.create_sidebar()
        self.create_main_content()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        self.primary_color = "#2196F3"
        self.secondary_color = "#FFC107"
        self.success_color = "#4CAF50"
        self.danger_color = "#F44336"
        self.warning_color = "#FF9800"
        self.bg_color = "#f5f5f5"
        self.card_bg = "#ffffff"
        
        # Configure styles
        style.configure("Title.TLabel", font=("Helvetica", 24, "bold"))
        style.configure("Subtitle.TLabel", font=("Helvetica", 14))
        style.configure("Card.TFrame", background=self.card_bg)
        style.configure("Sidebar.TFrame", background="#2c3e50")
        style.configure("Sidebar.TButton", 
                       font=("Helvetica", 11),
                       background="#34495e",
                       foreground="white",
                       padding=10)
        style.map("Sidebar.TButton",
                 background=[('active', '#2196F3')])
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Dashboard", command=self.show_dashboard)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Products menu
        products_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Products", menu=products_menu)
        products_menu.add_command(label="View All Products", command=self.show_products)
        products_menu.add_command(label="Add Product", command=self.show_add_product)
        products_menu.add_command(label="Low Stock Alert", command=self.show_low_stock)
        
        # Categories menu
        categories_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Categories", menu=categories_menu)
        categories_menu.add_command(label="Manage Categories", command=self.show_categories)
        
        # Transactions menu
        transactions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Transactions", menu=transactions_menu)
        transactions_menu.add_command(label="View Transactions", command=self.show_transactions)
        transactions_menu.add_command(label="Stock In", command=lambda: self.show_stock_movement("IN"))
        transactions_menu.add_command(label="Stock Out", command=lambda: self.show_stock_movement("OUT"))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        title_label = tk.Label(
            self.sidebar, 
            text="INVENTORY\nSYSTEM", 
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=20
        )
        title_label.pack(fill=tk.X)
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Products", self.show_products),
            ("Categories", self.show_categories),
            ("Transactions", self.show_transactions),
            ("Low Stock", self.show_low_stock),
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(
                self.sidebar,
                text=text,
                font=("Helvetica", 11),
                bg="#34495e",
                fg="white",
                activebackground="#2196F3",
                activeforeground="white",
                bd=0,
                padx=20,
                pady=12,
                cursor="hand2",
                command=command
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
    
    def create_main_content(self):
        """Create main content area"""
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def clear_main_content(self):
        """Clear main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    # ==================== DASHBOARD VIEW ====================
    
    def show_dashboard(self):
        """Display dashboard with statistics"""
        self.clear_main_content()
        self.current_view = "dashboard"
        
        # Header
        header = ttk.Label(self.main_frame, text="Dashboard", style="Title.TLabel")
        header.pack(anchor=tk.W, pady=(0, 20))
        
        # Stats cards frame
        cards_frame = ttk.Frame(self.main_frame)
        cards_frame.pack(fill=tk.X, pady=10)
        
        # Get stats
        stats = self.db.get_dashboard_stats()
        
        # Create stat cards
        stat_cards = [
            ("Total Products", stats.get('total_products', 0), "#2196F3"),
            ("Categories", stats.get('total_categories', 0), "#9C27B0"),
            ("Stock Value", f"${stats.get('stock_value', 0):,.2f}", "#4CAF50"),
            ("Low Stock Items", stats.get('low_stock_count', 0), "#F44336"),
        ]
        
        for title, value, color in stat_cards:
            self.create_stat_card(cards_frame, title, value, color)
        
        # Recent activity section
        activity_frame = ttk.LabelFrame(self.main_frame, text="Recent Transactions", padding=15)
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Transactions tree
        columns = ("Date", "Product", "Type", "Quantity", "User")
        tree = ttk.Treeview(activity_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(activity_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load recent transactions
        transactions = self.db.get_transactions(limit=10)
        for trans in transactions:
            tree.insert("", tk.END, values=(
                trans['created_at'].strftime("%Y-%m-%d %H:%M"),
                trans['product_name'],
                trans['transaction_type'],
                trans['quantity'],
                trans['user']
            ))
    
    def create_stat_card(self, parent, title, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg="white", padx=20, pady=20, relief=tk.RAISED, bd=1)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Color indicator
        indicator = tk.Frame(card, bg=color, width=5)
        indicator.pack(side=tk.LEFT, fill=tk.Y)
        
        # Content
        content = tk.Frame(card, bg="white")
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)
        
        title_label = tk.Label(content, text=title, font=("Helvetica", 12), bg="white", fg="#666")
        title_label.pack(anchor=tk.W)
        
        value_label = tk.Label(content, text=str(value), font=("Helvetica", 28, "bold"), bg="white", fg=color)
        value_label.pack(anchor=tk.W, pady=(5, 0))
    
    # ==================== PRODUCTS VIEW ====================
    
    def show_products(self):
        """Display all products"""
        self.clear_main_content()
        self.current_view = "products"
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header = ttk.Label(header_frame, text="Products", style="Title.TLabel")
        header.pack(side=tk.LEFT)
        
        # Search frame
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side=tk.RIGHT)
        
        search_entry = ttk.Entry(search_frame, width=30, font=("Helvetica", 11))
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(
            search_frame, 
            text="Search", 
            bg="#2196F3", 
            fg="white",
            padx=15,
            pady=5,
            bd=0,
            cursor="hand2",
            command=lambda: self.search_products(search_entry.get())
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Add Product button
        add_btn = tk.Button(
            header_frame,
            text="+ Add Product",
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=5,
            bd=0,
            cursor="hand2",
            command=self.show_add_product
        )
        add_btn.pack(side=tk.RIGHT, padx=20)
        
        # Products table
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "SKU", "Name", "Category", "Quantity", "Price", "Status")
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        column_widths = {"ID": 50, "SKU": 100, "Name": 200, "Category": 120, "Quantity": 80, "Price": 100, "Status": 100}
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.products_tree.xview)
        self.products_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        edit_btn = tk.Button(
            action_frame,
            text="Edit Selected",
            bg="#FFC107",
            fg="black",
            padx=20,
            pady=8,
            bd=0,
            cursor="hand2",
            command=self.edit_selected_product
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="Delete Selected",
            bg="#F44336",
            fg="white",
            padx=20,
            pady=8,
            bd=0,
            cursor="hand2",
            command=self.delete_selected_product
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        stock_btn = tk.Button(
            action_frame,
            text="Stock In/Out",
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=8,
            bd=0,
            cursor="hand2",
            command=self.stock_movement_selected
        )
        stock_btn.pack(side=tk.LEFT, padx=5)
        
        # Load products
        self.load_products()
    
    def load_products(self, search_term=None):
        """Load products into the treeview"""
        # Clear existing
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Get products
        products = self.db.get_all_products(search_term=search_term)
        
        for product in products:
            status = "Low Stock" if product['quantity'] <= product['min_stock_level'] else "In Stock"
            status_tag = "low" if status == "Low Stock" else "ok"
            
            self.products_tree.insert("", tk.END, values=(
                product['id'],
                product['sku'],
                product['name'],
                product['category_name'] or "Uncategorized",
                product['quantity'],
                f"${product['price']:.2f}",
                status
            ), tags=(status_tag,))
        
        # Configure tags
        self.products_tree.tag_configure("low", foreground="#F44336")
        self.products_tree.tag_configure("ok", foreground="#4CAF50")
    
    def search_products(self, search_term):
        """Search products"""
        self.load_products(search_term=search_term)
    
    def show_add_product(self):
        """Show add product dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"500x500+{x}+{y}")
        
        # Form
        ttk.Label(dialog, text="Add New Product", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fields
        fields = [
            ("Name:", "name", True),
            ("SKU:", "sku", True),
            ("Description:", "description", False),
            ("Quantity:", "quantity", True),
            ("Price:", "price", True),
            ("Min Stock Level:", "min_stock", True),
        ]
        
        entries = {}
        for i, (label, field, required) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame, width=35, font=("Helvetica", 11))
            entry.grid(row=i, column=1, sticky=tk.W, pady=5, padx=10)
            entries[field] = entry
        
        # Category dropdown
        ttk.Label(form_frame, text="Category:").grid(row=len(fields), column=0, sticky=tk.W, pady=5)
        categories = self.db.get_all_categories()
        category_names = [c['name'] for c in categories]
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(form_frame, textvariable=category_var, values=category_names, width=33)
        category_dropdown.grid(row=len(fields), column=1, sticky=tk.W, pady=5, padx=10)
        
        # Buttons
        btn_frame = ttk.Frame(dialog, padding=20)
        btn_frame.pack(fill=tk.X)
        
        def save_product():
            # Validate
            name = entries['name'].get().strip()
            sku = entries['sku'].get().strip()
            
            if not name or not sku:
                messagebox.showerror("Error", "Name and SKU are required!")
                return
            
            try:
                quantity = int(entries['quantity'].get() or 0)
                price = float(entries['price'].get() or 0)
                min_stock = int(entries['min_stock'].get() or 10)
            except ValueError:
                messagebox.showerror("Error", "Invalid number format!")
                return
            
            # Get category ID
            category_id = None
            selected_category = category_var.get()
            for cat in categories:
                if cat['name'] == selected_category:
                    category_id = cat['id']
                    break
            
            # Save
            product_id = self.db.add_product(
                name=name,
                sku=sku,
                description=entries['description'].get().strip(),
                category_id=category_id,
                quantity=quantity,
                price=price,
                min_stock=min_stock
            )
            
            if product_id:
                messagebox.showinfo("Success", "Product added successfully!")
                dialog.destroy()
                if self.current_view == "products":
                    self.load_products()
                else:
                    self.show_products()
            else:
                messagebox.showerror("Error", "Failed to add product!")
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(
            btn_frame, 
            text="Save Product", 
            bg="#4CAF50", 
            fg="white",
            padx=20,
            pady=5,
            bd=0,
            cursor="hand2",
            command=save_product
        ).pack(side=tk.RIGHT, padx=5)
    
    def edit_selected_product(self):
        """Edit the selected product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit!")
            return
        
        item = self.products_tree.item(selected[0])
        product_id = item['values'][0]
        
        product = self.db.get_product_by_id(product_id)
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        
        # Edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Product - {product['name']}")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"500x500+{x}+{y}")
        
        ttk.Label(dialog, text="Edit Product", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fields with current values
        fields_data = [
            ("Name:", "name", product['name']),
            ("SKU:", "sku", product['sku']),
            ("Description:", "description", product['description'] or ""),
            ("Quantity:", "quantity", str(product['quantity'])),
            ("Price:", "price", str(product['price'])),
            ("Min Stock Level:", "min_stock", str(product['min_stock_level'])),
        ]
        
        entries = {}
        for i, (label, field, value) in enumerate(fields_data):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame, width=35, font=("Helvetica", 11))
            entry.insert(0, value)
            entry.grid(row=i, column=1, sticky=tk.W, pady=5, padx=10)
            entries[field] = entry
        
        # Category dropdown
        ttk.Label(form_frame, text="Category:").grid(row=len(fields_data), column=0, sticky=tk.W, pady=5)
        categories = self.db.get_all_categories()
        category_names = [c['name'] for c in categories]
        category_var = tk.StringVar(value=product['category_name'] or "")
        category_dropdown = ttk.Combobox(form_frame, textvariable=category_var, values=category_names, width=33)
        category_dropdown.grid(row=len(fields_data), column=1, sticky=tk.W, pady=5, padx=10)
        
        # Buttons
        btn_frame = ttk.Frame(dialog, padding=20)
        btn_frame.pack(fill=tk.X)
        
        def update_product():
            name = entries['name'].get().strip()
            sku = entries['sku'].get().strip()
            
            if not name or not sku:
                messagebox.showerror("Error", "Name and SKU are required!")
                return
            
            try:
                quantity = int(entries['quantity'].get() or 0)
                price = float(entries['price'].get() or 0)
                min_stock = int(entries['min_stock'].get() or 10)
            except ValueError:
                messagebox.showerror("Error", "Invalid number format!")
                return
            
            category_id = None
            selected_category = category_var.get()
            for cat in categories:
                if cat['name'] == selected_category:
                    category_id = cat['id']
                    break
            
            success = self.db.update_product(
                product_id=product_id,
                name=name,
                sku=sku,
                description=entries['description'].get().strip(),
                category_id=category_id,
                quantity=quantity,
                price=price,
                min_stock=min_stock
            )
            
            if success:
                messagebox.showinfo("Success", "Product updated successfully!")
                dialog.destroy()
                self.load_products()
            else:
                messagebox.showerror("Error", "Failed to update product!")
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(
            btn_frame, 
            text="Update Product", 
            bg="#FFC107", 
            fg="black",
            padx=20,
            pady=5,
            bd=0,
            cursor="hand2",
            command=update_product
        ).pack(side=tk.RIGHT, padx=5)
    
    def delete_selected_product(self):
        """Delete the selected product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete!")
            return
        
        item = self.products_tree.item(selected[0])
        product_id = item['values'][0]
        product_name = item['values'][2]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            if self.db.delete_product(product_id):
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_products()
            else:
                messagebox.showerror("Error", "Failed to delete product!")
    
    def stock_movement_selected(self):
        """Handle stock in/out for selected product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product!")
            return
        
        item = self.products_tree.item(selected[0])
        product_id = item['values'][0]
        product_name = item['values'][2]
        
        self.show_stock_movement_dialog(product_id, product_name)
    
    def show_stock_movement(self, movement_type):
        """Show stock movement dialog"""
        self.show_products()
        messagebox.showinfo("Info", "Select a product and click 'Stock In/Out' button")
    
    def show_stock_movement_dialog(self, product_id, product_name):
        """Show dialog for stock in/out"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Stock Movement - {product_name}")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        ttk.Label(dialog, text=f"Stock Movement", font=("Helvetica", 16, "bold")).pack(pady=15)
        ttk.Label(dialog, text=f"Product: {product_name}", font=("Helvetica", 12)).pack(pady=5)
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Movement type
        ttk.Label(form_frame, text="Movement Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        movement_var = tk.StringVar(value="IN")
        ttk.Radiobutton(form_frame, text="Stock In", variable=movement_var, value="IN").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(form_frame, text="Stock Out", variable=movement_var, value="OUT").grid(row=1, column=1, sticky=tk.W)
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=10)
        qty_entry = ttk.Entry(form_frame, width=20, font=("Helvetica", 11))
        qty_entry.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        # Notes
        ttk.Label(form_frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, pady=5)
        notes_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 11))
        notes_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(dialog, padding=20)
        btn_frame.pack(fill=tk.X)
        
        def save_movement():
            try:
                quantity = int(qty_entry.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid quantity!")
                return
            
            movement_type = movement_var.get()
            notes = notes_entry.get().strip()
            
            transaction_id = self.db.add_transaction(
                product_id=product_id,
                transaction_type=movement_type,
                quantity=quantity,
                notes=notes
            )
            
            if transaction_id:
                messagebox.showinfo("Success", f"Stock {movement_type} recorded successfully!")
                dialog.destroy()
                self.load_products()
            else:
                messagebox.showerror("Error", "Failed to record transaction!")
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(
            btn_frame, 
            text="Save", 
            bg="#2196F3", 
            fg="white",
            padx=20,
            pady=5,
            bd=0,
            cursor="hand2",
            command=save_movement
        ).pack(side=tk.RIGHT, padx=5)
    
    # ==================== CATEGORIES VIEW ====================
    
    def show_categories(self):
        """Display categories management"""
        self.clear_main_content()
        self.current_view = "categories"
        
        header = ttk.Label(self.main_frame, text="Categories", style="Title.TLabel")
        header.pack(anchor=tk.W, pady=(0, 20))
        
        # Add category button
        add_btn = tk.Button(
            self.main_frame,
            text="+ Add Category",
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=5,
            bd=0,
            cursor="hand2",
            command=self.show_add_category
        )
        add_btn.pack(anchor=tk.W, pady=10)
        
        # Categories list
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Name", "Description")
        self.categories_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.categories_tree.heading(col, text=col)
            self.categories_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.categories_tree.yview)
        self.categories_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.categories_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        edit_btn = tk.Button(
            action_frame,
            text="Edit Selected",
            bg="#FFC107",
            fg="black",
            padx=20,
            pady=8,
            bd=0,
            cursor="hand2",
            command=self.edit_selected_category
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="Delete Selected",
            bg="#F44336",
            fg="white",
            padx=20,
            pady=8,
            bd=0,
            cursor="hand2",
            command=self.delete_selected_category
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_categories()
    
    def load_categories(self):
        """Load categories into treeview"""
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        categories = self.db.get_all_categories()
        for cat in categories:
            self.categories_tree.insert("", tk.END, values=(
                cat['id'],
                cat['name'],
                cat['description'] or ""
            ))
    
    def show_add_category(self):
        """Show add category dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Category")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Add New Category", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 11))
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=5)
        desc_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 11))
        desc_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        btn_frame = ttk.Frame(dialog, padding=20)
        btn_frame.pack(fill=tk.X)
        
        def save_category():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Category name is required!")
                return
            
            category_id = self.db.add_category(name, desc_entry.get().strip())
            if category_id:
                messagebox.showinfo("Success", "Category added successfully!")
                dialog.destroy()
                self.load_categories()
            else:
                messagebox.showerror("Error", "Failed to add category!")
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(
            btn_frame, 
            text="Save", 
            bg="#4CAF50", 
            fg="white",
            padx=20,
            pady=5,
            bd=0,
            cursor="hand2",
            command=save_category
        ).pack(side=tk.RIGHT, padx=5)
    
    def edit_selected_category(self):
        """Edit selected category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a category to edit!")
            return
        
        item = self.categories_tree.item(selected[0])
        category_id = item['values'][0]
        category_name = item['values'][1]
        category_desc = item['values'][2]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Category - {category_name}")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Edit Category", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 11))
        name_entry.insert(0, category_name)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=5)
        desc_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 11))
        desc_entry.insert(0, category_desc)
        desc_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        btn_frame = ttk.Frame(dialog, padding=20)
        btn_frame.pack(fill=tk.X)
        
        def update_category():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Category name is required!")
                return
            
            if self.db.update_category(category_id, name, desc_entry.get().strip()):
                messagebox.showinfo("Success", "Category updated successfully!")
                dialog.destroy()
                self.load_categories()
            else:
                messagebox.showerror("Error", "Failed to update category!")
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(
            btn_frame, 
            text="Update", 
            bg="#FFC107", 
            fg="black",
            padx=20,
            pady=5,
            bd=0,
            cursor="hand2",
            command=update_category
        ).pack(side=tk.RIGHT, padx=5)
    
    def delete_selected_category(self):
        """Delete selected category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a category to delete!")
            return
        
        item = self.categories_tree.item(selected[0])
        category_id = item['values'][0]
        category_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete category '{category_name}'?"):
            if self.db.delete_category(category_id):
                messagebox.showinfo("Success", "Category deleted successfully!")
                self.load_categories()
            else:
                messagebox.showerror("Error", "Failed to delete category!")
    
    # ==================== TRANSACTIONS VIEW ====================
    
    def show_transactions(self):
        """Display transactions history"""
        self.clear_main_content()
        self.current_view = "transactions"
        
        header = ttk.Label(self.main_frame, text="Transaction History", style="Title.TLabel")
        header.pack(anchor=tk.W, pady=(0, 20))
        
        # Transactions table
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Date", "Product", "SKU", "Type", "Quantity", "Notes", "User")
        self.trans_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.trans_tree.yview)
        self.trans_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.trans_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load transactions
        transactions = self.db.get_transactions(limit=100)
        for trans in transactions:
            self.trans_tree.insert("", tk.END, values=(
                trans['id'],
                trans['created_at'].strftime("%Y-%m-%d %H:%M"),
                trans['product_name'],
                trans['sku'],
                trans['transaction_type'],
                trans['quantity'],
                trans['notes'] or "",
                trans['user']
            ))
    
    # ==================== LOW STOCK VIEW ====================
    
    def show_low_stock(self):
        """Display low stock alerts"""
        self.clear_main_content()
        self.current_view = "low_stock"
        
        header = ttk.Label(self.main_frame, text="Low Stock Alerts", style="Title.TLabel")
        header.pack(anchor=tk.W, pady=(0, 20))
        
        warning_label = tk.Label(
            self.main_frame,
            text="The following products are running low on stock and need to be restocked.",
            font=("Helvetica", 11),
            fg="#F44336"
        )
        warning_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Table
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "SKU", "Name", "Current Stock", "Min Level", "Needed")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load low stock products
        products = self.db.get_low_stock_products()
        for product in products:
            needed = product['min_stock_level'] - product['quantity'] + 10
            tree.insert("", tk.END, values=(
                product['id'],
                product['sku'],
                product['name'],
                product['quantity'],
                product['min_stock_level'],
                needed
            ))
    
    # ==================== ABOUT ====================
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Inventory Management System\n\n"
            "Built with:\n"
            "- Python 3\n"
            "- Tkinter\n"
            "- MySQL\n\n"
            "Version 1.0"
        )
