import matrix as m


A = m.matData(3,5,[[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]])
B = m.matData(5,2,[[1,2],[3,4],[5,6],[7,8],[9,10]])
C = A*B
print(A)
print(B)
print(C)