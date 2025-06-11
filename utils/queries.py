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