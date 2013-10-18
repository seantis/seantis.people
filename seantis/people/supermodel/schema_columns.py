from seantis.plonetools import tools
from seantis.people.supermodel import (
    get_selectable_fields, get_table_columns, get_title_fields
)


def get_schema_columns(schema):
    columns = []

    fields_by_columns = (
        fields for ix, fields in sorted(
            tools.invert_dictionary(get_table_columns(schema)).items(),
            key=lambda x: x[0]
        )
    )

    for fields in fields_by_columns:
        columns.append(SchemaColumn(schema, fields))

    return columns


class SchemaColumn(object):

    def __init__(self, schema, fields):
        self.schema = schema
        self.fields = tools.order_fields_by_schema(fields, schema)
        self.titles = [self.schema[field].title for field in self.fields]
        self.contains_title_field = bool(
            set(self.fields) & set(get_title_fields(self.schema))
        )
        self.selectable = (
            len(self.fields) == 1 and self.fields[0] in get_selectable_fields(
                self.schema
            )
        )
