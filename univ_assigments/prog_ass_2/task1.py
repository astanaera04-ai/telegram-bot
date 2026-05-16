st_scores = []
a  = int(input("Qansha student: "))
s = 0;

for i in range(a):
    b = int(input())
    s += b
    st_scores.append(b)
print("print the average" , s / a)

print("maximum value:" , max(st_scores))

print("minimum  value:" , min(st_scores))

s2 = 0
for i in range(a):
    if (st_scores[i] > s / a):
        s2 +=1
print("greater than the average :" , s2)