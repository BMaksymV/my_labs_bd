from typing import Generic, TypeVar
from my_project import db

ModelT = TypeVar("ModelT", bound=db.Model)


class BaseDAO(Generic[ModelT]):
    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    def find_all(self) -> list[ModelT]:
        return db.session.query(self.model).all()

    def find_by_id(self, entity_id: int) -> ModelT | None:
        return db.session.get(self.model, entity_id)

    def create(self, entity: ModelT) -> ModelT:
        db.session.add(entity)
        db.session.commit()
        db.session.refresh(entity)
        return entity

    def update(self, entity: ModelT, data: dict) -> ModelT:
        for key, value in data.items():
            setattr(entity, key, value)
        db.session.commit()
        db.session.refresh(entity)
        return entity

    def delete(self, entity: ModelT) -> None:
        db.session.delete(entity)
        db.session.commit()
