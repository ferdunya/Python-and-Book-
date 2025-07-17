from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session


# Veritabanı ayarları
VERITABANI_URL = "sqlite:///kitaplar.db"

engine = create_engine(VERITABANI_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı modelleri
class Kullanici(Base):
    __tablename__ = "kullanicilar"
    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String, unique=True, index=True)
    sifre = Column(String)
    okunan_kitaplar = relationship("OkunanKitap", back_populates="kullanici", cascade="all, delete-orphan")

#birbirleriyle ilişkilendirilmiş base
class OkunanKitap(Base):
    __tablename__ = "okunan_kitaplar"
    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String)
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id"))
    kullanici = relationship("Kullanici", back_populates="okunan_kitaplar")

#admin masası fonksiyonu
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String, unique=True, index=True)
    sifre = Column(String)

Base.metadata.create_all(bind=engine)

# Servis fonksiyonları
def kayit_ol(session: Session, kullanici_adi: str, sifre: str) -> str:
    if session.query(Kullanici).filter(Kullanici.kullanici_adi == kullanici_adi).first():
        return "Bu kullanici adi zaten alinmis."
    
    yeni_kullanici = Kullanici(kullanici_adi=kullanici_adi, sifre=sifre)
    session.add(yeni_kullanici)
    session.commit()
    return "Kayit basarili!"

#giris yapan kullanici adi ve sifresi eslesirse giris yapabilir
def giris_yap(session: Session, kullanici_adi: str, sifre: str):
    kullanici = session.query(Kullanici).filter(Kullanici.kullanici_adi == kullanici_adi, Kullanici.sifre == sifre).first()
    if kullanici:
        return "Giris basarili!", kullanici
    else:
        return "Kullanici adi veya sifre hatali.", None

#veritabanina kitap ekleme fonksiyonu
def kitap_oku(session: Session, kullanici: Kullanici, kitap_basligi: str) -> str:
    yeni_okunan_kitap = OkunanKitap(baslik=kitap_basligi, kullanici_id=kullanici.id)
    session.add(yeni_okunan_kitap)
    session.commit()
    return f"{kitap_basligi} kitabi kaydedildi."

def kitaplarimi_gor(session: Session, kullanici: Kullanici):
    kitaplar = session.query(OkunanKitap).filter(OkunanKitap.kullanici_id == kullanici.id).all()
    if kitaplar:
        return [kitap.baslik for kitap in kitaplar]
    else:
        return "Henüz kitap okumadiniz."

#admin giris fonksiyonu eslesme
def admin_girisi(session: Session, kullanici_adi: str, sifre: str):
    admin = session.query(Admin).filter(Admin.kullanici_adi == kullanici_adi, Admin.sifre == sifre).first()
    if admin:
        return "Admin girisi basarili!", True
    else:
        return "Admin kullanici adi veya sifre hatali.", False

def tum_kullanicilari_goruntule(session: Session):
    kullanicilar = session.query(Kullanici).all()
    result = []
    for kullanici in kullanicilar:
        kitaplar = [kitap.baslik for kitap in kullanici.okunan_kitaplar]
        result.append((kullanici.kullanici_adi, kitaplar))
    return result

def kullanici_sil(session: Session, kullanici_adi: str) -> str:
    kullanici = session.query(Kullanici).filter(Kullanici.kullanici_adi == kullanici_adi).first()
    if kullanici:
        session.delete(kullanici)
        session.commit()
        return f"{kullanici_adi} kullanicisi silindi."
    else:
        return "Kullanici bulunamadi."
