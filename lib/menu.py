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


class Menu2:
    def __init__(self, title):
        self.title = title
        self.categories = []
        self.current_page = 0

    def register_category(self, category):
        self.categories.append(category)

    def display(self):
        while True:
            print("\n--- {} ---".format(self.name))
            start_idx = self.current_page * 7
            end_idx = min(start_idx + 7, len(self.items))

            for i, item in enumerate(self.items[start_idx:end_idx], start_idx + 1):
                print("{}. {} - {}".format(i, item.name, item.description))
            
            extra_options_start = len(self.items) if end_idx >= len(self.items) else end_idx + 1

            if end_idx < len(self.items):
                print(f"{extra_options_start}. Next")
                extra_options_start += 1
            
            print(f"{extra_options_start}. Back")

            choice = int(input("Choose an option: ")) - start_idx - 1
            
            if choice in [7, 6] and end_idx < len(self.items):
                self.current_page = (self.current_page + 1) % ((len(self.items) + 6) // 7)
            elif choice in [7, 6]:
                self.current_page = (self.current_page - 1) % ((len(self.items) + 6) // 7)
            elif choice in [6, 5]:
                return  # Return to the previous menu
            else:
                selected_item = self.items[start_idx + choice]
                selected_item.func()
                self.current_page = 0


class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.current_page = 0

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
vectors = Category("Vectors", "Operations and properties of vectors")# Registering the categories


vectors.register_item(MenuItem("Vector Operations", "Addition, Scalar Multiplication", example_func))
vectors.register_item(MenuItem("Dot Product", "Calculate dot product", example_func))
vectors.register_item(MenuItem("Cross Product", "Calculate cross product", example_func))
vectors.register_item(MenuItem("Vector Projections","Find projections of vectors", example_func))

# Matrices category
matrices = Category("Matrices", "Operations and properties of matrices")

matrices.register_item(MenuItem("Matrix Operations", "Addition, Multiplication", example_func))
matrices.register_item(MenuItem("Determinants", "Calculate determinants", example_func))
matrices.register_item(MenuItem("Inverses", "Find matrix inverses", example_func))
matrices.register_item(MenuItem("Transpose1", "Find the transpose of a matrix", example_func))
matrices.register_item(MenuItem("Transpose2", "Find the transpose of a matrix", example_func))
matrices.register_item(MenuItem("Transpose3", "Find the transpose of a matrix", example_func))
matrices.register_item(MenuItem("Transpose4", "Find the transpose of a matrix", example_func))
matrices.register_item(MenuItem("Transpose5", "Find the transpose of a matrix", example_func))
matrices.register_item(MenuItem("Transpose6", "Find the transpose of a matrix", example_func))
matrices.register_item(MenuItem("Transpose7", "Find the transpose of a matrix", example_func))
linear_algebra_menu.register_category(vectors)
linear_algebra_menu.register_category(matrices)
linear_algebra_menu.display()

