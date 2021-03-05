#task 1

lst = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
lst2 = list()

for i in lst:
    if i < 5:
        lst2.append(i)

print(lst2)


#task 2

list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']

print((list(set(list_a) & set(list_b)))) #items present in both lists
print((list(set(list_a) ^ set(list_b)))) #items present which does not overlap


#task 3

string = 'hi dee hi how are you mr dee'
print(len(set(string.split(" "))))


#task 4

print("What is your age?")
age = int(input())
print ("You reach retirement in " + str((65 - age)))

task 5

letter_scores = {
    "aeioulnrst": 1,
    "dg": 2,
    "bcmp": 3,
    "fhvwy": 4,
    "k": 5,
    "jx": 8,
    "qz": 10
}
counter = 0
print('Write a word')
word = input()
lst = list()
for key, value in letter_scores.items():
    letter_group = key
    for letter in letter_group:
        for i in word:
            if i == letter:
                counter += value
print(counter)



