from PIL import Image
import os

# Klasör yolu ve maksimum boyutunu belirleyin
folder_path = "/Users/ozgeariburnu/Downloads/Vectors"
index = 1
max_size = 7000


def loop_in_folder(folder_path):
    # Klasördeki tüm EPS dosyalarını seçin ve dönüştürün
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".eps"):
            convert_eps_to_jpg(folder_path, file_name)
        

def convert_eps_to_jpg(folder_path, file_name):
    input_path = os.path.join(folder_path, file_name)
    print(f'Start => {input_path}')

    # EPS dosyasını açın ve boyutunu değiştirin
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            if width >= height:
                ratio = max_size / width
                new_width = max_size
                new_height = int(height * ratio)
            else:
                ratio = max_size / height
                new_height = max_size
                new_width = int(width * ratio)
                
            img = img.resize((new_width, new_height))
            
            # JPEG dosyasını kaydedin
            new_file_name = os.path.splitext(file_name)[0] + ".jpg"
            output_path = os.path.join(folder_path, new_file_name)
            img.save(output_path)
            print(f'Success => {output_path}')
    except Exception as err:
        print(f'Error => {err}')


if __name__ == '__main__':
    path = os.path.join(folder_path, f'{index}')

    while os.path.exists(path):
        loop_in_folder(path)

        index += 1
        path = os.path.join(folder_path, f'{index}')