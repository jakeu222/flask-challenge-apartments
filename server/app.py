from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Tenant, Apartment, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )
api = Api(app)


@app.route("/apartments", methods=['GET', 'POST'])
def apartments_func():
    if request.method == 'GET':
        apt = Apartment.query.all()
        data = [apartment.to_dict() for apartment in apt]

        return make_response(
            jsonify(data),
            200
        )
    else:
        data = request.get_json()
        try:
            new_apartment = Apartment(
                number=data.get('number')
            )
            db.session.add(new_apartment)
            db.session.commit()

        except Exception:
            raise ValueError("Please provide a number")
        
        return make_response(new_apartment.to_dict(), 201)
    
@app.route("/apartments/<int:id>", methods=['PATCH', 'DELETE'])
def apartments_by_id(id):
    if request.method == 'PATCH':
        apt = Apartment.query.filter(Apartment.id == id).first()
        data = request.get_json()

        if not apt:
            return make_response({"error": "Apartment doesn't exist"}, 404)
        try:
            for field in data:
                setattr(apt, field, data[field])
            db.session.commit()
        except ValueError:
            raise ValueError("Something went wrong, probably your number")

        return make_response(
            jsonify(apt.to_dict()),
            202
        )
    elif request.method == 'DELETE':
        apt = Apartment.query.filter(Apartment.id == id).first()
        if not apt:
            return make_response({"error": "Apartment doesn't exist"}, 404)
        db.session.delete(apt)
        db.session.commit()

        return make_response({}, 204)
    




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




@app.route("/tenant", methods=['GET', 'POST'])
def tenant_func():
    if request.method == 'GET':
        apt = Tenant.query.all()
        data = [baranHawaiiShirt.to_dict() for baranHawaiiShirt in apt]

        return make_response(
            jsonify(data),
            200
        )
    else:
        data = request.get_json()
        try:
            new_apartment = Tenant(
                name=data.get('name'),
                age=data.get('age')
            )
            db.session.add(new_apartment)
            db.session.commit()

        except Exception:
            raise ValueError("Please provide a name and age")
        
        return make_response(new_apartment.to_dict(), 201)


@app.route("/tenant/<int:id>", methods=['PATCH', 'DELETE'])
def tenant_by_id(id):
    if request.method == 'PATCH':
        apt = Tenant.query.filter(Tenant.id == id).first()
        data = request.get_json()

        if not apt:
            return make_response({"error": "Tenant doesn't exist"}, 404)
        try:
            for field in data:
                setattr(apt, field, data[field])
            db.session.commit()
        except ValueError:
            raise ValueError("Something went wrong, probably your name or age")

        return make_response(
            jsonify(apt.to_dict()),
            202
        )
    elif request.method == 'DELETE':
        apt = Tenant.query.filter(Tenant.id == id).first()
        if not apt:
            return make_response({"error": "Tenant doesn't exist"}, 404)
        db.session.delete(apt)
        db.session.commit()

        return make_response({}, 204)
    

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Leases(Resource):
    def get(self):
        data = [lease.to_dict() for lease in db.session.query(Lease).all()]
        return data, 200
    
    def post(self):
        data = request.get_json()
        try:
            new_lease = Lease(
                rent=data.get('rent'),
                apartment_id=data.get('apartment_id'),
                tenant_id=data.get('tenant_id')
            )
            db.session.add(new_lease)
            db.session.commit()

        except Exception:
            raise ValueError("Please provide appropiate data")
        
        return new_lease.to_dict(), 201
    
api.add_resource(Leases, '/lease')

class LeaseID(Resource):
    def delete(self, id):
        apt = Lease.query.filter(Lease.id == id).first()
        if not apt:
            return make_response({"error": "Lease doesn't exist"}, 404)
        db.session.delete(apt)
        db.session.commit()

        return make_response({}, 204)
    
api.add_resource(LeaseID, '/lease/<int:id>')









if __name__ == '__main__':
    app.run( port = 3000, debug = True )









# from flask import Flask, make_response, jsonify,request
# from flask_migrate import Migrate
# from flask_restful import Api, Resource
# from models import db, Apartment, Tenant, Lease

# from models import db

# app = Flask( __name__ )
# app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
# app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

# migrate = Migrate( app, db )
# db.init_app( app )

