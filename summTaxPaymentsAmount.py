from datetime import datetime
from google.cloud import datastore
from utils.csvHelper import dictionaryListToCsv
from utils.currency import format_to_brazilian_currency
from models.filter import FilterModel
from utils.queries import queryByKind
import datetime


fileName = "tax-payments-entities.csv"
_project = "api-ms-tax-payment"
_environment = "production"
_filters = [
    FilterModel("created", ">", datetime.datetime(2025, 6, 9, 14, 10, 00, 00)),
    FilterModel("created", "<", datetime.datetime(2025, 6, 11, 14, 10, 00, 00)),
]


client = datastore.Client("{project}{environmentTermination}".format(
    project=_project,
    environmentTermination={
        "development": "-dev",
        "sandbox": "-sbx",
        "production": "",
    }[_environment],
))


barcodeResults = queryByKind("BarCodePayment", _filters, client)
darfResults = queryByKind("DarfPayment", _filters, client)

dictList = barcodeResults + darfResults

summ = 0
for payment in dictList:
    summ += int(payment["amount"])

print("TOTAL {kind} AMOUNT: {amount}".format(
    amount=format_to_brazilian_currency(summ),
    kind=_kind
))

dictionaryListToCsv(dictList, fileName)
