from fastapi import Form
from typing import Type
from pydantic import BaseModel

def as_form(cls: Type[BaseModel]):
    new_params = []
    for name, model_field in cls.model_fields.items():
        required = model_field.is_required
        default = model_field.default if not required else ...
        annotation = model_field.annotation

        # Append parameter info to list
        new_params.append((name, annotation, Form(default)))

    # Create as_form function dynamically with these params
    async def _as_form(**data):
        return cls(**data)

    # Set signature dynamically, omitted here for brevity
    # You can import 'signature' and 'Parameter' from 'inspect' if needed

    cls.as_form = _as_form
    return cls
