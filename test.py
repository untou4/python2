a='Сусов Роман vaa @ya'

if a.find('via')!= None:
    a = a[:a.find('via')].strip()
print(a)