
import tkinter as tk
from tkinter import ttk, messagebox
import redis
import string
import random
import webbrowser
import os
from datetime import datetime

class URLShortener:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Encurtador de URLs")
        self.window.geometry("600x500")
        
        # Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis_client = redis.from_url(redis_url)
        
        # Local storage for test shortener
        self.local_urls = {}
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill='both')
        
        # Redis Tab
        self.redis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.redis_tab, text='Redis Shortener')
        self.setup_redis_tab()
        
        # Local Tab
        self.local_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.local_tab, text='Local Shortener')
        self.setup_local_tab()
    
    def setup_redis_tab(self):
        # URL Input
        self.url_frame = ttk.LabelFrame(self.redis_tab, text="URL Original", padding=10)
        self.url_frame.pack(fill='x', padx=10, pady=5)
        
        self.url_entry = ttk.Entry(self.url_frame, width=50)
        self.url_entry.pack(fill='x', expand=True)
        
        # Expiration time
        self.exp_frame = ttk.LabelFrame(self.redis_tab, text="Tempo de Expiração (horas)", padding=10)
        self.exp_frame.pack(fill='x', padx=10, pady=5)
        
        self.exp_entry = ttk.Entry(self.exp_frame, width=10)
        self.exp_entry.pack(side='left')
        self.exp_entry.insert(0, "24")
        
        # Shorten button
        self.shorten_btn = ttk.Button(self.redis_tab, text="Encurtar URL", command=self.shorten_url_redis)
        self.shorten_btn.pack(pady=10)
        
        # Results
        self.result_frame = ttk.LabelFrame(self.redis_tab, text="URL Encurtada", padding=10)
        self.result_frame.pack(fill='x', padx=10, pady=5)
        
        self.short_url_var = tk.StringVar()
        self.short_url_label = ttk.Entry(self.result_frame, textvariable=self.short_url_var, state='readonly', width=50)
        self.short_url_label.pack(fill='x', expand=True)
        
        # Stats button
        self.stats_btn = ttk.Button(self.redis_tab, text="Ver Estatísticas", command=self.show_stats_redis)
        self.stats_btn.pack(pady=5)
        
        # Stats display
        self.stats_text = tk.Text(self.redis_tab, height=5, width=50)
        self.stats_text.pack(pady=10, padx=10)
    
    def setup_local_tab(self):
        # URL Input
        self.local_url_frame = ttk.LabelFrame(self.local_tab, text="URL Original (Local)", padding=10)
        self.local_url_frame.pack(fill='x', padx=10, pady=5)
        
        self.local_url_entry = ttk.Entry(self.local_url_frame, width=50)
        self.local_url_entry.pack(fill='x', expand=True)
        
        # Shorten button
        self.local_shorten_btn = ttk.Button(self.local_tab, text="Encurtar URL (Local)", command=self.shorten_url_local)
        self.local_shorten_btn.pack(pady=10)
        
        # Results
        self.local_result_frame = ttk.LabelFrame(self.local_tab, text="URL Encurtada (Local)", padding=10)
        self.local_result_frame.pack(fill='x', padx=10, pady=5)
        
        self.local_short_url_var = tk.StringVar()
        self.local_short_url_label = ttk.Entry(self.local_result_frame, textvariable=self.local_short_url_var, state='readonly', width=50)
        self.local_short_url_label.pack(fill='x', expand=True)
        
        # Local URLs list
        self.local_urls_frame = ttk.LabelFrame(self.local_tab, text="URLs Encurtadas", padding=10)
        self.local_urls_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.local_urls_text = tk.Text(self.local_urls_frame, height=8, width=50)
        self.local_urls_text.pack(pady=10, padx=10)
    
    def generate_short_code(self, length=6):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def shorten_url_redis(self):
        original_url = self.url_entry.get()
        if not original_url:
            messagebox.showerror("Erro", "Por favor, insira uma URL")
            return
            
        code = self.generate_short_code()
        expiration_hours = int(self.exp_entry.get() or 24)
        
        try:
            # Store URL mapping
            self.redis_client.setex(f"url:{code}", expiration_hours * 3600, original_url)
            
            # Initialize access counter
            self.redis_client.set(f"stats:{code}", 0)
            
            short_url = f"http://0.0.0.0:5000/{code}"
            self.short_url_var.set(short_url)
            
            # Add to sorted set of most accessed URLs
            self.redis_client.zadd("popular_urls", {code: 0})
        except redis.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar ao Redis")
    
    def shorten_url_local(self):
        original_url = self.local_url_entry.get()
        if not original_url:
            messagebox.showerror("Erro", "Por favor, insira uma URL")
            return
            
        code = self.generate_short_code()
        self.local_urls[code] = {
            'url': original_url,
            'created_at': datetime.now(),
            'visits': 0
        }
        
        short_url = f"http://0.0.0.0:5000/local/{code}"
        self.local_short_url_var.set(short_url)
        
        # Update URLs list
        self.update_local_urls_list()
    
    def show_stats_redis(self):
        code = self.short_url_var.get().split('/')[-1]
        if not code:
            messagebox.showerror("Erro", "Nenhuma URL encurtada disponível")
            return
            
        try:
            original_url = self.redis_client.get(f"url:{code}")
            if not original_url:
                messagebox.showerror("Erro", "URL não encontrada ou expirada")
                return
                
            access_count = self.redis_client.get(f"stats:{code}") or 0
            ttl = self.redis_client.ttl(f"url:{code}")
            
            stats = f"URL Original: {original_url.decode()}\n"
            stats += f"Acessos: {access_count.decode() if isinstance(access_count, bytes) else access_count}\n"
            stats += f"Tempo restante: {ttl//3600} horas, {(ttl%3600)//60} minutos"
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, stats)
        except redis.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Não foi possível conectar ao Redis")
    
    def update_local_urls_list(self):
        self.local_urls_text.delete(1.0, tk.END)
        for code, data in self.local_urls.items():
            self.local_urls_text.insert(tk.END, 
                f"Código: {code}\n"
                f"URL: {data['url']}\n"
                f"Visitas: {data['visits']}\n"
                f"Criado em: {data['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{'-'*50}\n")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = URLShortener()
    app.run()
