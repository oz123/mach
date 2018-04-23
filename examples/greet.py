from mach import mach1


@mach1
class Hello:

    default = 'greet'

    def greet(self, name: str, count: int = 1):
        if not name:
            name = input('Your name :')

        for c in range(count):
            print("Hello %s" % name)


Hello().run()
