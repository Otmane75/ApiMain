from flask import Flask,render_template,request,make_response
import gestionDB as db
from flask_restful import Api
from flask_restful import Resource,reqparse
import gestion_cert.sign_csr as mcsr
import json
from io import BytesIO
import signature.back as back

app = Flask(__name__)
api = Api(app)



class getConta(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, required=True)
        super(getConta, self).__init__()

    def get(self):
        contacts = db.lire_contacts()
        return contacts

    def post(self):
        args = self.parser.parse_args()
        arg1 = args['param']
        certificat=db.lire_certificat(int(arg1))
        # Logique pour créer un nouvel utilisateur
        #return {'user_id': param, 'name': 'John Doe'}
        return certificat
api.add_resource(getConta, '/contacts', '/contacts/<int:param>')

class manCert(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('csr', type=str)
        self.parser.add_argument('nom', type=str)
        self.parser.add_argument('prenom', type=str)
        self.parser.add_argument('cert_ed25519', type=str)
        self.parser.add_argument('cert_eccp256', type=str)
        super(manCert, self).__init__()

    def get(self):
        
        # Crée un dictionnaire Python
        data = {
            "nom": "John",
            "age": 30,
            "marié": True,
            "hobbies": ["lecture", "voyages", "natation"]
        }

        
        return data

    def post(self):
        args = self.parser.parse_args()
        arg1 = args['csr']
        certificat=mcsr.signCSR(arg1)
        print(certificat)

        data = {
            "certificat": certificat,
            
        }
        
        # Logique pour créer un nouvel utilisateur
        #return {'user_id': param, 'name': 'John Doe'}
        return data
    
    def put(self):
        args = self.parser.parse_args()
        nom = args['nom']
        prenom = args['prenom']
        cert_ed25519 = args['cert_ed25519']
        cert_eccp256 = args['cert_eccp256']
        if db.ajouter_contact(nom,prenom,cert_ed25519,cert_eccp256):
            data = {
                "ret": "contact ajouté avec succes",
                
            }
        
        # Logique pour créer un nouvel utilisateur
        #return {'user_id': param, 'name': 'John Doe'}
        return data
api.add_resource(manCert, '/csr', '/csr/<string:csr>')



class operations(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('operations', type=list, location='json')
        super(operations, self).__init__()

    def get(self):
        operations=db.lire_operations()    
        return operations

    def post(self):
        args = self.parser.parse_args()
        operations_list = args['operations']
        
        for oper in operations_list:
            db.ajouter_operation(oper[1], oper[2],oper[3],oper[4])
        return operations_list
api.add_resource(operations, '/operations', '/operations/<string:csr>')

pdf_files = []
class Verification(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('signataire', type=int, location='json')
        super(Verification, self).__init__()

    def get(self):
        html = render_template('index.html')
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        return response

    def post(self):
        pdf_file = request.files.get('pdf_file')
        args = self.parser.parse_args()
        signataire = args['signataire']

        if pdf_file is None:
            return {'message': 'Aucun fichier PDF soumis'}, 400

        if not pdf_file.filename.endswith('.pdf'):
            return {'message': 'Le fichier doit avoir une extension .pdf'}, 400

        # Traitez le fichier PDF ici (par exemple, vous pouvez le sauvegarder sur le serveur)
        pdf_file_content = pdf_file.read() # Lire le contenu en mode binaire

        #pdf = BytesIO(pdf_file_content)
        #pdf_file.save('test.pdf')
        #print(pdf)

        #pdf_stream = BytesIO(pdf_file.read())
        #print(pdf_file_content)

        reponse=back.verifier_signature(pdf_file_content)
        
        pdf_files.append(pdf_file.filename)  # Ajoutez le nom du fichier à la liste

        return {'message': 'Fichier PDF reçu avec succes','signature':reponse,'signataire':signataire}, 201
    

api.add_resource(Verification, '/verify', '/verify/')

'''
@app.route('/')
def hello():
    contacts = db.lire_contacts()
    return contacts
'''
if __name__ == '__main__':
    app.run()
