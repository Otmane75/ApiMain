from flask import Flask
import gestionDB as db
from flask_restful import Api
from flask_restful import Resource,reqparse
import gestion_cert.sign_csr as mcsr
import json

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
        self.parser.add_argument('operations', type=list)
        super(operations, self).__init__()

    def get(self):
        operations=db.lire_operations()    
        return operations

    def post(self):
        args = self.parser.parse_args()
        operations_list = args['operations']
        
        for oper in operations_list:
            db.ajouter_operation(oper[1], oper[2],oper[3],oper[4])
        return True
api.add_resource(operations, '/operations', '/operations/<string:csr>')

'''
@app.route('/')
def hello():
    contacts = db.lire_contacts()
    return contacts
'''
if __name__ == '__main__':
    app.run()
