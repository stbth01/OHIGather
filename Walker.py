import os
import yaml
import re
import shutil
import logging
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
from modules.DecryptPdf import DecryptPdf

class Walker():
    def __init__(self, config_name):
        logging.basicConfig(filename='logs/{}.log'.format(time.strftime("%Y%m%d-%H%M%S")), level=20)
        self.logger = logging.getLogger()

        self.decypter = DecryptPdf(self.logger)

        self.config = self.read_yaml(config_name)
        self.path = self.config['directory']
        self.out_path = self.config['out_dir']
        self.rx_folder_name = self.config['folder_name']
        self.rx_file_name = self.join_rx_list(self.config['file_names'])
        self.rx_exclude_folders = self.join_rx_list(self.config['exclude_folder_list'])
        self.squash = True if self.config['squash_folders'] == "True" else False
        self.p_num_re = self.config['p_num_regex']

    def join_rx_list(self, folder_list):
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
                self.logger.error(exc)

    def remove_instruction_pages(self, current_loc, out_loc):
        pages_to_keep = [0, 1, 2, 3] # page numbering starts from 0
        infile = self.decypter.decrypt(current_loc)
        output = PdfFileWriter()

        for i in pages_to_keep:
            p = infile.getPage(i)
            output.addPage(p)

        with open(out_loc, 'wb') as f:
            output.write(f)


    def move_file(self, dir_name, file_name, squash_folders=False):
        try: 
            if(squash_folders):
                # squash will just set the out to path to the config value
                out_dir = self.out_path
                # git parcel Number from dir
                try:
                    p_num = re.search(self.p_num_re, dir_name).group()
                except:
                    p_num = dir_name[-20:-5].replace('\\','')
                file_name_out = p_num+'_'+file_name


            else:
                # not squash dir_name which the subfolders and replaces
                # the stem of the dir defined in teh config with out dir
                # from teh config. This maintains the sub folders
                out_dir = dir_name.replace(self.path, self.out_path)
                file_name_out = file_name


            current_loc = os.path.join(dir_name, file_name)
            out_loc = os.path.join(out_dir, file_name_out)

            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            if (out_loc[-4:] == '.pdf'):
                self.remove_instruction_pages(current_loc, out_loc)
            else: 
                shutil.copy(current_loc, out_loc)

            self.logger.info("moving from: {} \n To: {}".format(current_loc, out_loc))
        except Exception as ex:
            self.logger.error(ex)

        


    def walk_dir(self):
        print("walking ", self.path)
        count = 0
        for dir_name, sub_dir_name, file_list in os.walk(self.path):
            if (re.search(self.rx_folder_name, dir_name) != None and 
                re.search(self.rx_exclude_folders, dir_name) == None):
                for fname in file_list:
                    if(re.search(self.rx_file_name, fname.lower()) != None):
                        count = count + 1
     
                        self.move_file(dir_name, fname, self.squash)
        
        self.logger.info("moved {} files".format(count))


