from database import Database


class Ingredient:

    def __init__(self, name, price, kcal, fat, carbs, protein):
        self.name = name
        self.price = price
        self.kcal = kcal
        self.fat = fat
        self.carbs = carbs
        self.protein = protein

    def pushToDatabase(self):

        query = 'SELECT * FROM `ingredient` WHERE 1'
        print(query)
        database = Database(query)
        print(database)
        return database