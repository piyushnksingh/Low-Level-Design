# class Shape:
#     def area(self):
#         raise NotImplementedError
#
#     def volume(self):
#         raise NotImplementedError  # 2D shapes don't need this!
#
#
# class Square(Shape):
#     def __init__(self, side):
#         self.side = side
#
#     def area(self):
#         return self.side * self.side
#
#     def volume(self):
#         raise Exception("Volume not applicable for Square")  # Unnecessary method
#
#
# class Rectangle(Shape):
#     def __init__(self, length, width):
#         self.length = length
#         self.width = width
#
#     def area(self):
#         return self.length * self.width
#
#     def volume(self):
#         raise Exception("Volume not applicable for Rectangle")  # Unnecessary method
#
#
# class Cube(Shape):
#     def __init__(self, side):
#         self.side = side
#
#     def area(self):
#         return 6 * self.side * self.side
#
#     def volume(self):
#         return self.side ** 3
#
#
# def main():
#     square = Square(5)
#     rectangle = Rectangle(4, 6)
#     cube = Cube(3)
#
#     print("Square Area:", square.area())
#     print("Rectangle Area:", rectangle.area())
#     print("Cube Area:", cube.area())
#     print("Cube Volume:", cube.volume())
#
#     try:
#         print("Square Volume:", square.volume())  # Will raise an exception
#     except Exception as e:
#         print("Exception:", str(e))
#
#
# if __name__ == "__main__":
#     main()



# ------------------------------------------------- ISP FOLLOWED -----------------------------------------

class TwoDimensionalShape:
    def area(self):
        raise NotImplementedError


class ThreeDimensionalShape(TwoDimensionalShape):
    def volume(self):
        raise NotImplementedError


# Square implements only the 2D interface
class Square(TwoDimensionalShape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side


# Rectangle implements only the 2D interface
class Rectangle(TwoDimensionalShape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


# Cube implements the 3D interface
class Cube(ThreeDimensionalShape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return 6 * self.side * self.side

    def volume(self):
        return self.side ** 3


def main():
    square = Square(5)
    rectangle = Rectangle(4, 6)
    cube = Cube(3)

    print("Square Area:", square.area())
    print("Rectangle Area:", rectangle.area())
    print("Cube Area:", cube.area())
    print("Cube Volume:", cube.volume())


if __name__ == "__main__":
    main()