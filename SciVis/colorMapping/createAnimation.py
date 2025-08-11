import matplotlib.pyplot as plt
import matplotlib.animation as animation

import os

def create_animation(image_folder, output_file):
    
    file_names = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    
    fig, ax = plt.subplots()
    ax.set_axis_off()
    img = plt.imread(os.path.join(image_folder, file_names[0]))
    im = ax.imshow(img)

    
    def update(frame):
        img = plt.imread(os.path.join(image_folder, file_names[frame]))
        im.set_array(img)
        return [im]

    
    ani = animation.FuncAnimation(fig, update, frames=len(file_names), blit=True,)
    os.makedirs("gifs", exist_ok=True)

    ani.save(f"gifs/{output_file}.gif", writer='pillow', fps=2)

if __name__ == "__main__":
    image_folders=["animation_continuous_inferno","animation_discrete_YlOrRd","animation_log_continuous_inferno","global_animation_continuous_inferno"]
    output_files=["continuous_inferno","discrete_YlOrRd","log_continuos_inferno","global_inferno"]
    for image_folder,output_file in zip(image_folders,output_files):
        create_animation(image_folder,output_file)