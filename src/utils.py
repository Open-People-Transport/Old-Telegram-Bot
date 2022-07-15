import json
from typing import Optional, Type, TypeVar

import requests
from pygraphic import GQLParameters, GQLQuery

QueryType = TypeVar("QueryType", bound=GQLQuery)


def request_query_parse_response(
    Query: Type[QueryType], parameters: Optional[GQLParameters] = None
) -> QueryType:
    query = Query.get_query_string()
    variables = parameters.dict(by_alias=True) if parameters else None
    data = {"query": query, "variables": variables}
    try:
        response = requests.post(
            "http://127.0.0.1:8000/graphql",
            data=json.dumps(data, default=str),
            headers={"Content-Type": "application/json"},
        )
        response_json = response.json()
        if errors := response_json.get("errors"):
            raise Exception(errors)
        result = Query.parse_obj(response_json["data"])
        return result
    except Exception as err:
        raise


_blank_data_counter = 0


def get_unique_blank():
    global _blank_data_counter
    _blank_data_counter += 1
    return f"blank {_blank_data_counter}"
