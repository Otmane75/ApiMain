from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
#from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Remplacez "utilisateur", "mot_de_passe", "nom_de_la_base_de_donnees" et "hote" par les valeurs appropriées
# (par exemple, "postgres", "mdp_postgres", "ma_base_de_donnees" et "localhost")

# Chaîne de connexion à PostgreSQL
#db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

db_url = f"postgresql://dbpostgre_k2mh_user:f7KuOrLLKjpxRQErnFbj1Tc9MRkGK7IJ@dpg-cj40jdmnqql8v0cr6vl0-a.frankfurt-postgres.render.com/dbpostgre_k2mh"

# Créez le moteur SQLAlchemy
engine = create_engine(db_url)
# Création de la base de données SQLite

#engine = create_engine('sqlite:///contacts.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Définition de la classe Contact pour mapper la table "contact"



class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    certificat_num = Column(String)
    certificat_ecc = Column(String)


class Historique(Base):
    __tablename__ = 'historique' 
    id = Column(Integer, primary_key=True)
    emetteur = Column(String)
    destinataire = Column(String)
    operation = Column(String)
    date = Column(String)
    commited = Column(Integer)    


# Création de la table "contact" dans la base de données
Base.metadata.create_all(engine)

# Fonctions pour ajouter, modifier et supprimer un contact
def ajouter_operation(emetteur, destinataire,operation,date):
    db_url = "postgresql://dbpostgre_k2mh_user:f7KuOrLLKjpxRQErnFbj1Tc9MRkGK7IJ@dpg-cj40jdmnqql8v0cr6vl0-a.frankfurt-postgres.render.com/dbpostgre_k2mh"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    operation = Historique(emetteur=emetteur, destinataire=destinataire,operation=operation,date=date,commited=1)
    session.add(operation)
    session.commit()


def lire_operations():
    db_url = "postgresql://dbpostgre_k2mh_user:f7KuOrLLKjpxRQErnFbj1Tc9MRkGK7IJ@dpg-cj40jdmnqql8v0cr6vl0-a.frankfurt-postgres.render.com/dbpostgre_k2mh"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    operations=session.query(Historique).all()
    if operations:
        result=[]
        for oper in operations:
            
            elem=[oper.id,oper.emetteur,oper.destinataire,oper.operation,oper.date,oper.commited]
            result.append(elem)
        return result
    else :
        return "Aucune operations trouvée"

def ajouter_contact(nom, prenom, certificat_num,certificat_ecc):
    db_url = "postgresql://dbpostgre_k2mh_user:f7KuOrLLKjpxRQErnFbj1Tc9MRkGK7IJ@dpg-cj40jdmnqql8v0cr6vl0-a.frankfurt-postgres.render.com/dbpostgre_k2mh"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    contact = Contact(nom=nom, prenom=prenom, certificat_num=certificat_num,certificat_ecc=certificat_ecc)
    session.add(contact)
    session.commit()
    session.close()
    print("Contact ajouté avec succès.")
    return True


def modifier_contact(contact_id, nom, prenom, certificat_num,certificat_ecc):
    contact = session.query(Contact).get(contact_id)
    if contact:
        contact.nom = nom
        contact.prenom = prenom
        contact.certificat_num = certificat_num
        contact.certificat_ecc=certificat_ecc
        session.commit()
        print("Contact modifié avec succès.")
    else:
        print("Contact introuvable.")


def supprimer_contact(contact_id):
    contact = session.query(Contact).get(contact_id)
    if contact:
        session.delete(contact)
        session.commit()
        print("Contact supprimé avec succès.")
    else:
        print("Contact introuvable.")


def lire_certificat(contact_id):
    db_url = "postgresql://dbpostgre_k2mh_user:f7KuOrLLKjpxRQErnFbj1Tc9MRkGK7IJ@dpg-cj40jdmnqql8v0cr6vl0-a.frankfurt-postgres.render.com/dbpostgre_k2mh"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    contact = session.query(Contact).get(contact_id)
    element = str(contact.id)+'|'+contact.nom+'|'+contact.prenom+'|'+contact.certificat_num+'|'+contact.certificat_ecc
    return element
    
        
