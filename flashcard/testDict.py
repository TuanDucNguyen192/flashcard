# # python
# # Tạo list các dictionary
# flashcards = [
#     {'say': 'noi', 'do': 'lam'}
# ]

# list1 = ["mot", "hai", "ba"]
# list2 = ["one", "two", "three"]

# for i in range(len(list1)):
#     new_card = {list1[i]: list2[i]}
#     flashcards.append(new_card)

# print(flashcards[2])  # {'say': 'noi', 'do': 'lam'}

data = [{"ten": "Nam"}, {'say': 'noi', 'do': 'lam'}]
output = list(data[0].keys())
print(output[0])
# for i in data[0].keys():
#     print(i)


