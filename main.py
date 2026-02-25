#!/usr/bin/env python3
"""
Inventory Management System
A desktop application built with Python 3, Tkinter, and MySQL
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import sys
from database import Database
from gui import InventoryGUI


def check_dependencies():
    """Check if required packages are installed"""
    try:
        import mysql.connector
        return True
    except ImportError:
        response = messagebox.askyesno(
            "Missing Dependencies",
            "MySQL Connector is not installed.\n\nWould you like to install it now?"
        )
        if response:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
                messagebox.showinfo("Success", "MySQL Connector installed successfully!\nPlease restart the application.")
                return False
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to install dependencies:\n{str(e)}")
                return False
        return False


def main():
    """Main entry point"""
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create main window
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("1200x700")
    root.minsize(1000, 600)
    
    # Set application icon (optional)
    try:
        root.iconbitmap("assets/icon.ico")
    except:
        pass
    
    # Initialize database connection
    db = None
    try:
        db = Database()
        if not db.connect():
            messagebox.showerror(
                "Database Error",
                "Failed to connect to MySQL database.\n\n"
                "Please ensure:\n"
                "1. MySQL server is running\n"
                "2. Database 'inventory_db' exists\n"
                "3. Credentials are correct (root/password)\n\n"
                "Run 'python setup_database.py' to setup the database."
            )
            return
    except Exception as e:
        messagebox.showerror("Error", f"Database connection failed:\n{str(e)}")
        return
    
    # Initialize GUI
    app = InventoryGUI(root, db)
    
    # Handle window close
    def on_closing():
        if db:
            db.disconnect()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start application
    root.mainloop()


if __name__ == "__main__":
    main()
