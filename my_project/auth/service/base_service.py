from typing import Any, Generic, TypeVar
from marshmallow import Schema
from my_project.auth.dao.base_dao import BaseDAO
from my_project.utils.exceptions import NotFoundError, ValidationError

ModelT = TypeVar("ModelT")


class BaseService(Generic[ModelT]):
    def __init__(
        self,
        dao: BaseDAO[ModelT],
        schema: Schema,
        entity_name: str,
    ) -> None:
        self.dao = dao
        self.schema = schema
        self.entity_name = entity_name

    def get_all(self) -> list[ModelT]:
        return self.dao.find_all()

    def get_by_id(self, entity_id: int) -> ModelT:
        entity = self.dao.find_by_id(entity_id)
        if entity is None:
            raise NotFoundError(f"{self.entity_name} with id={entity_id} not found")
        return entity

    def validate_business_rules(
        self,
        data: dict[str, Any],
        existing: ModelT | None = None,
    ) -> None:
        pass

    def create(self, raw_data: dict[str, Any]) -> ModelT:
        validated = self.schema.load(raw_data)
        self.validate_business_rules(validated, existing=None)
        entity = self.dao.model(**validated)
        return self.dao.create(entity)

    def update(self, entity_id: int, raw_data: dict[str, Any]) -> ModelT:
        if not raw_data:
            raise ValidationError("At least one field must be provided for update")
        entity = self.get_by_id(entity_id)
        validated = self.schema.load(raw_data, partial=True)
        self.validate_business_rules(validated, existing=entity)
        return self.dao.update(entity, validated)

    def delete(self, entity_id: int) -> None:
        entity = self.get_by_id(entity_id)
        self.dao.delete(entity)
