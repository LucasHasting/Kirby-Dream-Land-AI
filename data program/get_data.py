'''
Name: Lucas Hasting
Date: 11/20/2024

Source: https://datacrystal.tcrf.net/wiki/Kirby%27s_Dream_Land/RAM_map
'''

screen = 49152 # screen begining address

i = 1
cont = screen

file = ""
file += '{\n\t"info": {\n'

#screen info
while(i < 40):
    file += '\t\t"screen' + str(i) + '_0": {\n\t\t\t"address": ' + str(cont) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
    file += '\t\t"screen' + str(i) + '_1": {\n\t\t\t"address": ' + str(cont+1) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
    file += '\t\t"screen' + str(i) + '_2": {\n\t\t\t"address": ' + str(cont+2) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
    file += '\t\t"screen' + str(i) + '_3": {\n\t\t\t"address": ' + str(cont+3) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
    i += 1
    cont += 4

end = cont

file += '\t\t"screen' + str(i) + '_0": {\n\t\t\t"address": ' + str(cont) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"screen' + str(i) + '_1": {\n\t\t\t"address": ' + str(cont+1) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"screen' + str(i) + '_2": {\n\t\t\t"address": ' + str(cont+2) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"screen' + str(i) + '_3": {\n\t\t\t"address": ' + str(cont+3) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'

#game state, kirby and boss health
file += '\t\t"game_state": {\n\t\t\t"address": ' + str(53292) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"kirby_health": {\n\t\t\t"address": ' + str(53382) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"kirby_life": {\n\t\t\t"address": ' + str(53385) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"boss_health": {\n\t\t\t"address": ' + str(53395) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"kirby_x_scrol": {\n\t\t\t"address": ' + str(53340) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"kirby_x": {\n\t\t\t"address": ' + str(53331) + ',\n\t\t\t"type": ">u2"\n\t\t},\n'
file += '\t\t"kirby_y_scrol": {\n\t\t\t"address": ' + str(53341) + ',\n\t\t\t"type": ">u1"\n\t\t},\n'
file += '\t\t"kirby_y": {\n\t\t\t"address": ' + str(53333) + ',\n\t\t\t"type": ">u2"\n\t\t}\n'
file += "\t}\n}"

data_file = open('data.json', 'w')
data_file.write(file)
data_file.close()
