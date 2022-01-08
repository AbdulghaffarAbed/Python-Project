import os
import json
import re
import optparse
import logging
import shutil
from command import Command
from log import log_output_file
from csvv import csv_output_file

#from command import Command
#from project2.command import Command

def create_log_file(dict):
    logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format=dict)


class Parse:
    json_file = open("configuration.json","r")
    json_read = json_file.read()
    json_dict = json.loads(json_read)

    Threshold_size = str(json_dict[" Threshold_size "])
    Threshold_list = Threshold_size.split("KB")
    Threshold_size = int(Threshold_list[0])*1024

    Max_commands = int(json_dict[" Max_commands "])
    Max_log_files = int(json_dict[" Max_log_files "])
    Same_dir = json_dict[" Same_dir "]
    output = json_dict[" output "]

    parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
    parser.add_option("-s", "--inputscript", dest="input_script", type="string", help="specify input script path")
    parser.add_option("-o", "--outputscript", dest="output_script", type="string", help="specify output script path")
    (options, args) = parser.parse_args()
    input_script = str(options.input_script)
    output_script_path = str(options.output_script)

    script_file = open(input_script,"r")
    commands_list = script_file.readlines()

    comm = Command()
    dictionary = {}
    num_of_commands = 1
    for command in commands_list:
        if num_of_commands <= Max_commands:
            sublist = command.split(" ")
            if len(sublist) == 3 and sublist[0] == 'Grep':
                sublist[2] = sublist[2].strip()
                sublist[1] = re.sub(r'[<>"]',"",sublist[1])
                sublist[2] = re.sub(r'[<>"]',"",sublist[2])
                result = comm.grep(sublist[1], sublist[2])

            elif len(sublist) == 3 and sublist[0] == 'Mv_last':
                sublist[2] = sublist[2].strip()
                sublist[1] = re.sub(r'[<>"]',"",sublist[1])
                sublist[2] = re.sub(r'[<>"]',"",sublist[2])
                result = comm.Mv_last(sublist[1], sublist[2])

            elif len(sublist) == 2 and sublist[0] == 'Categorize':
                sublist[1] = sublist[1].strip()
                sublist[1] = re.sub(r'[<>"]',"",sublist[1])
                result = comm.categorize(sublist[1], Threshold_size)

            dictionary["Line-"+str(num_of_commands)] = str(result)
            num_of_commands += 1


    if Same_dir == True:
        try:
            os.mkdir("PASSED")
            os.mkdir("FAILED")
        except:
            pass

        flag = True  # to determine whether all lines passed execution or not
        if output == 'log':
            for i in range(len(dictionary)):
                if dictionary['Line-'+str(i+1)] == 'False':
                    flag = False
                    break
            if flag:
                log_output_file(output_script_path+"PASSED\\", dictionary, Max_log_files)
            else:
                log_output_file(output_script_path+"FAILED\\", dictionary, Max_log_files)

        elif output == 'csv':
            for i in range(len(dictionary)):
                if dictionary['Line-'+str(i+1)] == 'False':
                    flag = False
                    break
            if flag:
                csv_output_file(output_script_path+"PASSED\\", dictionary, Max_log_files)
            else:
                csv_output_file(output_script_path+"FAILED\\", dictionary, Max_log_files)

        else:  # type of file is not supported
            exit(0)

    else:
        try:
            shutil.rmtree(output_script_path+"PASSED\\")
        except:
            pass
        try:
            shutil.rmtree(output_script_path+"FAILED\\")
        except:
            pass

        if output == 'log':
            log_output_file(output_script_path, dictionary, Max_log_files)
        elif output == 'csv':
            csv_output_file(output_script_path, dictionary, Max_log_files)
        else:
            exit(0)