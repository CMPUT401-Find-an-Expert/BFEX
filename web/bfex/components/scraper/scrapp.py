class Scrapp(object):
    """This is the data structure of everything we scrape from a website.

       A professor will have multiple scrapps since each scrapp comes from a
       different source. This class is mostly full of getters and setters
    """
    def __init__(self):
        self.data_source = ""
        self.formated_name = ""
        self.title = ""
        self.text = ""
        self.date = ""
        self.meta_data = {}

    def set_name(self, name):
        """ :param name: formatted name of the faculty memeber.
            :return: none
        """
        self.formated_name = name

    def set_source(self, data_source):
        """ TODO: perhaps enumerate this?
            :param data_source: where we show what source we got the scrapp from.
            :return: none
        """
        self.data_source = data_source

    def set_title(self, title):
        """ :param title: title of the abstract/paper/body we grab.
            :return: none
        """
        self.title = title

    def set_text(self, text):
        """ :param text: huge amount of text that we get from the websites.
            :return: none
        """
        self.text = text

    def set_date(self, date):
        """ :param date: date we pull from the article.
            :return: none
        """
        self.date = date

    def add_meta(self, attr, meta):
        """ :param attr: the new/unique attribute we want to save to the scrapp.
            :param meta: the info of that attribute.
            :return: none
        """
        self.meta_data[attr] = meta
