from seantis.plonetools.setuphandlers import get_sane_index_handler_and_step

add_catalog_indexes, import_indexes = get_sane_index_handler_and_step(
    'seantis.people', [
        ('first_letter', 'FieldIndex')
    ]
)
