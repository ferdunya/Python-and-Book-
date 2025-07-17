import tkinter as tk
from tkinter import messagebox
from database_services import SessionLocal, Admin, kayit_ol, giris_yap, kitap_oku, kitaplarimi_gor, admin_girisi, tum_kullanicilari_goruntule, kullanici_sil


class App:
    def __init__(self, root):
        self.root = root
        self.session = SessionLocal()
        self.kullanici = None

        # Admin hesabını oluşturmak için eğer admin hesabı yoksa
        if not self.session.query(Admin).first():
            admin = Admin(kullanici_adi="admin", sifre="admin")
            self.session.add(admin)
            self.session.commit()

        self.root.title("Kitaplar Uygulamasi")
        self.create_main_menu()

#ana menu olusturma    
    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, text="Kayit Olun", command=self.kayit_ol_sayfasi).pack(pady=10)
        tk.Button(self.root, text="Giris Yapin", command=self.giris_yap_sayfasi).pack(pady=10)
        tk.Button(self.root, text="Admin Girisi Yap", command=self.admin_girisi_sayfasi).pack(pady=10)
        tk.Button(self.root, text="Cikis Yap", command=self.root.quit).pack(pady=10)
        
#kayıt olma fonksiyonu
    def kayit_ol_sayfasi(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Kullanici adi").pack()
        kullanici_adi_entry = tk.Entry(self.root)
        kullanici_adi_entry.pack()

        tk.Label(self.root, text="Sifre").pack()
        sifre_entry = tk.Entry(self.root, show="*")
        sifre_entry.pack()

        def kayit():
            kullanici_adi = kullanici_adi_entry.get()
            sifre = sifre_entry.get()
            mesaj = kayit_ol(self.session, kullanici_adi, sifre)
            messagebox.showinfo("Bilgi", mesaj)
            if mesaj == "Kayit basarili!":
                self.create_main_menu()

        tk.Button(self.root, text="Kayit Ol", command=kayit).pack(pady=10)
        tk.Button(self.root, text="Geri", command=self.create_main_menu).pack(pady=10)

    #giris fonksiyonu
    def giris_yap_sayfasi(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
#tkinter arayüz kodları
        tk.Label(self.root, text="Kullanici adi").pack()
        kullanici_adi_entry = tk.Entry(self.root)
        kullanici_adi_entry.pack()

        tk.Label(self.root, text="Sifre").pack()
        sifre_entry = tk.Entry(self.root, show="*")
        sifre_entry.pack()

#giris fonksiyonu ve arayüzü        
        def giris():
            kullanici_adi = kullanici_adi_entry.get()
            sifre = sifre_entry.get()
            mesaj, kullanici = giris_yap(self.session, kullanici_adi, sifre)
            messagebox.showinfo("Bilgi", mesaj)
            if kullanici:
                self.kullanici = kullanici
                self.kullanici_menu()

        tk.Button(self.root, text="Giris Yap", command=giris).pack(pady=10)
        tk.Button(self.root, text="Geri", command=self.create_main_menu).pack(pady=10)

#user menusu fonksiyonu    
    def kullanici_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, text="Kitap Oku", command=self.kitap_oku_sayfasi).pack(pady=10)
        tk.Button(self.root, text="Kitaplarimi Gor", command=self.kitaplarimi_gor_sayfasi).pack(pady=10)
        tk.Button(self.root, text="Cikis", command=self.create_main_menu).pack(pady=10)

#database kitap ekleme
    def kitap_oku_sayfasi(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Okudugunuz kitabin adi").pack()
        kitap_basligi_entry = tk.Entry(self.root)
        kitap_basligi_entry.pack()

        def kitap_oku_fonksiyonu():
            kitap_basligi = kitap_basligi_entry.get()
            mesaj = kitap_oku(self.session, self.kullanici, kitap_basligi)
            messagebox.showinfo("Bilgi", mesaj)

        tk.Button(self.root, text="Kitap Oku", command=kitap_oku_fonksiyonu).pack(pady=10)
        tk.Button(self.root, text="Geri", command=self.kullanici_menu).pack(pady=10)
        
#database deki kitapları görme
    def kitaplarimi_gor_sayfasi(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        kitaplar = kitaplarimi_gor(self.session, self.kullanici)
        if isinstance(kitaplar, list):
            for kitap in kitaplar:
                tk.Label(self.root, text=kitap).pack()
        else:
            tk.Label(self.root, text=kitaplar).pack()

        tk.Button(self.root, text="Geri", command=self.kullanici_menu).pack(pady=10)


    def admin_girisi_sayfasi(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Admin Kullanici adi").pack()
        admin_kullanici_adi_entry = tk.Entry(self.root)
        admin_kullanici_adi_entry.pack()

        tk.Label(self.root, text="Admin Sifre").pack()
        admin_sifre_entry = tk.Entry(self.root, show="*")
        admin_sifre_entry.pack()
        
#admin giris fonksiyonu 
        def admin_giris():
            admin_kullanici_adi = admin_kullanici_adi_entry.get()
            admin_sifre = admin_sifre_entry.get()
            mesaj, basarili = admin_girisi(self.session, admin_kullanici_adi, admin_sifre)
            messagebox.showinfo("Bilgi", mesaj)
            if basarili:
                self.admin_menu()

        tk.Button(self.root, text="Admin Girisi Yap", command=admin_giris).pack(pady=10)
        tk.Button(self.root, text="Geri", command=self.create_main_menu).pack(pady=10)

#admin hakimiyet menusu fonksiyonu
    def admin_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, text="Tum Kullanicilari Goruntule", command=self.tum_kullanicilari_goruntule_sayfasi).pack(pady=10)
        tk.Button(self.root, text="Kullanici Sil", command=self.kullanici_sil_sayfasi).pack(pady=10)
        tk.Button(self.root, text="Cikis", command=self.create_main_menu).pack(pady=10)

    def tum_kullanicilari_goruntule_sayfasi(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        kullanicilar = tum_kullanicilari_goruntule(self.session)
        for kullanici_adi, kitaplar in kullanicilar:
            tk.Label(self.root, text=f"Kullanici: {kullanici_adi}").pack()
            for kitap in kitaplar:
                tk.Label(self.root, text=f" - {kitap}").pack()

        tk.Button(self.root, text="Geri", command=self.admin_menu).pack(pady=10)

#admin veri tabanından kullanıcı silme fonksiyonu
    def kullanici_sil_sayfasi(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Silinecek Kullanici adi").pack()
        kullanici_adi_entry = tk.Entry(self.root)
        kullanici_adi_entry.pack()

        def sil():
            kullanici_adi = kullanici_adi_entry.get()
            mesaj = kullanici_sil(self.session, kullanici_adi)
            messagebox.showinfo("Bilgi", mesaj)

        tk.Button(self.root, text="Kullanici Sil", command=sil).pack(pady=10)
        tk.Button(self.root, text="Geri", command=self.admin_menu).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
