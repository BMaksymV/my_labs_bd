from typing import Any
from flask import jsonify, request
from marshmallow import Schema
from my_project.auth.service.base_service import BaseService
from my_project.utils.exceptions import BadRequestError, ValidationError


def get_json_body(allow_empty: bool = False) -> dict[str, Any]:
    data = request.get_json(silent=True)
    if data is None:
        if allow_empty and (not request.data or not request.data.strip()):
            return {}
        raise BadRequestError("Request body must be a valid JSON object")
    if not isinstance(data, dict):
        raise BadRequestError("Request body must be a JSON object")
    if not allow_empty and not data:
        raise ValidationError("Request body cannot be empty")
    return data


class BaseCRUDController:
    def __init__(self, service: BaseService, schema_cls: type[Schema]) -> None:
        self.service = service
        self.dto = schema_cls()
        self.dtos = schema_cls(many=True)

    def get_all(self):
        items = self.service.get_all()
        return jsonify(self.dtos.dump(items)), 200

    def get_by_id(self, entity_id: int):
        item = self.service.get_by_id(entity_id)
        return jsonify(self.dto.dump(item)), 200

    def create(self):
        data = get_json_body()
        item = self.service.create(data)
        return jsonify(self.dto.dump(item)), 201

    def update(self, entity_id: int):
        data = get_json_body()
        item = self.service.update(entity_id, data)
        return jsonify(self.dto.dump(item)), 200

    def delete(self, entity_id: int):
        self.service.delete(entity_id)
        return "", 204
