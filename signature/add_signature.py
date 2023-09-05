from io import BytesIO
import re
import hashlib


def ajouter_signature(pdf, contenu_signature):

    # Lire le PDF
    with open(pdf, "rb") as fic:
        pdf = fic.read()

    # Trouver l'indice du prochain objet
    objets = re.findall(b"(\d+) 0 obj", pdf)

    if objets:
        objet = objets[-1]
        indice = int(objet) + 1
    else:
        print("Aucun objet trouvé dans le PDF")
        objet = 0
        indice = 1

    #objet = re.findall(b"/(\d+) 0 obj", pdf)[-1]
    #indice = int(objet) + 1
    #print(indice)

    # Ajouter le nouvel objet
    signa = b"endobj\n"
    signa += b"%d 0 obj\n" % indice
    signa += b"<<\n"
    signa += b"  /Type /Signature\n"
    signa += b"  /Filter /Adobe.PPKLite\n"
    signa += b"  /SubFilter /adbe.pkcs7.sha1\n"
    signa += b"  /Contents <%s>\n" % contenu_signature
    signa += b">>\n"
    signa += b"endobj"
    # print(signa)
    pdf = pdf.replace(b"endobj", signa, 1)

    # Enregistrer le PDF modifié
    with open("signature/add_signature/sortie.pdf", "wb") as fic:
        fic.write(pdf)


def recuperer_signature(pdf):
    # Lire le PDF
    #pdf=pdf.read()
    #pdf = BytesIO(pdf_stream.read())
    #with open(pdf, "rb") as fic:
    #    pdf = fic.read()

    # Trouver l'objet de signature
    objet = re.search(b"(\d+) 0 obj\n<<\n  /Type /Signature", pdf)

    if objet:
        numero_objet = objet.group(1)

        # Trouver le contenu de l'objet
        debut = pdf.index(b"%s 0 obj" % numero_objet)
        fin = pdf.index(b"endobj", debut)

        # Extrait le contenu de l'objet
        signature = pdf[debut:fin]
        num = int(signature.split(b" 0")[0])
        signature2 = signature.split(
            b"/Contents")[1].split(b"<")[1].split(b">")[0]

        return [num, signature2]

    else:
        return None


def supprimer_objet(pdf, numero_objet):

    # Lire le PDF
    #with open(pdf, "rb") as fic:
    #    pdf = fic.read()

    # Trouver le début et la fin de l'objet
    debut = pdf.index(f"{numero_objet} 0 obj".encode())
    fin = pdf.index(b"endobj", debut)

    # Supprimer l'objet de la chaîne de caractères
    pdf = pdf[:debut-7] + pdf[fin:]

    # Enregistrer le PDF mis à jour
    with open("signature/output.pdf", "wb") as fic:
        fic.write(pdf)
######################################################################


def calculer_hash_pdf(fichier_pdf):
    hash_pdf = hashlib.sha256()
    with open(fichier_pdf, "rb") as f:
        hash_pdf.update(f.read())
    return hash_pdf.hexdigest()


######################################################################
#signature = b"5468697320697320616e206578616d706c65207369676e617475726520696e2048657861646563696d616c21"
#ajouter_signature("signature/add_signature/document.pdf", signature)

'''
signature = recuperer_signature("signature/add_signature/sortie.pdf")
print(signature[1])
# if signature:
#    numero_objet = int(re.search(b"/(\d+) 0 obj", signature).group(1))
supprimer_objet("sortie.pdf", signature[0])


hash_original = calculer_hash_pdf("signature/add_signature/document.pdf")
hash_final = calculer_hash_pdf("signature/add_signature/sortie.pdf")

hash_final2 = calculer_hash_pdf("signature/add_signature/output.pdf")


print("hash_original: "+hash_original)
print("hash_final: "+hash_final)
print("hash_final2: "+hash_final2)
'''