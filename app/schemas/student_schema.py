from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date


class StudentSchema(Schema):
    """
    Schema for validating and serializing Student data
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Name is required'}
    )
    department = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Department is required'}
    )
    cgpa = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=4.0),
        error_messages={'required': 'CGPA is required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required', 'invalid': 'Invalid email format'}
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('cgpa')
    def validate_cgpa(self, value):
        if value < 0.0 or value > 4.0:
            raise ValidationError('CGPA must be between 0.0 and 4.0')


class StudentUpdateSchema(Schema):
    """
    Schema for validating student update data (partial updates allowed)
    """
    name = fields.Str(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    department = fields.Str(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    cgpa = fields.Float(
        validate=validate.Range(min=0.0, max=4.0),
        allow_none=True
    )
    email = fields.Email(allow_none=True)
    
    @validates('cgpa')
    def validate_cgpa(self, value):
        if value is not None and (value < 0.0 or value > 4.0):
            raise ValidationError('CGPA must be between 0.0 and 4.0')
