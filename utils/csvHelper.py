# -*- coding: utf-8 -*-
import csv
import io
import sys

def dictionaryListToCsv(dict_list, file_name):
    if not dict_list:
        raise ValueError("The input dictionary list cannot be empty.")

    fieldnames = dict_list[0].keys()

    class UnicodeWriter:
        def __init__(self, f, dialect=csv.excel, **kwds):
            self.queue = io.BytesIO()
            self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
            self.stream = f

        def writerow(self, row):
            self.writer.writerow([s.encode("utf-8") if isinstance(s, unicode) else unicode(s).encode("utf-8") for s in row])
            data = self.queue.getvalue()

            self.stream.write(data)
            self.queue.truncate(0)
            self.queue.seek(0)

        def writerows(self, rows):
            for row in rows:
                self.writerow(row)

    class UnicodeDictWriter:
        def __init__(self, f, fieldnames, restval="", extrasaction="raise", dialect=csv.excel, *args, **kwds):
            self.writer = UnicodeWriter(f, dialect=dialect, *args, **kwds)
            self.fields = fieldnames
            self.restval = restval
            self.extrasaction = extrasaction

        def writeheader(self):
            header = dict(zip(self.fields, self.fields))
            self.writer.writerow([unicode(header.get(k, "")) for k in self.fields])


        def writerow(self, rowdict):
            output_row = []
            for field in self.fields:
                value = rowdict.get(field, self.restval)

                if not isinstance(value, unicode):
                    value = unicode(value)
                output_row.append(value)
            self.writer.writerow(output_row)

    try:
        with open(file_name, 'wb') as csvfile:
            writer = UnicodeDictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row_dict in dict_list:
                writer.writerow(row_dict)

        print("CSV file {} created successfully in the current directory.".format(file_name))
    except IOError as e:
        print("Error writing CSV file {}: {}".format(file_name, e))
        raise
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))
        raise
