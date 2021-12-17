from mongoengine import Document, StringField, FloatField, ReferenceField


class Product(Document):
    name = StringField(required=True, allow_none=False, max_length=30)
    price = FloatField(required=True, allow_none=False, max_length=10)
    category = ReferenceField('Category', required=True, allow_none=False)

    meta = {'collection': 'products'}


class Category(Document):
    name = StringField(required=True, allow_none=False, max_length=30)
    status = StringField(required=True, allow_none=False)

    meta = {'collection': 'category'}
