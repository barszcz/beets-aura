
from flask_restful import fields
from beets.dbcore import types

beets_type_map = {
    types.Boolean: fields.Boolean,
    types.Float: fields.Float,
    types.Integer: fields.Integer,
    types.PaddedInt: fields.Integer,
    types.ScaledInt: fields.Integer,
    types.String: fields.String
}

def conv_beets_type(b_type):
    return beets_type_map.get(b_type)
