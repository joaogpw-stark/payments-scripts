from datetime import datetime
from google.cloud import datastore
from utils.csvHelper import dictionaryListToCsv
from utils.currency import format_to_brazilian_currency
from models.filter import FilterModel
from utils.queries import queryByKindPaginated
import datetime


fileName = "shipping-requests-amount.csv"
_project = "api-ms-edi"
_environment = "production"
_kind = "ShippingRequest"
_filters = [
    FilterModel("action", "=", "create"),
    FilterModel("bank", "=", "itau"),
    FilterModel("type", "=", "charge-payment"),
]


client = datastore.Client("{project}{environmentTermination}".format(
    project=_project,
    environmentTermination={
        "development": "-dev",
        "sandbox": "-sbx",
        "production": "",
    }[_environment],
))

dictList = queryByKindPaginated(_kind, _filters, client)

dictionaryListToCsv(dictList, fileName)
