from flask import Flask, jsonify, request
from models import Category, Product
from schemas import ErrorSchema, ErrorEntitySchema, CategorySchema, CategoryEditSchema, ProductSchema, \
    ProductEditSchema, ProductCreateSchema
from marshmallow.exceptions import ValidationError
from flasgger import Swagger, swag_from
from mongoengine import connect

connect(
    db='ecommerce',
    host='127.0.0.1',
    port=27017,
    username='db_username',
    password='db_password',
    authentication_source='admin'
)

app = Flask(__name__)
swag = Swagger(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/category-create', methods=['POST'])
@swag_from({
    'tags': ['Category'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': CategorySchema
    }],
    'responses': {
        200: {
            'description': 'Register has been created.',
            'schema': CategorySchema
        },
        422: {
            'description': 'Unprocessable Entity.',
            'schema': ErrorEntitySchema
        },
        500: {
            'description': 'Internal Server Error.',
            'schema': ErrorSchema
        }
    }
})
def category_create():
    """
    Create category
    """
    try:
        data_ = CategorySchema().load(request.json)
        object_ = Category(**data_)
        object_.save()
        data_ = CategorySchema().dump(object_)

        return jsonify({'data': data_}), 201
    except ValidationError as e:
        print(e)
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}

        return jsonify(errors), 422
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error.'}), 500


@app.route('/category-list', methods=['GET'])
@swag_from({
    'tags': ['Category'],
    'responses': {
        200: {
            'schema': CategorySchema
        }
    }
})
def category_list():
    """
    Listing Category
    """
    objects_ = Category.objects
    data_ = CategorySchema().dump(objects_, many=True)

    return jsonify({'data': data_}), 200


@app.route('/category/<string:category_id>', methods=['PATCH'])
@swag_from({
    'tags': ['Category'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': CategoryEditSchema
    }],
    'responses': {
        200: {
            'schema': CategoryEditSchema
        },
        404: {
            'description': 'Register Not Found.',
            'schema': ErrorSchema
        },
        422: {
            'description': 'Unprocessable Entity.',
            'schema': ErrorEntitySchema
        },
        500: {
            'description': 'Internal Server Error',
            'schema': ErrorSchema
        }
    }
})
def category_edit(category_id):
    """
    Edit category
    """
    try:
        object_ = Category.objects.with_id(category_id)
        data_ = CategoryEditSchema().load(request.json)
        object_.update(**data_)

        return jsonify({'message': 'Edit done!'}), 200

    except ValidationError as e:
        print(e)
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}
        return jsonify(errors), 422
    except Exception as e:
        print(e)
        return jsonify({'message': 'Not found'}), 404


@app.route('/category-list/<string:category_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Categories'],
    'parameters': [{  # ESTUDAR SOBRE ESSES PARAMETROS
        'in': 'path',
        'name': 'path',
        'required': True,
        'schema': CategorySchema
    }],
    'responses': {
        204: {
            'description': 'Delete done!',
            'schema': ErrorSchema
        },
        404: {
            'description': 'Not Found.',
            'schema': ErrorSchema
        }
    }
})
def category_delete(category_id):
    """
    Delete category
    """
    try:
        category = Category.objects.with_id(category_id)
        if Product.objects(category=category['id']):
            return 'Product registered in this category', 422
        else:
            data_ = CategorySchema().dump(category)
            Category.delete(category)
            return jsonify({'data': data_}), 204

    except Exception as e:
        print(e)
        return jsonify({'message': 'Not found'}), 404


# ---------------------------------------------- P R O D U T O --------------------------------------------------------


@app.route('/products-create', methods=['POST'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        200: {
            'description': 'The register has been created.',
            'schema': ProductSchema
        },
        422: {
            'description': 'Unprocessable Entity.',
            'schema': ErrorEntitySchema
        },
        500: {
            'description': 'Internal Server Error.',
            'schema': ErrorSchema
        }
    }
})
def products_create():
    """
    Create products
    """
    try:
        data_ = ProductCreateSchema().load(request.json)
        cat = Category.objects.with_id(data_['category'])
        if cat['status'] == 'active':
            object_ = Product(name=data_['name'], price=data_['price'], category=cat)
            object_.save()
            data_ = ProductSchema().dump(object_)
            return jsonify({'data': data_}), 201
        else:
            return 'Category is inactive', 422
    except ValidationError as e:
        print(e)
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}
        return jsonify(errors), 422
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error.'}), 500


@app.route('/products-list', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'responses': {
        200: {
            'schema': ProductSchema
        }
    }
})
def products_list():
    """
    Listing products
    """
    objects_ = Product.objects
    data_ = ProductSchema().dump(objects_, many=True)

    return jsonify({'data': data_}), 200


@app.route('/products/<string:product_id>', methods=['PATCH'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductEditSchema
    }],
    'responses': {
        200: {
            'schema': ProductEditSchema
        },
        404: {
            'description': 'Register Not Found.',
            'schema': ErrorSchema
        },
        422: {
            'description': 'Unprocessable Entity.',
            'schema': ErrorEntitySchema
        },
        500: {
            'description': 'Internal Server Error',
            'schema': ErrorSchema
        }
    }
})
def products_edit(product_id):
    """
    Edit products
    """
    try:
        data_ = ProductEditSchema().load(request.json)
        object_ = Product.objects.with_id(product_id)
        if data_['name'] and data_['price']:
            print("0")
            object_['name'] = data_['name']
            object_['price'] = data_['price']

        elif data_['name'] and data_['category']:
            print("1")
            if data_['name']:object_['name'] = data_['name']
            data_['category'] = Category.objects.with_id(data_['category'])
            object_['category'] = data_['category']

        elif data_['price'] and data_['category']:
            print("2")
            object_['price'] = data_['price']
            data_['category'] = Category.objects.with_id(data_['category'])
            object_['category'] = data_['category']

        elif data_['name'] and data_['price'] and data_['category']:
            print("3")
            object_['name'] = data_['name']
            object_['price'] = data_['price']
            data_['category'] = Category.objects.with_id(data_['category'])
            object_['category'] = data_['category']

        object_.update(**data_)
        obj = ProductEditSchema().dump(object_)
        return jsonify({'data': obj}), 200

    except ValidationError as e:
        print(e)
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}
        return jsonify(errors), 422
    except Exception as e:
        print(e)
        return jsonify({'message': 'Not found'}), 404


@app.route('/products-list/<string:product_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'path',
        'name': 'path',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        204: {
            'description': 'Delete done!',
            'schema': ErrorSchema
        },
        404: {
            'description': 'Not Found.',
            'schema': ErrorSchema
        }
    }
})
def products_delete(product_id):
    """
    Delete products
    """
    try:
        prod = Product.objects.with_id(product_id)
        del_prod = ProductSchema().dump(prod)
        Product.delete(prod)
        return del_prod, 204

    except Exception as e:
        print(e)
        return jsonify({'message': 'Not found'}), 404
