import hashlib


from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.x509 import load_pem_x509_certificate
import random
import string


############################################################################################################################
def sha512_for_pdf(pdf_path):
    hash = hashlib.sha512()
    with open(pdf_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()



def verify_signature(signature,challenge):
    
    #with open('certificatePerso.pem', 'rb') as cert_file:
    with open('signature/certificate_ed25519.pem', 'rb') as cert_file:
        cert_data = cert_file.read()
    cert = load_pem_x509_certificate(cert_data)
    
    
    public_key = cert.public_key()

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    public_key_hex = public_key_bytes.hex()
    print("Public Key:", public_key_hex)
    message = challenge.encode()
    signature_hex = signature
    signature = bytes.fromhex(signature_hex)
    try:
        public_key.verify(signature, message)
        print("La signature est valide.")
        return True
    except InvalidSignature:
        print("La signature est invalide.")



'''
pdf_path = 'document_decrypted.pdf'
pdf_hash = sha512_for_pdf(pdf_path)
print(pdf_hash)
if demande_signature(str(pdf_hash)):
    print("ues")
else:
    print("noooo")
'''

#print(sign_pdf('sortie.pdf'))