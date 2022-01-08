import logging
import os
from command import Command
import shutil

#delete handler for the created data file
def removeHandler(first):
    new_handler = logging.FileHandler(file_name)
    logger.addHandler(new_handler)

#Give name to the new log file
def fileName(path):
    comm = Command()
    index = 2
    file_name = 'output1.log'
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
            if (extension == 'log'):
                count += 1
    return count

#Create log file
def log_output_file(path, DIC, Max_log_files):
    #Create log file
    logging.basicConfig(filename=fileName(path), level=logging.INFO, filemode='w')
    logger = logging.getLogger()  # logging object
    # Our message inserted in these sentance
    logger.info(DIC)
    # Get logger (logging object) handlers
    logger.handlers
    first = logger.handlers[0]
    first.close()
    logger.removeHandler(first)

    files_number = num_of_files(path)

    if files_number >  Max_log_files:  # if file numbers greater than the specific number delete the oldest one
        log_files = []
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        for p in paths:
            lis = p.split(".")
            if lis[len(lis)-1] == "log":
                log_files.append(p)
        oldest_file = min(log_files, key=os.path.getctime)
        os.remove(oldest_file)