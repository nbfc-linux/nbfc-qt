from collections import OrderedDict

class MyTableFieldDefinition:
    def __init__(self, name):
        self.name = name
        self.display = lambda v: str(v)
        self.default = None
        self.types = (str,)
        self.validate = lambda v: True

    def setDisplay(self, display):
        self.display = display

    def setDefault(self, default):
        self.default = default

    def setTypes(self, types):
        self.types = types

    def setValidate(self, callback):
        self.validate = callback

class MyTableWidget(QTableWidget):
    def __init__(self, *a):
        super().__init__(*a)
        self.fields = []
        self.flag_callback = lambda flags: flags

    def setColumnFields(self, fields):
        self.fields = fields

    def setItemFlagCallback(self, callback):
        self.flag_callback = callback

    def set_row_defaults(self, row):
        for column_id, field in enumerate(self.fields):
            item = QTableWidgetItem(field.display(field.default))
            item.setData(Qt.UserRole, field.default)
            item.setFlags(self.flag_callback(item.flags()))
            self.setItem(row, column_id, item)

    def update_row(self, row, dictionary):
        errors = []

        for column_id, field in enumerate(self.fields):
            if field.name in dictionary:
                if not isinstance(dictionary[field.name], field.types):
                    errors.append((field.name, TypeError))
                elif not field.validate(dictionary[field.name]):
                    errors.append((field.name, ValueError))
                else:
                    item = QTableWidgetItem(field.display(dictionary[field.name]))
                    item.setData(Qt.UserRole, dictionary[field.name])
                    item.setFlags(self.flag_callback(item.flags()))
                    self.setItem(row, column_id, item)
            else:
                errors.append((field.name, KeyError))

        return errors 

    def get_row_as_dict(self, row):
        r = OrderedDict()

        for column_id, field in enumerate(self.fields):
            r[field.name] = self.item(row, column_id).data(Qt.UserRole)

        return r

    def swap_rows(self, row1, row2):
        row1_items = [self.takeItem(row1, i) for i in range(self.columnCount())]
        row2_items = [self.takeItem(row2, i) for i in range(self.columnCount())]

        for column, item in enumerate(row1_items):
            self.setItem(row2, column, item)

        for column, item in enumerate(row2_items):
            self.setItem(row1, column, item)

    def get_selected_row(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return None

        return selected_items[0].row()

    def move_row_up(self):
        row = self.get_selected_row()
        if row is None or row == 0:
            return

        self.swap_rows(row, row - 1)
        self.selectRow(row - 1)

    def move_row_down(self):
        row = self.get_selected_row()
        if row is None or row == self.rowCount() - 1:
            return

        self.swap_rows(row, row + 1)
        self.selectRow(row + 1)

    def remove_selected_row(self):
        row = self.get_selected_row()
        if row is None:
            return

        self.removeRow(row)
