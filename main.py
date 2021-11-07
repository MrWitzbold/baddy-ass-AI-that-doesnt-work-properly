import random
import math

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", ".", ","]
alphabet_numbers = []

possible_diferences = [-0.7071067811865475, -0.1873204098133684, -0.05425610705059791, -0.02145920209481811, -0.010438175545588346, -0.005813248141223526, -0.00355556982902272, -0.0023283830525012705, -0.0016058579599510514, -0.0011534555363703625, -0.0008560162577146979, -0.0006525517771757139, -0.0005087272567019241, -0.0004042143291536071, -0.00032645802587383255, -0.00026742062627960195, -0.00022179469210725777, -0.0001859800304166992, -0.00015747612709726688, 
-0.0001345095453347822, -0.00011579884659296269, -0.00010040248586218325, -8.761814475988228e-05, -7.691473729243281e-05, -6.788562943738086e-05]

def sigmoid(x):
    result = x/(math.sqrt(1 + x**2))
    if result > 0.99999:
        result = (result-0.99999)*100000
    return result

def unsigmoid(x):
    print("Getting value for: " + str(abs(x)))
    result = x*29
    return result

def return_neurons(file):
    neurons = []
    file_lines = open(file, 'r').readlines()
    for line in file_lines:
        if line.startswith("neuron="):
            neuron = line.split("=")[1]
            neurons.append(neuron)
    return neurons

def return_weights(file):
    weights = []
    file_lines = open(file, 'r').readlines()
    for line in file_lines:
        if line.startswith("weight="):
            weight = line.split("=")[1]
            weights.append(weight)
    return weights

def save_point(file, neurons, weights):
    with open(file, "w") as file:
        for i in range(0, len(neurons)):
            file.write("neuron=" + str(neurons[i]) + "\n")
            file.write("weight=" + str(weights[i]) + "\n")
    file.close()

def setup_file():
    for i in range(0, 52):
        with open("neurons.txt", "a") as file:
            print("Writing")
            neuron_n = sigmoid(random.randint(1, 26))
            file.write("neuron=" + str(neuron_n) + "\n")
            file.write("weight=0.5\n")
    file.close()

def adjust_neurons(neurons, j):
    new_neurons = []
    for i in range(0, len(neurons)):
        new_neurons.append(sigmoid(neurons[i] + j))
    return new_neurons

def get_final_result(neurons, weights, j):
    sum = 0
    amount = 0
    for i in range(0, len(neurons)):
        sum += sigmoid((neurons[i] * weights[i]) + j**2)
        amount += 1
    return sum/amount

def train(file_to_read, neurons, weights, iterations):
    generated_text = ""
    file = open(file_to_read, "r").readlines()
    for i in range(0, iterations):
        line = file[i]
        for j in range(0, len(line)):
            neurons = adjust_neurons(neurons, j)
            current_letter = line[j]
            letter_number = abs((unsigmoid(get_final_result(neurons, weights, j))))
            print(letter_number)
            machine_letter = alphabet[int(round(abs(letter_number-1)))]
            random_difference = possible_diferences[random.randint(0, len(possible_diferences)-1)]
            if current_letter == letter_number:
                weights[random.randint(0, len(weights)-1)] -= random_difference*100
            else:
                weights[random.randint(0, len(weights)-1)] += random_difference*100
            generated_text += machine_letter
        if i+1 >= len(file):
            return generated_text
    return generated_text

    
# 52 neurons, 2 for each letter
# converge the into a single number
# have each neuron have a weight (sigmoidded) to multiply by at the end, then take an average of them
# if wrong then tweak a little to positive, if right tweak a little to negative

for i in range(0, len(alphabet)):
    alphabet_numbers.append(i)

first_time = False
try:
    file_r = open("neurons.txt", "r")
    file_r.close()
except Exception as e:
    first_time = True

if first_time:
    setup_file()

neurons = return_neurons("neurons.txt")
weights = return_weights("neurons.txt")

neurons_aux = []
weights_aux = []

for i in range(0, len(neurons)):
    neurons_aux.append(float(neurons[i].replace("\n", "")))
    weights_aux.append(float(weights[i].replace("\n", "")))

neurons = neurons_aux
weights = weights_aux

print(neurons)
print(weights)

generated_text = train("book_to_read.txt", neurons, weights, 50000)
save_point("neurons.txt", neurons, weights)
print(generated_text)
