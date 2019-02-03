import os
import yaml
import re
import shutil
import logging
import time

class Walker():
    def __init__(self, config_name):
        logging.basicConfig(filename='logs/{}.log'.format(time.strftime("%Y%m%d-%H%M%S")), level=10)

        self.config = self.read_yaml(config_name)
        self.path = self.config['directory']
        self.out_path = self.config['out_dir']
        self.rx_folder_name = self.config['folder_name']
        self.rx_file_name = self.config['file_name'] 
        self.rx_exclude_folders = self.skip_folder(self.config['exclude_folder_list'])

    def skip_folder(self, folder_list):
        out_string = '('
        for folder in folder_list:
            out_string = out_string + folder + "|"

        out_string = out_string[:-1] + ')'
        return out_string

    def read_yaml(self, config_name):
        with open(config_name, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                logging.error(exc)

    def move_file(self, dir_name, file_name):
        try: 
            current_loc = os.path.join(dir_name, file_name)
            out_dir = dir_name.replace(self.path, self.out_path)
            out_loc = os.path.join(out_dir, file_name)

            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            shutil.copy(current_loc, out_loc)

            logging.info("moving from: {} \n To: {}".format(current_loc, out_loc))
        except Exception as ex:
            logging.error(ex)
        


    def walk_dir(self):
        print("walking ", self.path)
        count = 0
        for dir_name, sub_dir_name, file_list in os.walk(self.path):
            if (re.search(self.rx_folder_name, dir_name) != None and 
                re.search(self.rx_exclude_folders, dir_name) == None):
                for fname in file_list:
                    if(re.search(self.rx_file_name, fname) != None):
                        count = count + 1
     
                        self.move_file(dir_name, fname)
        
        logging.info("moved {} files".format(count))


