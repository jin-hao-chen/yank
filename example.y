import mymodule

fun add(a, b) {
    let sum = a + b
    return sum
}

a = 10
b = 20
sum = add(a, b)

print("Sum is " + sum.str())

msg = "This is darling3"
print(msg)

users = ["foo", "bar"]
scores = {"foo": 91, "bar": 88}
print(users)
print(scores)


# This is comments
# Define Class

class Person {
    let name;
    let age;
    
    +new(self, name, age) {
        self.name = name
        self.age = age
    }
    
    say(self, words) {
        print(words)
    }
}

print('Hello world!')
