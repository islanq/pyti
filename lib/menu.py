from collections import namedtuple

MenuItem = namedtuple('MenuItem', ['name', 'description', 'func'])

class Menu:
    def __init__(self, title):
        self.title = title
        self.categories = []

    def register_category(self, category):
        self.categories.append(category)

    def display(self):
        while True:  # Keep displaying the menu until 'Exit' is chosen
            print("\n--- {} ---".format(self.title))
            for i, category in enumerate(self.categories, 1):
                print("{}. {} - {}".format(i, category.name, category.description))

            print("{}. Exit".format(len(self.categories) + 1))

            choice = int(input("Choose an option: "))
            if choice == len(self.categories) + 1:
                return "Exit"
            else:
                selected_category = self.categories[choice - 1]
                selected_category.display()


class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []

    def register_item(self, item):
        self.items.append(item)

    def display(self):
        while True:  # Keep displaying the category until 'Back' is chosen
            print("\n--- {} ---".format(self.name))
            for i, item in enumerate(self.items, 1):
                print("{}. {} - {}".format(i, item.name, item.description))

            print("{}. Back".format(len(self.items) + 1))

            choice = int(input("Choose an option: "))
            if choice == len(self.items) + 1:
                return  # Return to the previous menu
            else:
                selected_item = self.items[choice - 1]
                selected_item.func()

class CategoryItem:
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func

def example_func():
    print("Example function executed.")







# Define categories and items within "Linear Algebra"
linear_algebra_menu = Menu("Linear Algebra")

# Vectors category
vectors = Category("Vectors", "Operations and properties of vectors")
vectors.register_item(MenuItem("Vector Operations", "Addition, Scalar Multiplication", example_func))
vectors.register_item(MenuItem("Dot Product", "Calculate dot product", example_func))
vectors.register_item(MenuItem("Cross Product", "Calculate cross product", example_func))
vectors.register_item(MenuItem("Vector Projections", "Find projections of vectors", example_func))

# Matrices category
matrices = Category("Matrices", "Operations and properties of matrices")
matrices.register_item(MenuItem("Matrix Operations", "Addition, Multiplication", example_func))
matrices.register_item(MenuItem("Determinants", "Calculate determinants", example_func))
matrices.register_item(MenuItem("Inverses", "Find matrix inverses", example_func))
matrices.register_item(MenuItem("Transpose", "Find the transpose of a matrix", example_func))

# Registering the categories
linear_algebra_menu.register_category(vectors)
linear_algebra_menu.register_category(matrices)

# Display the main Linear Algebra menu to show the categories and items
# For demonstration purposes, let's display only the "Vectors" and "Matrices" categories and their items

linear_algebra_menu.display()  # Uncomment this line to run the menu (requires interactive session)

#print("Linear Algebra menu, categories, and items are set up. Uncomment the last line to run in an interactive session.")
# def main():
#     main_menu = Menu("Main Menu")

#     category1 = Category("Category 1", "First Category")
#     category2 = Category("Category 2", "Second Category")

#     item1 = CategoryItem("Option 1", "Description 1", example_func)
#     item2 = CategoryItem("Option 2", "Description 2", example_func)

#     category1.register_item(item1)
#     category1.register_item(item2)

#     main_menu.register_category(category1)
#     main_menu.register_category(category2)

#     while True:
#         result = main_menu.display()
#         if result == "Exit":
#             break

# if __name__ == "__main__":
#     main()
