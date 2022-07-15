import json
from typing import Optional, Type, TypeVar

import requests
from pygraphic import GQLParameters, GQLQuery

QueryType = TypeVar("QueryType", bound=GQLQuery)


def request_query_parse_response(
    Query: Type[QueryType], parameters: Optional[GQLParameters] = None
) -> QueryType:
    query = Query.get_query_string()
    query = query.replace("String", "String!")
    variables = parameters.dict() if parameters else None
    data = {"query": query, "variables": variables}
    try:
        response = requests.post(
            "http://127.0.0.1:8000/graphql",
            data=json.dumps(data, default=str),
            headers={"Content-Type": "application/json"},
        )
        result = Query.parse_obj(response.json()["data"])
        return result
    except Exception as err:
        raise


_blank_data_counter = 0


def get_unique_blank():
    global _blank_data_counter
    _blank_data_counter += 1
    return f"blank {_blank_data_counter}"
