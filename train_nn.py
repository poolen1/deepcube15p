import create_training


data_generator = create_training.CreateTrainingSet()
data_set = data_generator.create_sets(100, 100)

# print(data_set)

print("sets: ", len(data_set))

length = 0
for sets in data_set:
    length += len(sets)
print("samples: ", length)
