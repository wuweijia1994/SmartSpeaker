import tarfile
import os
import shutil

def build_directory(file_path):
    if not(os.path.exists(file_path)):
        os.mkdir(file_path)
        print("Build up directory successfully: " + file_path)
    else:
        print("This directory has been built: " + file_path)

def un_tar(zip_file_path, file, common_file):
    file_name = os.path.join(zip_file_path, file)
    target_name = os.path.join(zip_file_path, common_file, file)
    common_name = os.path.join(zip_file_path, common_file)
    tar = tarfile.open(file_name)  
    names = tar.getnames()

    build_directory(common_name)

    for name in names:  
        tar.extract(name, common_name)
    tar.close()

def get_subfolders(dir):
    if os.path.exists(dir):
        filtered_dir = os.listdir(dir)
        #special for MAC
        if(filtered_dir.count(".DS_Store") > 0):
            filtered_dir.remove(".DS_Store")
        return filtered_dir
    else:
        return ""

def go_through(zip_file_path):
    files = get_subfolders(zip_file_path)
    for file in files:
        if(file.endswith('.tgz')):
            file_dir = os.path.join(zip_file_path, file)
            common_path = 'Unzip files'
            build_directory(os.path.join(zip_file_path, common_path))
            un_tar(zip_file_path, file, common_file=common_path)

def gather_files(gather_file_path):
    build_directory(os.path.join(gather_file_path, "wav"))
    files = get_subfolders(gather_file_path)
    for file in files:
        #Only gether the .wav files
        wav_file_path = os.path.join(gather_file_path, file, "wav")
        wav_files = get_subfolders(wav_file_path)
        for file in wav_files:
            shutil.copy(os.path.join(wav_file_path, file), os.path.join(gather_file_path, "wav"))

if __name__ == '__main__':
    # go_through('/Users/weijiawu/Downloads/archive')
    gather_files('/Users/weijiawu/Downloads/archive/Unzip files')
