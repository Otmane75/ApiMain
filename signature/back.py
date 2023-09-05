import signature.add_signature as ADD_SIG
import signature.signature as SIG


def verifier_signature(fichier_verif_sig):
    signature = ADD_SIG.recuperer_signature(fichier_verif_sig)
    ADD_SIG.supprimer_objet(fichier_verif_sig, signature[0])
    hash = SIG.sha512_for_pdf("signature/output.pdf")
    print(signature[1].decode('ISO-8859-1'))
    print(hash)
    SIG.verify_signature(signature[1].decode('ISO-8859-1'),hash)

