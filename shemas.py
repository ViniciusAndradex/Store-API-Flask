from marshmallow import Schema, fields


class ItemSchemas(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchemas(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchemas(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)