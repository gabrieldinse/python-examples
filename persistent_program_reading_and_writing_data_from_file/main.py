import os

try:
    fout = open('output.txt', 'w')
except:
    print('lol deu errado bro kkkk')
    

num1 = int(1.02)
num2 = 2.013
str1 = 'lol'
line = 'conteudo: ' + '%d, %g e \'%s\'' % (num1, num2, str1) 
fout.write(line)
fout.close()