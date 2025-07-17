from database_services import Kullanici, OkunanKitap, SessionLocal

#veritabanina kullanici kaydetme fonksiyonu
def kayit_ol(session):
    kullanici_adi = input("Kullanici adi: ")
    if session.query(Kullanici).filter(Kullanici.kullanici_adi == kullanici_adi).first():
        print("Bu kullanici adi zaten alinmis.")
        return

    sifre = input("Sifre: ")
    yeni_kullanici = Kullanici(kullanici_adi=kullanici_adi, sifre=sifre)
    session.add(yeni_kullanici)
    session.commit()
    print("Kayit basarili!")

#veritabanına kullanicinin giris yapmasi icin gereken fonksiyon
def giris_yap(session):
    kullanici_adi = input("Kullanici adi: ")
    sifre = input("Sifre: ")

    kullanici = session.query(Kullanici).filter(Kullanici.kullanici_adi == kullanici_adi, Kullanici.sifre == sifre).first()
    if kullanici:
        print("Giris basarili!")
        return kullanici
    else:
        print("Kullanici adi veya sifre hatali.")
        return None
        
#veritabanına kitap kaydetme fonksiyonu
def kitap_oku(session, kullanici):
    kitap_basligi = input("Okudugunuz kitabin adi: ")
    yeni_okunan_kitap = OkunanKitap(baslik=kitap_basligi, kullanici_id=kullanici.id)
    session.add(yeni_okunan_kitap)
    session.commit()
    print(f"{kitap_basligi} kitabi kaydedildi.")

#veritabanina kayitli kitaplarini görme fonsiyonu
def kitaplarimi_gor(session, kullanici):
    kitaplar = session.query(OkunanKitap).filter(OkunanKitap.kullanici_id == kullanici.id).all()
    if kitaplar:
        print("Okudugunuz kitaplar:")
        for kitap in kitaplar:
            print(f"- {kitap.baslik}")
    else:
        print("Henüz kitap okumadiniz.")
