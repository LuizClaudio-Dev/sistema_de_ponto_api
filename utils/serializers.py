import json
from datetime import datetime


def model_dict_json_serializer(model: list[dict[str, any]] | dict[str, any]) -> list[dict[str, any]] | dict[str, any]:
    if isinstance(model, list):
        result = json.loads(json.dumps(
            model, default=lambda o: o.isoformat() if isinstance(o, datetime) else o))
        return result
    else:
        result = model
        for key, value in result.items():
            if isinstance(value, datetime):
                model[key] = value.isoformat()
        return result


def get_response_with_pagination(titulo: str, response: dict[str, any], total: int, page: int, limit: int):
    total_pages = (total + limit - 1) // limit

    response = {
        "data": {titulo: response},
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
        },
    }

    return response
