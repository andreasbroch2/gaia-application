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
        query = 'INSERT INTO `ingredient`(`name`, `price`, `kcal`, `fat`, `carbs`, `protein`) VALUES ("{}", {}, {}, {}, {}, {})'.format(self.name, self.price, self.kcal, self.fat, self.carbs, self.protein)
        print(query)
        database = Database()
        database.insert(query)
        print(database)
        return database