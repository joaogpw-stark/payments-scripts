from re import sub

def queryByKind(kind, filters, client):
    query = client.query(
        kind=kind,
    )

    for filter in filters:
        query.add_filter(filter.key, filter.operator, filter.value)

    dictList = []
    for entity in query.fetch():
        dictList.append(dict(entity))

    return dictList


def _queryPage(kind, filters, batch_size, client, start_cursor=None):
    query = client.query(kind=kind)
    for f in filters:
        query.add_filter(f.key, f.operator, f.value)

    cursor_bytes = start_cursor.encode("utf-8") if start_cursor else None

    iterator = query.fetch(limit=batch_size, start_cursor=cursor_bytes)

    try:
        page = next(iterator.pages)
        entities = list(page)
    except StopIteration:
        entities = []

    next_cursor_bytes = iterator.next_page_token
    next_cursor_str = next_cursor_bytes.decode("utf-8") if next_cursor_bytes else None

    results = [dict(entity) for entity in entities]

    return results, next_cursor_str

def queryByKindPaginated(kind, filters, datastoreClient):
    dictList = []
    current_cursor = None

    while True:
        page_results, next_cursor = _queryPage(
            kind,
            filters,
            1000,
            datastoreClient,
            start_cursor=current_cursor
        )

        dictList.extend(page_results)

        if not next_cursor:
            break

        current_cursor = next_cursor

    return dictList
