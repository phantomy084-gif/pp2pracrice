people = {"John": 20, "Alice": 19, "Tedd": 17, "Luna": 23}
people_name = ["Alice" , "John"]

for name, age in people.items():
    if age > 18 and age < 24:
        for i in people_name:
            if i == name:
                print(f"{name} : passed!!")
        