from schema import Schema, Or


def paginate_schema(original_schema):
    paginated_schema = Schema({
        "count": int,
        "next": Or(str, None),
        "previous": Or(str, None),
        "current_page": int,
        "items_per_page": int,
        "results": original_schema
    })
    return paginated_schema