'''
def lire_certificat(contact_id):
    engine = create_engine('sqlite:///contacts.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    contact = session.query(Contact).get(contact_id)
    if contact:
        certificat_num = contact.certificat_num
        with open("certificate.pem", "w") as file:
            file.write(certificat_num)
        element = str(contact.id)+'|'+contact.nom+'|'+contact.prenom
        with open("contact", "w") as file:
            file.write(element)
        return certificat_num
        print(
            f"Certificat numérique du contact avec ID {contact_id}: {certificat_num}")
    else:
        return None
        print("Contact introuvable.")
'''
def lire_contacts():
    db_url = "postgresql://dbpostgre_k2mh_user:f7KuOrLLKjpxRQErnFbj1Tc9MRkGK7IJ@dpg-cj40jdmnqql8v0cr6vl0-a.frankfurt-postgres.render.com/dbpostgre_k2mh"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    contacts = session.query(Contact).all()
    if contacts:
        result = []
        for contact in contacts:
            contact_info = {
                "id": contact.id,
                "nom": contact.nom,
                "prenom": contact.prenom
            }
            result.append(contact_info)
        return result
    else:
        return "Aucun contact trouvé."


# Exemple d'utilisation des fonctions
'''
ajouter_contact("otm6", "mak6", """-----BEGIN CERTIFICATE-----
MIIDuzCCAqOgAwIBAgIUMZDkCS9NbAf7QlWvnq9ZATHO7AwwDQYJKoZIhvcNAQEL
BQAwbTELMAkGA1UEBhMCTUExCzAJBgNVBAgMAkZFMQswCQYDVQQHDAJNRTELMAkG
A1UECgwCTUUxCzAJBgNVBAsMAk1FMQwwCgYDVQQDDANPVE0xHDAaBgkqhkiG9w0B
CQEWDVlFU0BHTUFJTC5DT00wHhcNMjMwNzA0MTAwODE5WhcNMjMwODAzMTAwODE5
WjBtMQswCQYDVQQGEwJNQTELMAkGA1UECAwCRkUxCzAJBgNVBAcMAk1FMQswCQYD
VQQKDAJNRTELMAkGA1UECwwCTUUxDDAKBgNVBAMMA09UTTEcMBoGCSqGSIb3DQEJ
ARYNWUVTQEdNQUlMLkNPTTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
ALrlYKTLQI46ytf7wehAfoghQlYXSzS2W476YyUA3K7awRtjsWWLHHcxVK0f68qp
dOGqT9lrNSqtD8MA6q1zti7UAsboglbZGdoDXKAFwtlcInpCBAwfB0qcYzddMVVo
QpRy6RC9o1YCk1tuoXhZ3fes1J5Hsdfxfce9D1knI/V6OfpePn0xlSbtf1YGfku1
iyEY5JN26pkHPJTZIIuC29LjkgILC4G8v5Ua1gjUwRmReyg32qU/cCfwLYAP5h4T
7INIj/Qax6hXAc0PzPAXEEen2w4q4H3Hiy6s3tyljbfFeELv1/ncyV0YOcku9h3u
dmMtF+Pny8pemtEDPWNJGRcCAwEAAaNTMFEwHQYDVR0OBBYEFNe7KdpmMt3SE5qB
ZE0tUHLZ/leyMB8GA1UdIwQYMBaAFNe7KdpmMt3SE5qBZE0tUHLZ/leyMA8GA1Ud
EwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAJ61paqFE5TWzgTlb+f4OuWe
SrkA9ZD5jhkbpxcq8hwZ2k4TV+iI+V6/QSARinfEmpM0Su05Wc09VOTXsODXVX5k
MtVLEsdfrMHWZwAGVF2zLayeyh6DUKx0lNuOUBfD50x8Uo3q+Exr+aufO0Oh/RBX
yXjhhQj6oJtyvrdE8usrUuDlcCWxsTU3goasGmS2sbtA8dvmBFVONzUZSUwikf/8
/kmj+jq6NCM/HxDqu8+h/c3S/nhh52JoFT8kwJQKqcbVDLwWyAnv8Yp2EGnxwrrx
+CX2lLVHdbccqN/TuyggDX3mM4xoqbkKA1nc04wwFUxgOp1sUGzzkqfoQ/fLcW0=
-----END CERTIFICATE-----""", """-----BEGIN CERTIFICATE-----
cert ecc 1
-----END CERTIFICATE-----""")
ajouter_contact("asm5", "md5", """-----BEGIN CERTIFICATE-----
MIID6TCCAtGgAwIBAgIURWy5aeNYi7XKPshgsXwOkX6pvvgwDQYJKoZIhvcNAQEL
BQAwgYMxCzAJBgNVBAYTAm1hMQ4wDAYDVQQIDAVyYWJhdDENMAsGA1UEBwwEc2Fs
ZTEQMA4GA1UECgwHa2VuaXRyYTENMAsGA1UECwwEZW5zYTENMAsGA1UEAwwEZW5z
YTElMCMGCSqGSIb3DQEJARYWYXNtYWFtc2FhZDk3QGdtYWlsLmNvbTAeFw0yMzA3
MDQxMjI3MjZaFw0yMzA4MDMxMjI3MjZaMIGDMQswCQYDVQQGEwJtYTEOMAwGA1UE
CAwFcmFiYXQxDTALBgNVBAcMBHNhbGUxEDAOBgNVBAoMB2tlbml0cmExDTALBgNV
BAsMBGVuc2ExDTALBgNVBAMMBGVuc2ExJTAjBgkqhkiG9w0BCQEWFmFzbWFhbXNh
YWQ5N0BnbWFpbC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDv
J7l45X5bU5xAeBPsBnLnfr1hBVV9PQUlfawTZwkEtWZja5iam499BfSvUWk+lroK
SrM6qFfD7EHcL7gh4O0yNLi/Pv+6vxtfkvP3tBAdI78KQkPi06zGQn7E+j1KYiIw
YDjnnF2RkQ2RMdi9J04RuHRCJc2rnDBnH48zT3hFJlmLKqKhPMCV6+CbzBijGFdW
HM9l9fSHvHmoe6Mak2GJSW5m3drju4UiFICMihH/Hkb2HiMOieUtr8W/mLo7hpTp
7RSRlnOsdCSuSL/6c4HMuTlMuv45SwEnh6RVPBLvbfCIHbFHooFbgH3Hye55OlEd
zeO66tWFKBHzqAF4evLVAgMBAAGjUzBRMB0GA1UdDgQWBBT7ac6gTkg+edPHxdbB
nSUmC1m3GDAfBgNVHSMEGDAWgBT7ac6gTkg+edPHxdbBnSUmC1m3GDAPBgNVHRMB
Af8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQC52ZNRKlmVHZXmtPeWIU59Uc+L
ehEDZsXQXeT0C5jODtsWtIqupBj+GmSKVKMSuaQWuzTL89rE2GNTrfPEow+O1Tj0
SD7sU3CXe5Y2y7MfDGuZgB1PvCGbOhq5CgsiSCp/HHdIvtoaA1Qo7oa7udFuxuB3
mb3cEC4OfAQrNrKVLetnkMsKDTHJ4MUg/20G5EIXXHSdEkpnb1uiDF97xdNucT5b
m9+zUjBhtGgiXnUrXBbu6B7BoAHtBvZNoAfTKHkJ7UI2TLSPanGD25hAp9D72Ua+
KpDGEvy70v4+jrtkOclUUGdGcgutBIAbL2me8eH1M5hr+pVLT3RYJFPRNjRG
-----END CERTIFICATE-----""", """-----BEGIN CERTIFICATE-----
cert ecc
-----END CERTIFICATE-----""")'''
# lire_certificat(1)
# print(lire_contacts())
#ajouter_contact("Doe", "John", "123456789")
#modifier_contact(1, "Doe", "Jane", "987654321")
# supprimer_contact(1)
