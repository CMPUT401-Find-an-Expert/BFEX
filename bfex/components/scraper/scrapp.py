class Scrapp(object):
    def __init__(self):
        self.data_source = ""
        self.formated_name = ""
        self.title = ""
        self.text = ""
        self.date = ""
        self.meta_data = {}

    def set_name(self, name):
        self.formated_name = name

    def set_source(self, data_source):
        self.data_source = data_source

    def set_title(self, title):
        self.title = title

    def set_text(self, text):
        self.text = text

    def set_date(self, date):
        self.date = date

    def add_meta(self, attr, meta):
        self.meta_data[attr] = meta
