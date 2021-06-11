from UI import UI


class Table(UI):

    def __init__(self):
        super().__init__()
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
            index += 1

        for size in row_spacing.values():
            spacing += "{:<" + str(size+10) + "} "

        self.style_print(spacing.format(*self.fields), "g*")

        for record in self.records:
            self.style_print(spacing.format(*record), "t")


