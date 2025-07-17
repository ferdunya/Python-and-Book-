from database_services import Admin, Kullanici

#admin giris fonksiyonu
def admin_girisi(session):
    kullanici_adi = input("Admin kullanici adi: ")
    sifre = input("Admin sifresi: ")

#admin sifre ve kullanıcı adı uyusuyorsa giris yapabilir    
    admin = session.query(Admin).filter(Admin.kullanici_adi == kullanici_adi, Admin.sifre == sifre).first()
    if admin:
        print("Admin girisi basarili!")
        return True
    else:
        print("Admin kullanici adi veya sifre hatali.")
        return False
        
#tüm kullanıcıları görebilme fonksiyonu
def tum_kullanicilari_goruntule(session):
    kullanicilar = session.query(Kullanici).all()
    for kullanici in kullanicilar:
        kitaplar = ', '.join([kitap.baslik for kitap in kullanici.okunan_kitaplar])
        print(f"Kullanici: {kullanici.kullanici_adi}, Okunan kitaplar: {kitaplar}")
        
#tüm kullanıcıları sileilme fonksiyonu
def kullanici_sil(session):
    kullanici_adi = input("Silmek istediginiz kullanicinin adi: ")
    kullanici = session.query(Kullanici).filter(Kullanici.kullanici_adi == kullanici_adi).first()
    if kullanici:
        session.delete(kullanici)
        session.commit()
        print(f"{kullanici_adi} kullanicisi silindi.")
    else:
        print("Kullanici bulunamadi.")
