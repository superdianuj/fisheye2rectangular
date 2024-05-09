import imageio.v2 as imageio
import os
import cv2
import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--use_remapping', type=bool, default=True)
parser.add_argument('--dir', type=str, required=True)
args=parser.parse_args()

# CONVErt insp to png
#================================================================================================
directory=args.dir

# Sort files by numeric order
file_names = sorted(os.listdir(directory), key=lambda x: int(x.split('_')[-1].split('_')[-1].split('_')[-1].split('_')[-1].split('.')[0]) if '_' in x else int(x.split('.')[0]))

# Full paths of the files
images_path = [os.path.join(directory, file_name) for file_name in file_names if file_name.endswith('.insp') or file_name.endswith('.INSP')]

pos=0

new_dir=directory+'_png'

if os.path.exists(new_dir):
    os.system('rm -r '+new_dir)

print(images_path)
os.mkdir(new_dir)

for filename in images_path:
    # Extract the RGB image data using exiftool
    subprocess.run(['exiftool', '-b', '-PreviewImage', filename], stdout=open(f'temp_image.jpg', 'wb'))

    # Read the extracted RGB image using OpenCV
    rgb = cv2.imread('temp_image.jpg')

    # Rotate the image 90 degrees clockwise using cv2
    rgb = cv2.rotate(rgb, cv2.ROTATE_180)

    # Save the rotated RGB image as a PNG file using OpenCV
    cv2.imwrite(f'{new_dir}/{pos}.png', rgb)
    pos += 1

os.remove('temp_image.jpg')



# from pngs, convert to equirectangular
#================================================================================================
if not args.use_remapping:
    directory=new_dir

    # Sort files by numeric order
    file_names = sorted(os.listdir(directory), key=lambda x: int(x.split('_')[-1].split('_')[-1].split('_')[-1].split('_')[-1].split('.')[0]) if '_' in x else int(x.split('.')[0]))


    # Full paths of the files
    images_path = [os.path.join(directory, file_name) for file_name in file_names if file_name.endswith('.png')]


    new_directory = directory + '_equirectangular'
    if os.path.exists(new_directory):
        os.system('rm -r '+new_directory)

    os.mkdir(new_directory)

    counter=0
    print("!!!")
    print(images_path)

    for filename in images_path:
        os.system(f'ffmpeg -i {filename} -filter_complex "[0:v]v360=input=dfisheye:output=equirect:pitch=-22:roll=-10:yaw=20:ih_fov=191.5:iv_fov=191.5[out_v]" -map "[out_v]" {new_directory}/im_{counter}.png')
        # os.system(f'ffmpeg -i {filename} -filter_complex "[0:v]v360=input=dfisheye:output=equirect:pitch=-20:roll=-25:yaw=15:ih_fov=195:iv_fov=195:h_fov=195:v_fov=195[out_v]" -map "[out_v]" {new_directory}/im_{counter}.png')
        counter+=1


else:

    directory=new_dir

    # Sort files by numeric order
    file_names = sorted(os.listdir(directory), key=lambda x: int(x.split('_')[-1].split('_')[-1].split('_')[-1].split('_')[-1].split('.')[0]) if '_' in x else int(x.split('.')[0]))


    # Full paths of the files
    images_path = [os.path.join(directory, file_name) for file_name in file_names if file_name.endswith('.png')]


    new_directory = directory + '_equirectangular_remapped'
    if os.path.exists(new_directory):
        os.system('rm -r '+new_directory)

    os.mkdir(new_directory)

    os.system('gcc -o projection projection.c -lm')
    os.system(f'./projection -x xmap.pgm -y ymap.pgm -h 910 -w 1920 -r 910 -c 1920 -b 0 -m samsung_gear_360')

    counter=0

    for filename in images_path:
        os.system(f'ffmpeg -i {filename} -i xmap.pgm -i ymap.pgm -filter_complex remap {new_directory}/im_{counter}.png -y')
       
        img=cv2.imread(f'{new_directory}/im_{counter}.png')
       
	img_left_cropped = img[:, :img.shape[1]//2]
	img_right_cropped = img[:, img.shape[1]//2:img.shape[1]]


	new_img_right=img_left_cropped
	#new_img_left=cv2.rotate(img_right_cropped, cv2.ROTATE_180)
	new_img_left=img_right_cropped

	# stich thr right half of the original image with the rotated image 
	img_stiched = cv2.hconcat([new_img_left, new_img_right])

        cv2.imwrite(f'{new_directory}/im_{counter}.png', img_stiched)

        counter+=1


     


