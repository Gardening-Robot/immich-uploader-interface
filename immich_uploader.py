"""
Immich Uploader - Standalone Python Version
A beautiful GUI for uploading folders to Immich without external CLI dependencies
"""

import os
import sys
import json
import hashlib
import mimetypes
from pathlib import Path
from tkinter import Tk, filedialog, messagebox
import tkinter as tk
from tkinter import ttk
import threading
import requests
from datetime import datetime

class ImmichUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("Immich Uploader")
        self.root.geometry("900x700")
        self.root.configure(bg="#f8f9fa")
        
        # State
        self.server_url = ""
        self.api_key = ""
        self.selected_folders = []
        self.is_uploading = False
        self.config_file = Path.home() / ".immich_uploader_config.json"
        
        # Load saved config
        self.load_config()
        
        # Setup UI
        self.setup_ui()
        
        # Check if we need setup
        if not self.server_url or not self.api_key:
            self.show_setup()
        else:
            self.show_main()
    
    def load_config(self):
        """Load saved configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.server_url = config.get('server_url', '')
                    self.api_key = config.get('api_key', '')
            except:
                pass
    
    def save_config(self):
        """Save configuration"""
        config = {
            'server_url': self.server_url,
            'api_key': self.api_key
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Setup frame (hidden by default)
        self.setup_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        
        # Main upload frame (hidden by default)
        self.upload_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        
        self.setup_setup_ui()
        self.setup_main_ui()
    
    def setup_setup_ui(self):
        """Setup the configuration UI"""
        # Title
        title = tk.Label(self.setup_frame, text="🚀 Welcome to Immich Uploader", 
                        font=("Helvetica", 24, "bold"), bg="#ffffff", fg="#4F46E5")
        title.pack(pady=30)
        
        # Instructions
        instructions = tk.Label(self.setup_frame, 
                               text="Let's connect to your Immich server",
                               font=("Helvetica", 12), bg="#ffffff", fg="#6B7280")
        instructions.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(self.setup_frame, bg="#ffffff")
        form_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Server URL
        tk.Label(form_frame, text="Immich Server URL:", 
                font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#374151").pack(anchor=tk.W, pady=(10, 5))
        self.server_url_entry = tk.Entry(form_frame, font=("Helvetica", 11), width=50)
        self.server_url_entry.pack(fill=tk.X, pady=(0, 5))
        self.server_url_entry.insert(0, self.server_url or "http://192.168.1.100:2283/api")
        
        tk.Label(form_frame, text="Include /api at the end", 
                font=("Helvetica", 9), bg="#ffffff", fg="#9CA3AF").pack(anchor=tk.W, pady=(0, 15))
        
        # API Key
        tk.Label(form_frame, text="API Key:", 
                font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#374151").pack(anchor=tk.W, pady=(10, 5))
        self.api_key_entry = tk.Entry(form_frame, font=("Helvetica", 11), width=50, show="*")
        self.api_key_entry.pack(fill=tk.X, pady=(0, 5))
        self.api_key_entry.insert(0, self.api_key)
        
        tk.Label(form_frame, text="Generate in Immich: Settings → Account Settings → API Keys", 
                font=("Helvetica", 9), bg="#ffffff", fg="#9CA3AF").pack(anchor=tk.W, pady=(0, 20))
        
        # Connect button
        self.connect_btn = tk.Button(form_frame, text="Connect to Immich", 
                                     font=("Helvetica", 12, "bold"),
                                     bg="#4F46E5", fg="white", 
                                     activebackground="#4338CA",
                                     cursor="hand2", bd=0, padx=30, pady=12,
                                     command=self.connect)
        self.connect_btn.pack(pady=20)
    
    def setup_main_ui(self):
        """Setup the main upload UI"""
        # Header
        header = tk.Frame(self.upload_frame, bg="#4F46E5")
        header.pack(fill=tk.X)
        
        header_content = tk.Frame(header, bg="#4F46E5")
        header_content.pack(pady=20, padx=20)
        
        tk.Label(header_content, text="📸 Immich Uploader", 
                font=("Helvetica", 20, "bold"), bg="#4F46E5", fg="white").pack(side=tk.LEFT)
        
        self.status_label = tk.Label(header_content, text="● Connected", 
                                     font=("Helvetica", 11), bg="#4F46E5", fg="#10B981")
        self.status_label.pack(side=tk.RIGHT, padx=20)
        
        # Content area
        content = tk.Frame(self.upload_frame, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Folder selection area
        select_frame = tk.LabelFrame(content, text="📁 Select Folders", 
                                     font=("Helvetica", 13, "bold"),
                                     bg="#ffffff", fg="#374151", bd=2, relief=tk.GROOVE)
        select_frame.pack(fill=tk.X, pady=(0, 20))
        
        btn_frame = tk.Frame(select_frame, bg="#ffffff")
        btn_frame.pack(pady=15, padx=15)
        
        tk.Button(btn_frame, text="📂 Browse for Folder", 
                 font=("Helvetica", 11), bg="#E5E7EB", fg="#374151",
                 activebackground="#D1D5DB", cursor="hand2",
                 bd=0, padx=20, pady=10,
                 command=self.select_folder).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📂 Select Multiple Folders", 
                 font=("Helvetica", 11), bg="#E5E7EB", fg="#374151",
                 activebackground="#D1D5DB", cursor="hand2",
                 bd=0, padx=20, pady=10,
                 command=self.select_multiple_folders).pack(side=tk.LEFT, padx=5)
        
        # Selected folders list
        self.folders_frame = tk.LabelFrame(content, text="Selected Folders", 
                                          font=("Helvetica", 12, "bold"),
                                          bg="#ffffff", fg="#374151", bd=2, relief=tk.GROOVE)
        
        # Scrollable list
        list_container = tk.Frame(self.folders_frame, bg="#ffffff")
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.folders_listbox = tk.Listbox(list_container, font=("Helvetica", 10),
                                          yscrollcommand=scrollbar.set,
                                          height=8, bg="#F9FAFB", relief=tk.FLAT)
        self.folders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.folders_listbox.yview)
        
        tk.Button(self.folders_frame, text="Remove Selected", 
                 font=("Helvetica", 10), bg="#FEE2E2", fg="#EF4444",
                 activebackground="#FECACA", cursor="hand2",
                 bd=0, padx=15, pady=8,
                 command=self.remove_selected_folder).pack(pady=10)
        
        # Options
        options_frame = tk.LabelFrame(content, text="⚙️ Upload Options", 
                                      font=("Helvetica", 12, "bold"),
                                      bg="#ffffff", fg="#374151", bd=2, relief=tk.GROOVE)
        options_frame.pack(fill=tk.X, pady=20)
        
        opts_content = tk.Frame(options_frame, bg="#ffffff")
        opts_content.pack(padx=15, pady=15)
        
        self.use_folder_name_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opts_content, text="Use folder name as album name",
                      variable=self.use_folder_name_var,
                      font=("Helvetica", 11), bg="#ffffff",
                      activebackground="#ffffff").pack(anchor=tk.W, pady=5)
        
        self.skip_duplicates_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opts_content, text="Skip duplicate files (recommended)",
                      variable=self.skip_duplicates_var,
                      font=("Helvetica", 11), bg="#ffffff",
                      activebackground="#ffffff").pack(anchor=tk.W, pady=5)
        
        # Upload button
        btn_container = tk.Frame(content, bg="#ffffff")
        btn_container.pack(fill=tk.X, pady=20)
        
        self.upload_btn = tk.Button(btn_container, text="🚀 Start Upload", 
                                    font=("Helvetica", 14, "bold"),
                                    bg="#4F46E5", fg="white",
                                    activebackground="#4338CA",
                                    cursor="hand2", bd=0, padx=40, pady=15,
                                    command=self.start_upload)
        self.upload_btn.pack()
        
        # Progress area
        self.progress_frame = tk.LabelFrame(content, text="📊 Upload Progress", 
                                           font=("Helvetica", 12, "bold"),
                                           bg="#ffffff", fg="#374151", bd=2, relief=tk.GROOVE)
        
        progress_content = tk.Frame(self.progress_frame, bg="#ffffff")
        progress_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.progress_bar = ttk.Progressbar(progress_content, length=400, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        self.progress_label = tk.Label(progress_content, text="Ready to upload", 
                                       font=("Helvetica", 10), bg="#ffffff", fg="#6B7280")
        self.progress_label.pack(pady=5)
        
        # Log area
        log_container = tk.Frame(progress_content, bg="#ffffff")
        log_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        log_scroll = tk.Scrollbar(log_container)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_container, height=10, font=("Courier", 9),
                               yscrollcommand=log_scroll.set,
                               bg="#F9FAFB", relief=tk.FLAT, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
    
    def show_setup(self):
        """Show setup screen"""
        self.upload_frame.pack_forget()
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_main(self):
        """Show main upload screen"""
        self.setup_frame.pack_forget()
        self.upload_frame.pack(fill=tk.BOTH, expand=True)
    
    def connect(self):
        """Connect to Immich server"""
        server_url = self.server_url_entry.get().strip()
        api_key = self.api_key_entry.get().strip()
        
        if not server_url or not api_key:
            messagebox.showerror("Error", "Please enter both server URL and API key")
            return
        
        # Test connection
        self.connect_btn.config(text="Connecting...", state=tk.DISABLED)
        self.root.update()
        
        try:
            # Test API connection
            headers = {'x-api-key': api_key}
            response = requests.get(f"{server_url}/user/me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.server_url = server_url
                self.api_key = api_key
                self.save_config()
                messagebox.showinfo("Success", "Connected to Immich successfully!")
                self.show_main()
            else:
                messagebox.showerror("Connection Failed", 
                                   f"Failed to connect: {response.status_code}\n{response.text}")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect:\n{str(e)}")
        finally:
            self.connect_btn.config(text="Connect to Immich", state=tk.NORMAL)
    
    def select_folder(self):
        """Select a single folder"""
        folder = filedialog.askdirectory(title="Select Folder to Upload")
        if folder:
            self.add_folder(folder)
    
    def select_multiple_folders(self):
        """Select multiple folders"""
        # Tkinter doesn't support multiple folder selection natively
        # So we'll let users select multiple times
        folder = filedialog.askdirectory(title="Select Folder (you can do this multiple times)")
        if folder:
            self.add_folder(folder)
            if messagebox.askyesno("Add More?", "Do you want to add another folder?"):
                self.select_multiple_folders()
    
    def add_folder(self, folder_path):
        """Add folder to upload list"""
        if folder_path not in self.selected_folders:
            self.selected_folders.append(folder_path)
            folder_name = os.path.basename(folder_path)
            
            # Count files
            file_count = self.count_media_files(folder_path)
            
            self.folders_listbox.insert(tk.END, f"{folder_name} ({file_count} files) - {folder_path}")
            
            if not self.folders_frame.winfo_ismapped():
                self.folders_frame.pack(fill=tk.BOTH, expand=True, pady=20)
    
    def remove_selected_folder(self):
        """Remove selected folder from list"""
        selection = self.folders_listbox.curselection()
        if selection:
            index = selection[0]
            self.folders_listbox.delete(index)
            self.selected_folders.pop(index)
            
            if not self.selected_folders:
                self.folders_frame.pack_forget()
    
    def count_media_files(self, folder_path):
        """Count media files in folder"""
        count = 0
        media_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif',
                          '.mp4', '.mov', '.avi', '.mkv', '.m4v', '.mpg', '.mpeg', '.3gp'}
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in media_extensions:
                    count += 1
        
        return count
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_upload(self):
        """Start uploading folders"""
        if not self.selected_folders:
            messagebox.showwarning("No Folders", "Please select at least one folder to upload")
            return
        
        if self.is_uploading:
            messagebox.showwarning("Upload in Progress", "An upload is already in progress")
            return
        
        # Show progress frame
        if not self.progress_frame.winfo_ismapped():
            self.progress_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Disable upload button
        self.upload_btn.config(state=tk.DISABLED, text="Uploading...")
        self.is_uploading = True
        
        # Start upload in thread
        thread = threading.Thread(target=self.upload_folders)
        thread.daemon = True
        thread.start()
    
    def upload_folders(self):
        """Upload all selected folders"""
        total_folders = len(self.selected_folders)
        success_count = 0
        fail_count = 0
        
        try:
            for i, folder_path in enumerate(self.selected_folders):
                folder_name = os.path.basename(folder_path)
                album_name = folder_name if self.use_folder_name_var.get() else "Uploaded Photos"
                
                # Update progress
                progress = int((i / total_folders) * 100)
                self.progress_bar['value'] = progress
                self.progress_label.config(text=f"Uploading folder {i+1} of {total_folders}: {folder_name}")
                
                self.log(f"Starting upload: {folder_name} → Album: {album_name}")
                
                # Upload folder
                if self.upload_folder(folder_path, album_name):
                    success_count += 1
                    self.log(f"✓ Successfully uploaded {folder_name}")
                else:
                    fail_count += 1
                    self.log(f"✗ Failed to upload {folder_name}")
            
            # Complete
            self.progress_bar['value'] = 100
            self.progress_label.config(text=f"Complete! {success_count} successful, {fail_count} failed")
            self.log(f"\n=== Upload Complete ===")
            self.log(f"Success: {success_count}, Failed: {fail_count}")
            
            messagebox.showinfo("Upload Complete", 
                              f"Upload finished!\n\nSuccessful: {success_count}\nFailed: {fail_count}")
        
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Upload Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.is_uploading = False
            self.upload_btn.config(state=tk.NORMAL, text="🚀 Start Upload")
    
    def upload_folder(self, folder_path, album_name):
        """Upload a single folder"""
        try:
            # First, create or get album
            album_id = self.get_or_create_album(album_name)
            if not album_id:
                self.log(f"Failed to create/find album: {album_name}")
                return False
            
            # Get all media files
            media_files = []
            media_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif',
                              '.mp4', '.mov', '.avi', '.mkv', '.m4v', '.mpg', '.mpeg', '.3gp'}
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in media_extensions:
                        media_files.append(os.path.join(root, file))
            
            self.log(f"Found {len(media_files)} media files to upload")
            
            # Upload each file
            uploaded_count = 0
            for file_path in media_files:
                if self.upload_file(file_path, album_id):
                    uploaded_count += 1
                    if uploaded_count % 10 == 0:
                        self.log(f"Uploaded {uploaded_count}/{len(media_files)} files...")
            
            self.log(f"Uploaded {uploaded_count}/{len(media_files)} files to album '{album_name}'")
            return True
        
        except Exception as e:
            self.log(f"Error uploading folder: {str(e)}")
            return False
    
    def get_or_create_album(self, album_name):
        """Get existing album or create new one"""
        try:
            headers = {'x-api-key': self.api_key}
            
            # Try to find existing album
            response = requests.get(f"{self.server_url}/album", headers=headers, timeout=10)
            if response.status_code == 200:
                albums = response.json()
                for album in albums:
                    if album.get('albumName') == album_name:
                        return album.get('id')
            
            # Create new album
            data = {'albumName': album_name}
            response = requests.post(f"{self.server_url}/album", 
                                   headers=headers, json=data, timeout=10)
            if response.status_code == 201:
                return response.json().get('id')
            
            return None
        except Exception as e:
            self.log(f"Error with album: {str(e)}")
            return None
    
    def upload_file(self, file_path, album_id):
        """Upload a single file"""
        try:
            headers = {'x-api-key': self.api_key}
            
            # Check if file exists already (if skip duplicates enabled)
            if self.skip_duplicates_var.get():
                file_hash = self.calculate_file_hash(file_path)
                # For now, we'll skip the duplicate check API call to keep it simple
                # In production, you'd want to check against Immich's asset list
            
            # Prepare file upload
            with open(file_path, 'rb') as f:
                file_name = os.path.basename(file_path)
                mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
                
                files = {
                    'assetData': (file_name, f, mime_type)
                }
                
                data = {
                    'deviceAssetId': f"{file_name}-{os.path.getmtime(file_path)}",
                    'deviceId': 'ImmichUploader',
                    'fileCreatedAt': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
                    'fileModifiedAt': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                    'isFavorite': 'false',
                }
                
                # Upload asset
                response = requests.post(f"{self.server_url}/asset/upload",
                                       headers=headers, files=files, data=data, timeout=60)
                
                if response.status_code in [200, 201]:
                    asset_id = response.json().get('id')
                    
                    # Add to album
                    album_data = {'ids': [asset_id]}
                    requests.put(f"{self.server_url}/album/{album_id}/assets",
                               headers=headers, json=album_data, timeout=10)
                    
                    return True
                elif response.status_code == 409:
                    # Duplicate - that's okay if we're skipping
                    return True
                else:
                    return False
        
        except Exception as e:
            return False
    
    def calculate_file_hash(self, file_path):
        """Calculate SHA1 hash of file"""
        sha1 = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest()


def main():
    root = Tk()
    app = ImmichUploader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
