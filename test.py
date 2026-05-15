class Test:
    name = "HELLO"

    def __str__(self):
        return f"This is the 'Test' object with {self.name} name"


test = Test()

print(test)
