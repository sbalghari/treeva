def greet(name):
    return f"Hello, {name}!"


class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


class Greeter:
    def __init__(self, prefix):
        self.prefix = prefix

    def greet(self, name):
        return f"{self.prefix}{name}"


for i in range(10):
    print(i)

x = 0
while x < 5:
    x += 1

if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

try:
    result = 1 / 0
except ZeroDivisionError:
    print("caught")
finally:
    print("done")

raise RuntimeError("boom")
