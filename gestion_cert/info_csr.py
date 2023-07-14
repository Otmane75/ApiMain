from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def extract_csr_info(csr_content):
    # Charger le CSR à partir du fichier PEM
    
    csr = x509.load_pem_x509_csr(csr_content.encode('utf-8'), default_backend())
    
    # Extraire les informations du CSR
    subject = csr.subject
    public_key = csr.public_key()

    # Convertir la clé publique au format PEM
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Afficher les informations extraites
    print("Sujet du CSR :", subject)
    print("Clé publique du CSR (format PEM) :\n", public_key_pem.decode())





