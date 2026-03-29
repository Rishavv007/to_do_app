from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date
from . import ma
import enum as _enum


class EnumStr(fields.Str):
    """A string field that correctly serializes Python Enum values."""
    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, _enum.Enum):
            return value.value
        return super()._serialize(value, attr, obj, **kwargs)


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, error="Field cannot be blank"))
    description = fields.Str(allow_none=True, load_default=None)
    priority = EnumStr(load_default="MEDIUM", validate=validate.OneOf(["LOW", "MEDIUM", "HIGH"]))
    deadline = fields.Date(allow_none=True, load_default=None)
    status = EnumStr(load_default="PENDING", validate=validate.OneOf(["PENDING", "IN_PROGRESS", "DONE"]))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates("deadline")
    def validate_deadline(self, value):
        if value and value < date.today():
            raise ValidationError("Deadline cannot be in the past.")


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class AISuggestionSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(allow_none=True)
    deadline = fields.Date(allow_none=True, load_default=None)


class AIResponseSchema(Schema):
    priority = fields.Str(load_default="MEDIUM", validate=validate.OneOf(["LOW", "MEDIUM", "HIGH"]))
    subtasks = fields.List(fields.Str(), load_default=list)
