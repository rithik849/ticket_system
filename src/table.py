
class Table:

    def __init__(self):
        self.fields = []
        self.records = []

    def clear(self):
        self.fields = []
        self.records = []

    def set_fields(self, fields):
        self.fields = fields

    def set_records(self, records):
        self.records = records

    def print_table(self):
        spacing = ""

        row_spacing = {}
        index = 0

        for field in self.fields:
            row_spacing[field] = len(field)
            for record in self.records:
                if row_spacing[field] < len(str(record[index])):
                    row_spacing[field] = len(str(record[index]))

        for size in row_spacing.values():
            spacing += "{:<" + str(size+10) + "} "

        print(spacing.format(*self.fields))

        for record in self.records:
            print(spacing.format(*record))