# from typing import Type, List, Optional, TypeVar
# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from pydantic import BaseModel

# T = TypeVar('T')  # A type variable for the model

# class CRUDBase:
#     def __init__(self, model: Type[T]):
#         self.model = model

#     def get(self, db: Session, obj_id: int) -> Optional[T]:
#         """ Get a single record by ID """
#         return db.query(self.model).filter(self.model.id == obj_id).first()

#     def get_list(self, db: Session, skip: int = 0, limit: int = 10) -> List[T]:
#         """ Get a list of records with pagination """
#         return db.query(self.model).offset(skip).limit(limit).all()

#     def create(self, db: Session, obj_in: BaseModel) -> T:
#         """ Create a new record """
#         db_obj = self.model(**obj_in.dict())
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def update(self, db: Session, obj_id: int, obj_in: BaseModel) -> Optional[T]:
#         """ Update an existing record by ID """
#         db_obj = db.query(self.model).filter(self.model.id == obj_id).first()
#         if not db_obj:
#             raise HTTPException(status_code=404, detail="Item not found")

#         for key, value in obj_in.dict(exclude_unset=True).items():
#             setattr(db_obj, key, value)

#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

#     def delete(self, db: Session, obj_id: int) -> Optional[T]:
#         """ Delete a record by ID """
#         db_obj = db.query(self.model).filter(self.model.id == obj_id).first()
#         if not db_obj:
#             raise HTTPException(status_code=404, detail="Item not found")

#         db.delete(db_obj)
#         db.commit()
#         return db_obj
