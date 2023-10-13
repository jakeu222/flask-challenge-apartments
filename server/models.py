from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartment_table'

    id = db.Column(db.Integer, primary_key =True)
    number = db.Column(db.Integer, nullable=False )
    lease_a_relationship = db.relationship('Lease', back_populates='apartment_relationship')
    # lease = db.relationship('Lease', backref='apartment')


class Tenant(db.Model, SerializerMixin):
    __tablename__="tenant_table"

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    lease_t_relationship = db.relationship('Lease', back_populates='tenant_relationship')
    # lease = db.relationship('Lease', backref='tenant')

    @validates('age')
    def validate_age(self, key, age):
        if isinstance(age, int) and age >= 18:
            return age
        else:
            raise ValueError("Not a valid age, you are too young!")



class Lease(db.Model, SerializerMixin):
    __tablename__="lease_table"

    id = db.Column(db.Integer, primary_key =True)
    rent = db.Column(db.Integer, nullable=False)

    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment_table.id'))
    apartment_relationship = db.relationship('Apartment', back_populates='lease_a_relationship')

    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant_table.id'))
    tenant_relationship = db.relationship('Tenant', back_populates='lease_t_relationship')

    serialize_rules = ('-tenant_relationship', '-apartment_relationship')











# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Api, Resource
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy

# db = SQLAlchemy()


# class Apartment(db.Model,SerializerMixin):
#     __tablename__ = 'apartment_table'

#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.Integer)

#     lease = db.relationship('Lease', backref='apartment')

#     def __repr__(self):
#         return f'Apartment {self.id, self.number}'


# class Tenant(db.Model,SerializerMixin):
#     __tablename__ = 'tenant_table'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     age = db.Column(db.Integer)

#     lease = db.relationship('Lease', backref='tenant')

#     @validates('age')
#     def validate_age(self,key, age):
#         if not age >= 18:
#             raise ValueError('Invalid age!')
#         return age
#     def __repr__(self):
#         return f'<Camper {self.id}, {self.name}'

# class Lease(db.Model,SerializerMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     rent = db.Column(db.Float)
#     apartment_id = db.Column(db.Integer, db.ForeignKey('apartment_table.id'))
#     tenant_id = db.Column(db.Integer, db.ForeignKey('tenant_table.id'))
#     serialize_rules = ('-tenant', '-apartment' )

#     def __repr__(self):
#         return f'<Lease {self.id}>'