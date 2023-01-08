
class JobRow:
    def __init__(self, soup):
        self.soup = soup

    def find_value(self, tag, class_name):
        element = self.soup.find(tag, class_=class_name, default=None)
        if element:
            subelement = element.find(class_='field-content')
            return subelement.text
        else:
            return None

    @property
    def title(self):
        return self.find_value('span', 'views-field-title')

    @property
    def grade(self):
        return self.find_value('span', 'views-field-field-epso-grade')

    @property
    def domain(self):
        return self.find_value('div', 'views-field-field-epso-domain')

    @property
    def institution(self):
        return self.find_value('span', 'views-field-field-epso-institution')

    @property
    def location(self):
        return self.find_value('span', 'views-field-field-epso-location')

    @property
    def deadline(self):
        return self.find_value('span', 'views-field-field-epso-deadline')
