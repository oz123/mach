from mach import mach1


@mach1
class Calculator:

    def add(self, a: int, b: int):
        """adds two numbers and prints the result"""
        print(a + b)

    def div(self, a: int, b: int):
        """divide one number by the other"""
        print(a / b)


calc = Calculator()

calc.run()
