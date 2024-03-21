"""
Shapes and associated methods.
"""

class Shape():
    """The general shape class."""
    def __init__(self, color, name) -> None:
        self.color = color
        self.name = name

    def say_name(self):
        """Return shape greering."""
        return f"My name is {self.name}"

    def get(self):
        """Return color."""
        return f"This is my color: {self.color}"

class Rectangle(Shape):
    """The rectangle class."""
    def __init__(self, color, name, width, height) -> None:
        super().__init__(color, name)
        self.width = width
        self.height = height

    def say_name(self):
        """Return shape greeting."""
        return f"My name is {self.name} and I am a rectangle."

    def area(self):
        """Return shape area."""
        return self.width * self.height

    def perimeter(self):
        """Return shape perimeter."""
        return self.width * 2 + self.height * 2

class Circle(Shape):
    """The circle class."""
    def __init__(self, color, name, radius) -> None:
        super().__init__(color, name)
        self.radius = radius

    def say_name(self):
        """Return shape greeting."""
        return f"My name is {self.name} and I am a circle."

    def area(self):
        """Return shape area."""
        return 3.14 * self.radius**2

    def perimeter(self):
        """Return shape perimeter."""
        return 2 * 3.14 * self.radius
