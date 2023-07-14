

import OpenSSL.crypto 
import gestion_cert.info_csr as info



def signCSR(csr_data):
    print(csr_data)
    csr = OpenSSL.crypto.load_certificate_request(
        OpenSSL.crypto.FILETYPE_PEM, csr_data)
    #info.extract_csr_info(csr)
    

    # Charger la clé privée du certificat signataire
    with open('private_keyOTM.pem', 'r') as f:
        signing_key_data = f.read().encode('utf-8')
        signing_key = OpenSSL.crypto.load_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, signing_key_data)
    # Charger l'émetteur (issuer) du certificat signataire
    with open('certificateOTM.pem', 'r') as f:
        signing_cert_data = f.read().encode('utf-8')
        signing_cert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, signing_cert_data)
        issuer = signing_cert.get_subject()
    
    
    # Créer le certificat signé
    cert = OpenSSL.crypto.X509()
    cert.set_subject(csr.get_subject())
    cert.set_pubkey(csr.get_pubkey())
    cert.set_notBefore(b'20230701000000Z')
    cert.set_notAfter(b'20240701000000Z')
    cert.set_serial_number(1000)
    cert.set_issuer(issuer)
    cert.sign(signing_key, 'sha256')


    cert_pem = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert).decode('utf-8')
    return cert_pem
    '''
    # Enregistrer le certificat signé dans un fichier
    with open('cert1.pem', 'w') as f:
        f.write(OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert).decode('utf-8'))
    '''


'''
# Charger le CSR à signer
with open('csr.pem', 'r') as f:
    csr_data = f.read().encode('utf-8')
    print(csr_data)
    csr = OpenSSL.crypto.load_certificate_request(
        OpenSSL.crypto.FILETYPE_PEM, csr_data)
    
# Charger la clé privée du certificat signataire
with open('private_keyOTM.pem', 'r') as f:
    signing_key_data = f.read().encode('utf-8')
    signing_key = OpenSSL.crypto.load_privatekey(
        OpenSSL.crypto.FILETYPE_PEM, signing_key_data)



# Charger l'émetteur (issuer) du certificat signataire
with open('certificate.pem', 'r') as f:
    signing_cert_data = f.read().encode('utf-8')
    signing_cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, signing_cert_data)
    issuer = signing_cert.get_subject()

# Créer le certificat signé
cert = OpenSSL.crypto.X509()
cert.set_subject(csr.get_subject())
cert.set_pubkey(csr.get_pubkey())
cert.set_notBefore(b'20230701000000Z')
cert.set_notAfter(b'20240701000000Z')
cert.set_serial_number(1000)
cert.set_issuer(issuer)
cert.sign(signing_key, 'sha256')

# Enregistrer le certificat signé dans un fichier
with open('cert.pem', 'w') as f:
    f.write(OpenSSL.crypto.dump_certificate(
        OpenSSL.crypto.FILETYPE_PEM, cert).decode('utf-8'))
'''