
from blindman.discord import get_avatar

x = get_avatar('87351108317491200', size=1024)
print(len(x))
with open('tmp', 'wb') as f:
    f.write(x)

'''
import imageio.v2 as imageio

writer = imageio.get_writer('output1.mp4', fps=30)
tmp = imageio.imread('imageio:astronaut.png')
for i in range(1200):
    print("Frame", i)
    writer.append_data(tmp)

writer.close()
'''
