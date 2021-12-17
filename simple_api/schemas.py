from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=2, max=30))
    status = fields.Str(required=True, allow_none=False, validate=validate.OneOf(['active', 'inactive']))

    class Meta:
        fields = ('id', 'name', 'status')
        ordered = True


class CategoryEditSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=2, max=30))
    status = fields.Str(required=True, allow_none=False, validate=validate.OneOf(['active', 'inactive']))

    class Meta:
        fields = ('id', 'name', 'status')
        ordered = True


class ProductSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=2, max=30))
    price = fields.Float(required=True, allow_none=False, validate=validate.Range(min=0))
    category = fields.Nested(CategorySchema, required=True)

    class Meta:
        fields = ('id', 'name', 'price', 'category')
        ordered = True


class ProductEditSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String(required=False, allow_none=False, validate=validate.Length(min=2, max=30))
    price = fields.Float(required=False, allow_none=False, validate=validate.Range(min=0))
    category = fields.String(required=False, allow_none=False, validate=validate.Length(min=2, max=40))

    class Meta:
        fields = ('name', 'price', 'category')
        ordered = True


class ProductCreateSchema(Schema):
    name = fields.String(required=False, allow_none=False, validate=validate.Length(min=2, max=30))
    price = fields.Float(required=False, allow_none=False, validate=validate.Range(min=0))
    category = fields.String(required=False, allow_none=False, validate=validate.Length(min=2, max=30))

    class Meta:
        fields = ('name', 'price', 'category')
        ordered = True


class ErrorSchema(Schema):
    message = fields.String(required=True, allow_none=False)


class ErrorFieldSchema(Schema):
    field_name = fields.List(fields.String(required=True), required=True)


class ErrorEntitySchema(Schema):
    message = fields.String(required=True, allow_none=False)
    errors = fields.Nested(ErrorFieldSchema, required=True)

    class Meta:
        fields = ('message', 'errors')
        ordered = True
