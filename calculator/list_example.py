
# Creating a list
my_list = [1, 2, 3, "apple", "banana"]

# Accessing elements
print("First element:", my_list[0])
print("Last element:", my_list[-1])

# Slicing a list
print("Slicing:", my_list[1:4])

# Modifying a list
my_list[0] = "new value"
print("Modified list:", my_list)

# Adding elements
my_list.append("orange")
print("Appended list:", my_list)

# Inserting elements
my_list.insert(2, "grape")
print("Inserted list:", my_list)

# Removing elements
my_list.remove("banana")
print("Removed list:", my_list)

# List length
print("List length:", len(my_list))

# Iterating through a list
print("Iterating through the list:")
for item in my_list:
    print(item)
