
import imageio.v2 as imageio

writer = imageio.get_writer('output1.mp4', fps=30)
tmp = imageio.imread('imageio:astronaut.png')
for i in range(1200):
    print("Frame", i)
    writer.append_data(tmp)

writer.close()
