#task 1
#Make a new list that has all the elements less than 5 from this list in it and print out this new list.

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
#Count the occurrence of each word, and print the word plus the count.

string = 'hi dee hi how are you mr dee'
word_dict = dict()
word_list = string.split(" ")
for word in word_list:
    if word in word_dict.keys():
        word_dict[word] += 1
    else:
        word_dict[word] = 1
for key, val in word_dict.items():
    print(key, val)


#task 4

print("What is your age?")
age = int(input())
print ("You reach retirement in " + str((65 - age)))

#task 5

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



