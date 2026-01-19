import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime


ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
FILE_KAMAR = "data_kamar.csv"
FILE_PENGHUNI = "data_penghuni.csv"

def inisialisasi_csv():
    if not os.path.exists(FILE_KAMAR):
        with open(FILE_KAMAR, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nomor_kamar", "harga", "status"])
            for i in range(1, 31):
                writer.writerow([f"{i:02d}", "1000000", "Tersedia"])

    if not os.path.exists(FILE_PENGHUNI):
        with open(FILE_PENGHUNI, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["nomor_kamar", "nama", "no_hp", "tgl_masuk", "bulan", "total", "status_bayar"])

inisialisasi_csv()

class AppKos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Kos v2.6")
        self.root.geometry("1200x850")
        self.root.configure(bg="#f0f2f5")
        
        
        self.center_window(1200, 850)
        
        
        self.main_container = tk.Frame(self.root, bg="#f0f2f5")
        self.main_container.pack(fill="both", expand=True)
        
        
        self.show_login_page()

    def center_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def show_login_page(self):
        
        for widget in self.main_container.winfo_children():
            widget.destroy()

        
        login_frame = tk.Frame(self.main_container, bg="white", padx=40, pady=40, highlightbackground="#ced4da", highlightthickness=1)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        tk.Label(login_frame, text="🏨", font=("Arial", 50), bg="white").pack(pady=10)
        tk.Label(login_frame, text="ADMIN LOGIN", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=10)

        tk.Label(login_frame, text="Username", bg="white", font=("Segoe UI", 10)).pack(anchor="w", pady=(20,0))
        self.e_user = tk.Entry(login_frame, font=("Segoe UI", 12), bg="#f8f9fa")
        self.e_user.pack(fill="x", pady=5, ipady=5)
        self.e_user.insert(0, "admin")

        tk.Label(login_frame, text="Password", bg="white", font=("Segoe UI", 10)).pack(anchor="w", pady=(10,0))
        self.e_pass = tk.Entry(login_frame, font=("Segoe UI", 12), show="●", bg="#f8f9fa")
        self.e_pass.pack(fill="x", pady=5, ipady=5)
        self.e_pass.insert(0, "admin123")

        btn_login = tk.Button(login_frame, text="MASUK KE SISTEM", bg="#2980b9", fg="white", 
                              font=("Segoe UI", 12, "bold"), command=self.cek_login, cursor="hand2")
        btn_login.pack(fill="x", pady=30, ipady=10)

    def cek_login(self):
        if self.e_user.get() == ADMIN_USER and self.e_pass.get() == ADMIN_PASS:
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Username atau Password Salah!")

    def show_dashboard(self):
        
        for widget in self.main_container.winfo_children():
            widget.destroy()

        
        header = tk.Frame(self.main_container, bg="#2c3e50", height=70)
        header.pack(fill="x")
        tk.Label(header, text="🏨 DASHBOARD MANAJEMEN KOS", bg="#2c3e50", fg="white", 
                 font=("Segoe UI", 18, "bold")).pack(pady=20)

       
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#2980b9", foreground="white", font=("Segoe UI", 10, "bold"))
        
        self.tabs = ttk.Notebook(self.main_container)
        self.tab_daftar = tk.Frame(self.tabs, bg="#f0f2f5")
        self.tab_checkout = tk.Frame(self.tabs, bg="#f0f2f5")
        
        self.tabs.add(self.tab_daftar, text="  📝 PENDAFTARAN BARU  ")
        self.tabs.add(self.tab_checkout, text="  🚪 PEMBAYARAN & CHECKOUT  ")
        self.tabs.pack(fill="both", expand=True, padx=10, pady=5)

        self.room_labels = {}
        self.build_pendaftaran_ui()
        self.build_checkout_ui()
        self.build_status_map()
        self.refresh_all()

    def build_pendaftaran_ui(self):
        main_frame = tk.Frame(self.tab_daftar, bg="#f0f2f5")
        main_frame.pack(expand=True, fill="both")
        
        card = tk.LabelFrame(main_frame, text=" FORMULIR REGISTRASI ", 
                             font=("Segoe UI", 14, "bold"), 
                             bg="white", padx=40, pady=30, relief="flat", 
                             highlightthickness=1, highlightbackground="#ced4da")
        card.place(relx=0.5, rely=0.45, anchor="center") 

        lbl_font = ("Segoe UI", 11, "bold")
        entry_font = ("Segoe UI", 12)
        entry_width = 40 

        tk.Label(card, text="Pilih Kamar (Nomor - Harga)", bg="white", font=lbl_font).grid(row=0, column=0, sticky="w", pady=(5, 2))
        self.cb_kamar = ttk.Combobox(card, state="readonly", width=38, font=entry_font)
        self.cb_kamar.grid(row=1, column=0, pady=(0, 15), ipady=5) 
        self.cb_kamar.bind("<<ComboboxSelected>>", self.hitung_total_daftar)

        tk.Label(card, text="Nama Penghuni Full", bg="white", font=lbl_font).grid(row=2, column=0, sticky="w", pady=(5, 2))
        self.e_nama = tk.Entry(card, width=entry_width, font=entry_font, bg="#f8f9fa")
        self.e_nama.grid(row=3, column=0, pady=(0, 15), ipady=5)

        tk.Label(card, text="Nomor WhatsApp (Aktif)", bg="white", font=lbl_font).grid(row=4, column=0, sticky="w", pady=(5, 2))
        self.e_hp = tk.Entry(card, width=entry_width, font=entry_font, bg="#f8f9fa")
        self.e_hp.grid(row=5, column=0, pady=(0, 15), ipady=5)

        tk.Label(card, text="Durasi Sewa (Bulan)", bg="white", font=lbl_font).grid(row=6, column=0, sticky="w", pady=(5, 2))
        self.e_bulan = tk.Entry(card, width=entry_width, font=entry_font, bg="#f8f9fa")
        self.e_bulan.grid(row=7, column=0, pady=(0, 15), ipady=5)
        self.e_bulan.bind("<KeyRelease>", self.hitung_total_daftar)

        self.lbl_total_view = tk.Label(card, text="Total Tagihan: Rp 0", bg="white", 
                                      fg="#27ae60", font=("Segoe UI", 16, "bold"))
        self.lbl_total_view.grid(row=8, column=0, pady=20)

        tk.Button(card, text="SIMPAN DATA PENDAFTARAN", bg="#27ae60", fg="white", 
                  font=("Segoe UI", 12, "bold"), cursor="hand2",
                  command=self.simpan_data, width=35, height=2).grid(row=9, column=0, pady=5)

    def build_checkout_ui(self):
        table_frame = tk.Frame(self.tab_checkout, bg="white", padx=15, pady=15)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("kamar", "nama", "no_hp", "tgl", "bln", "total", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        heads = ["No. Kamar", "Nama", "No. HP", "Tgl Masuk", "Bulan", "Total Biaya", "Status Bayar"]
        for col, h in zip(columns, heads):
            self.tree.heading(col, text=h)
            self.tree.column(col, anchor="center", width=110)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.pilih_penghuni_checkout)

        self.action_panel = tk.LabelFrame(self.tab_checkout, text=" Area Pelunasan & Check Out ", 
                                         font=("Segoe UI", 10, "bold"), bg="#d6eaf8", padx=20, pady=20)
        self.action_panel.pack(fill="x", padx=20, pady=10)

        self.lbl_info_co = tk.Label(self.action_panel, text="Pilih penghuni di tabel untuk memulai...", bg="#d6eaf8", font=("Segoe UI", 11, "italic"))
        self.lbl_info_co.pack(side="top", anchor="w")

        pay_control = tk.Frame(self.action_panel, bg="#d6eaf8")
        pay_control.pack(fill="x", pady=15)

        tk.Label(pay_control, text="Nominal Bayar (Rp):", bg="#d6eaf8", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.e_bayar_input = tk.Entry(pay_control, font=("Segoe UI", 12), width=20)
        self.e_bayar_input.pack(side="left", padx=15)
        
        tk.Button(pay_control, text="💵 PROSES BAYAR LUNAS", bg="#2980b9", fg="white", 
                  font=("Segoe UI", 10, "bold"), command=self.proses_bayar, padx=15).pack(side="left", padx=5)
        
        self.btn_co = tk.Button(pay_control, text="🚪 CHECK OUT SEKARANG", bg="#e67e22", fg="white", 
                                font=("Segoe UI", 10, "bold"), state="disabled", command=self.proses_checkout, padx=15)
        self.btn_co.pack(side="left", padx=5)

    def build_status_map(self):
        map_frame = tk.LabelFrame(self.main_container, text=" Peta Hunian Kamar (Live) ", bg="white", padx=10, pady=10)
        map_frame.pack(fill="x", padx=20, pady=10)
        grid_frame = tk.Frame(map_frame, bg="white")
        grid_frame.pack()
        for i in range(1, 31):
            num = f"{i:02d}"
            lbl = tk.Label(grid_frame, text=num, width=5, height=2, relief="flat", font=("Segoe UI", 9, "bold"))
            row, col = (i-1) // 15, (i-1) % 15
            lbl.grid(row=row, column=col, padx=3, pady=3)
            self.room_labels[num] = lbl

    def refresh_all(self):
        tersedia_display = []
        self.h_map = {}
        with open(FILE_KAMAR, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                num, harga, stat = r["nomor_kamar"], r["harga"], r["status"]
                self.h_map[num] = int(harga)
                self.room_labels[num].config(bg="#2ecc71" if stat == "Tersedia" else "#e74c3c", fg="white")
                if stat == "Tersedia": tersedia_display.append(f"{num} - Rp {int(harga):,}")
        self.cb_kamar['values'] = tersedia_display
        
        self.tree.delete(*self.tree.get_children())
        with open(FILE_PENGHUNI, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                self.tree.insert("", "end", values=(r["nomor_kamar"], r["nama"], r["no_hp"], r["tgl_masuk"], r["bulan"], r["total"], r["status_bayar"]))

    def hitung_total_daftar(self, event=None):
        
        try:
            selection = self.cb_kamar.get()
            nomor_saja = selection.split(" - ")[0]
            harga_kamar = self.h_map[nomor_saja]
            durasi = int(self.e_bulan.get())
            total = harga_kamar * durasi
            self.lbl_total_view.config(text=f"Total Tagihan: Rp {total:,}")
        except: self.lbl_total_view.config(text="Total Tagihan: Rp 0")

    def simpan_data(self):

        selection = self.cb_kamar.get()
        nm, hp, bln = self.e_nama.get(), self.e_hp.get(), self.e_bulan.get()
        if not selection or not nm or not bln:
            messagebox.showwarning("Gagal", "Lengkapi semua data!")
            return
        kmr = selection.split(" - ")[0]
        total = self.h_map[kmr] * int(bln)
        tgl = datetime.now().strftime("%Y-%m-%d")
        with open(FILE_PENGHUNI, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([kmr, nm, hp, tgl, bln, total, "Belum Lunas"])
        self.update_csv_kamar(kmr, "Terisi")
        self.refresh_all()
        self.e_nama.delete(0, tk.END); self.e_hp.delete(0, tk.END); self.e_bulan.delete(0, tk.END); self.cb_kamar.set('')
        messagebox.showinfo("Sukses", f"Data penghuni kamar {kmr} disimpan.")

    def pilih_penghuni_checkout(self, event):
        sel = self.tree.selection()
        if not sel: return
        val = self.tree.item(sel)["values"]
        self.sel_kamar = str(val[0]).zfill(2)
        self.sel_tagihan = int(val[5])
        self.sel_status = val[6]
        self.lbl_info_co.config(text=f"📌 Kamar: {self.sel_kamar} | Nama: {val[1]} | Tagihan: Rp {self.sel_tagihan:,}", font=("Segoe UI", 11, "bold"), fg="#1b4f72")
        self.btn_co.config(state="normal" if self.sel_status == "Lunas" else "disabled")

    def proses_bayar(self):
        try:
            if not hasattr(self, 'sel_kamar'): return
            inp = int(self.e_bayar_input.get())
            if inp >= self.sel_tagihan:
                rows = []
                with open(FILE_PENGHUNI, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f); header = next(reader); rows.append(header)
                    for r in reader:
                        if r[0] == self.sel_kamar: r[6] = "Lunas"
                        rows.append(r)
                with open(FILE_PENGHUNI, "w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(rows)
                self.refresh_all()
                self.btn_co.config(state="normal")
                messagebox.showinfo("Pembayaran", "Status berhasil diubah menjadi Lunas!")
            else: messagebox.showerror("Gagal", "Uang kurang.")
        except: messagebox.showerror("Error", "Input angka.")

    def proses_checkout(self):
        if messagebox.askyesno("Konfirmasi", f"Proses Check Out kamar {self.sel_kamar}?"):
            rows = []
            with open(FILE_PENGHUNI, newline="", encoding="utf-8") as f:
                reader = csv.reader(f); header = next(reader); rows.append(header)
                for r in reader:
                    if r[0] != self.sel_kamar: rows.append(r)
            with open(FILE_PENGHUNI, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
            self.update_csv_kamar(self.sel_kamar, "Tersedia")
            self.refresh_all()
            self.lbl_info_co.config(text="Pilih penghuni di tabel untuk memulai...", font=("Segoe UI", 11, "italic"), fg="black")
            self.e_bayar_input.delete(0, tk.END)
            self.btn_co.config(state="disabled")

    def update_csv_kamar(self, num, stat):
        rows = []
        with open(FILE_KAMAR, newline="", encoding="utf-8") as f:
            reader = csv.reader(f); header = next(reader); rows.append(header)
            for r in reader:
                if r[0] == num: r[2] = stat
                rows.append(r)
        with open(FILE_KAMAR, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)

if __name__ == "__main__":
    root = tk.Tk()
    AppKos(root)
    root.mainloop()