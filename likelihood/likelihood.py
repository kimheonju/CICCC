from model import model

# Calculate probability for a given observation
probability = model.probability([["heavy", "no", "delayed", "miss"]])

print(probability)