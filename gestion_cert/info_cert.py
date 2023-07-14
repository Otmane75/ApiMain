from cryptography import x509
from cryptography.hazmat.backends import default_backend


def extract_certificate_info(cert_path):
    # Charger le certificat à partir du fichier PEM
    with open(cert_path, "rb") as cert_file:
        cert = x509.load_pem_x509_certificate(
            cert_file.read(), default_backend())

    # Extraire les informations du certificat
    subject = cert.subject
    issuer = cert.issuer
    valid_from = cert.not_valid_before
    valid_to = cert.not_valid_after
    public_key = cert.public_key()

    # Afficher les informations extraites
    print("Sujet du certificat :", subject)
    print("Émetteur du certificat :", issuer)
    print("Valide du", valid_from)
    print("Valide jusqu'au", valid_to)
    print("Clé publique du certificat :", public_key)


# Exemple d'utilisation
cert_path = "cert.pem"
extract_certificate_info(cert_path)
