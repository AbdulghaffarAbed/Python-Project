import csv
import os
from command import Command

#Give name to the new log file
def fileName(path):
    comm = Command()
    index = 2
    file_name = 'output1.csv'
    status = comm.grep(file_name, path)
    while status:
        lis = file_name.split(".")
        lis[0] = lis[0][0:len(lis[0])-1]
        lis[0] += str(index)
        lis[1] = "." + lis[1]       #extension
        file_name = lis[0]+lis[1]
        index += 1
        status = comm.grep(file_name, path)
    return path+file_name


def num_of_files(path):
    count = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for i in filenames:
            listt = i.split(".")
            extension = listt[len(listt)-1]
            if (extension == 'csv'):
                count += 1
    return count

def csv_output_file(path, dictionary, Max_log_files):
    with open(fileName(path), 'w', newline='') as i:
        write_var = csv.writer(i)
        dictionary = dict(dictionary)
        write_var.writerow(dictionary.keys())
        write_var.writerow(dictionary.values())

    files_number = num_of_files(path)
    if files_number > Max_log_files:  # if file numbers greater than the specific number delete the oldest one
        log_files = []
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        for p in paths:
            lis = p.split(".")
            if lis[len(lis) - 1] == "csv":
                log_files.append(p)
        oldest_file = min(log_files, key=os.path.getctime)
        os.remove(oldest_file)