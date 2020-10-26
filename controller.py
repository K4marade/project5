from model import Model
from view import View
from database import Database
from constants import DB_NAME


class Controller:
    """Class that defines the interactions between the View, Model and Database"""

    def __init__(self):
        """Class constructor"""

        self.view = View()
        self.model = Model()
        self.database = Database()

    def pre_process(self):

        self.database.create_database()
        self.database.create_tables()
        categories = self.model.get_categories()
        self.database.insert_categories(categories)
        aliments = self.model.get_aliments(categories)
        for cat, elements in aliments.items():
            aliments[cat] = self.clean_data(elements)
        for cat, elements in aliments.items():
            self.database.insert_aliments(elements)
        for cat, elements in aliments.items():
            self.database.insert_associated(cat, elements)

    def clean_data(self, aliments):
        """
            Method that...
        """
        lst_data = []
        for aliment in aliments:
            for products in aliment['products']:
                valid_tag = ["product_name_fr", "nutriscore_grade", "url", "stores"]
                if not all(tag in products for tag in valid_tag):
                    pass
                else:
                    if products['product_name_fr'] != '':
                        data = [products['code'], products['product_name_fr'], products['nutriscore_grade'],
                                products['url'],
                                products['stores']]
                        lst_data.append(data)
        return lst_data

    def process(self):
        """Method that defines all the program's process"""
        DB = self.database.is_database_created()
        if DB is None:
            self.pre_process()
        else:
            pass

        scenario = self.view.choose_scenario()
        if scenario == '1':
            self.get_substitute()
        elif scenario == '2':
            self.get_saved_aliments()
        elif scenario == '3':
            self.database.close_cursor()
            quit(print("Bye"))

    def get_substitute(self):
        """Method that gets a substitute aliment with a better nutriscore"""

        categories = self.database.select_categories()
        category = self.view.choose_category(categories)

        aliments = self.database.select_aliments(category)
        aliment = self.view.choose_aliment(aliments)

        nutriscore = self.database.select_nutriscore(aliment)
        substitute = self.database.select_substitute(category, nutriscore)  # nutriscore)

        choice = self.view.display_substitute(aliment, substitute)
        if choice == '1':
            self.database.insert_substitute(aliment, substitute)
            self.process()
        elif choice == '2':
            self.process()
        elif substitute is None:
            self.process()

    def get_saved_aliments(self):
        substitute = self.database.select_saved_substitutes()
        self.view.display_saved_substitute(substitute)
        self.process()
