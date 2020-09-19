#!/usr/bin/env python3
#https://github.com/LeahKuhn/BCH5884

import math

Ax, Ay = input("Please input the x and y-coordinates for point A separated by a space: ").split()
Ax = int(Ax)
Ay = int(Ay)

Bx, By = input("Please input the x and y-coordinates for point B separated by a space: ").split()
Bx = int(Bx)
By = int(By)

Cx, Cy = input("Please input the x and y-coordinates for point C separated by a space: ").split()
Cx = int(Cx)
Cy = int(Cy)

#print(type(Ax))
print("A: (",Ax,",",Ay,")"," B: (",Bx,",",By,")"," C: (",Cx,",",Cy,")", sep='' )

#Determine square of length of all sides
a_sq = (Bx - Cx)**2 + (By - Cy)**2
b_sq = (Ax - Cx)**2 + (Ay - Cy)**2
c_sq = (Ax - Bx)**2 + (Ay - By)**2

#print("a**2 = ", a_sq, "b**2 = ", b_sq, "c**2 = ", c_sq)

# Length of all sides
a = math.sqrt(a_sq)
b = math.sqrt(b_sq)
c = math.sqrt(c_sq)

#print("a:", a, "b:", b, "c:", c)

# Law of Cosines
alpha = math.degrees(math.acos((b_sq + c_sq - a_sq) / (2 * b * c)))
beta = math.degrees(math.acos((c_sq + a_sq - b_sq) / (2 * c * a)))
gamma = 180 - (alpha + beta)

alpha = round(alpha, 2)
beta = round(beta, 2)
gamma = round(gamma, 2)

print("alpha =", alpha, "\nbeta =", beta, "\ngamma =", gamma)


print("Done!")