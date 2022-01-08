import os
import shutil

def move_file(src_path, dst_path):
    try:
        shutil.move(src_path, dst_path)
    except:
        #print("The file attempted to move is already moved to the destination directory")
        pass

class Command:
    def __int__(self):
        pass

    def grep(self, file, path):
        try:     #check whether the specified path exists by trying to list its files and subdirectories
            os.listdir(path)
        except:
            return False

        found = False  #flag to determine whether the file exists in the specified path
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                if(file == i):
                    found = True
                    f = os.path.join(dirpath, i)
                    #print("file: "+file+" exists and its path is: "+f)
        return found


    def Mv_last(self, src_path, dst_path):
        try:     #check whether the specified source and destination pathes exist
            os.listdir(src_path)
            os.listdir(dst_path)
        except:
            return False

        try:
            files = os.listdir(src_path)
            paths = [os.path.join(src_path, basename) for basename in files]
            latest_file = max(paths, key=os.path.getctime)
            #print("latest file is: " + latest_file)
            move_file(latest_file, dst_path)
            return True
        except:
            return False

    def categorize(self, src_path, threshold_size):
        try:    # check whether the source path exists
            os.listdir(src_path)
        except:
            return False

        try:
            less_threshold_directory = "less_than_threshold"
            path = os.path.join(src_path, less_threshold_directory)
            os.mkdir(path)
        except:
            pass

        try:
            more_threshold_directory = "more_than_threshold"
            path = os.path.join(src_path, more_threshold_directory)
            os.mkdir(path)
        except:
            pass


        for dirpath, dirnames, filenames in os.walk(src_path):
            for i in filenames:
                # use join to concatenate all the components of path
                f = os.path.join(dirpath, i)

                file_size = os.path.getsize(f)
                if (file_size < threshold_size):
                    src_directory = f
                    dest_directory = os.path.join(src_path, less_threshold_directory)
                    move_file(src_directory, dest_directory)

                elif (file_size > threshold_size):
                    src_directory = f
                    dest_directory = os.path.join(src_path, more_threshold_directory)
                    move_file(src_directory, dest_directory)
        return True