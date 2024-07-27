# Function to convert from numbers to Emoji Numbers:
def to_emoji(input):
  arr = ["0","1","2","3","4","5","6","7","8","9"]
  #arr = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
  working = [*map(int,str(input))]
  answer = []
  for i in range(len(working)):
    temp1 = working[i]
    temp = arr[temp1]
    answer.append(temp)
  list = ''.join(answer)
  if len(list)<5:
    #list = "0"+str(list)
    #list = "0️⃣ "+str(list)
    pass
  return list