# # @app.route('/')
# # def home():
# #     return ''

# # @app.get('/apartments')
# # def get_all_apartments():
# #     apartments = Apartment.query.all()
# #     data = [apartment.to_dict(rules=("-lease",)) for apartment in apartments]

# #     return make_response(
# #         jsonify(data),
# #         200
# #     )

# # @app.post('/apartments')
# # def post_apartment():
# #     data = request.get_json()

# #     try:
# #         new_apartment = Apartment(
# #             number=data.get("number")

# #         )

# #         db.session.add(new_apartment)
# #         db.session.commit()

# #         return make_response(
# #             jsonify(new_apartment.to_dict(rules=('-lease',))),
# #             201
# #         )
# #     except ValueError:
# #         return make_response(
# #             jsonify({"error": ["validation errors"]}),
# #             406
# #         )

# # @app.patch('/apartments/<init:id>')
# # def patch_apartments_by_id(id):
# #     apartment = Apartment.query.filter(Apartment.id == id).first()
# #     data = request.get_json()

# #     if not apartment:
# #         return make_response(
# #             jsonify({"error": "Camper not found"}),
# #             404
# #         )
    
# #     try:
# #         for field in data:
# #             setattr(apartment, field, data[field])
# #         db.session.add(apartment)
# #         db.session.commit()

    
# #         return make_response(
# #             jsonify(apartment.to_dict(rules=('-lease',))),
# #             202
# #         )
# #     except ValueError as e:
# #         print(e.__str__())
# #         return make_response(
# #             jsonify({"error": ["validation errors"]}),
# #             406
# #         )
    
# # @app.delete('/apartments/<int:id>')
# # def delete_apartment(id):
# #     apartment = Apartment.query.filter(Apartment.id == id).first()

# #     if not apartment:
# #         return make_response(
# #             jsonify({"error": "Activity not found"}),
# #             404
# #         )
    
# #     db.session.delete(apartment)
# #     db.session.commit()

# #     return make_response(jsonify({}), 204) 


# # @app.get('/tenants')
# # def get_all_tenants():
# #     tenants = Tenant.query.all()
# #     data = [tenant.to_dict(rules=("-lease",)) for tenant in tenants]

# #     return make_response(
# #         jsonify(data),
# #         200
# #     )

# # @app.post('/tenants')
# # def post_tenant():
# #     data = request.get_json()

# #     try:
# #         new_tenant = Tenant(
# #             name=data.get("name")

# #         )

# #         db.session.add(new_tenant)
# #         db.session.commit()

# #         return make_response(
# #             jsonify(new_tenant.to_dict(rules=('-lease',))),
# #             201
# #         )
# #     except ValueError:
# #         return make_response(
# #             jsonify({"error": ["validation errors"]}),
# #             406
# #         )

# # @app.patch('/tenants/<init:id>')
# # def patch_tenants_by_id(id):
# #     tenant = Tenant.query.filter(Tenant.id == id).first()
# #     data = request.get_json()

# #     if not tenant:
# #         return make_response(
# #             jsonify({"error": "Camper not found"}),
# #             404
# #         )
    
# #     try:
# #         for field in data:
# #             setattr(tenant, field, data[field])
# #         db.session.add(tenant)
# #         db.session.commit()

    
# #         return make_response(
# #             jsonify(tenant.to_dict(rules=('-lease',))),
# #             202
# #         )
# #     except ValueError as e:
# #         print(e.__str__())
# #         return make_response(
# #             jsonify({"error": ["validation errors"]}),
# #             406
# #         )
# # @app.delete('/tenants/<int:id>')
# # def delete_tenant(id):
# #     tenant = Tenant.query.filter(Tenant.id == id).first()

# #     if not tenant:
# #         return make_response(
# #             jsonify({"error": "Activity not found"}),
# #             404
# #         )
    
# #     db.session.delete(tenant)
# #     db.session.commit()

# #     return make_response(jsonify({}), 204) 


# # @app.get('/leases')
# # def get_all_leases():
# #     leases = Lease.query.all()
# #     data = [lease.to_dict(rules=("-tenant.lease","-apartment.lease")) for lease in leases]

# #     return make_response(
# #         jsonify(data),
# #         200
# #     )






# if __name__ == '__main__':
#     app.run( port = 3000, debug = True )