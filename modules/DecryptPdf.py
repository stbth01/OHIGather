import PyPDF2
import os

# decrypter class
class DecryptPdf:
    def __init__(self, logger):
        self.logger = logger


    # this function will decrypt the file located at in_file_path 
    # if necessary, and whether or not, will leave the resulting 
    # file in the location given by out_file_path
    # returns boolean result: True if successful, False if unsuccessful
    def decrypt(self, in_file_path):
        try:
            # open input file in read-binary mode
            file = open(in_file_path, 'rb')
            # create a file reader
            pdf_file = PyPDF2.PdfFileReader(file)

            self.logger.debug(pdf_file.isEncrypted)
            if pdf_file.isEncrypted:
                try: 
                    # attempt decryption using PyPDF2
                    pdf_file.decrypt('')
                     # TODO: fix bug here? write to disk BTH This this close resolves this
                    self.logger.debug('Decrypted (using PyPDF2) for {}'.format(in_file_path))
                    return pdf_file

                except:
                    try:
                        # if PyPDF2 failed, try to decrypt using qpdf shell command
                        command="cp '"+in_file_path+"' temp.pdf"
                        os.system(command)
                        command2 = 'qpdf --password= --decrypt temp.pdf decypted.pdf'
                        os.system(command2)
                        self.logger.debug('Decrypted (using qpdf) for {}'.format(in_file_path))

                        return PyPDF2.PdfFileReader('decypted.pdf', 'rb')
                    except Exception as e:
                        self.logger.error('Unable to decrypt using either PyPDF2 or qpdf! {}'.format(in_file_path),exc_info=True )
            else:
                self.logger.debug('Not encrypted {}'.format(in_file_path))
                import pdb; pdb.set_trace()
                return pdf_file


            # we succeeded in decrypting if it was necessary,
            # and left thea file in the desired condition at
            # the proper location.
        except:
            self.logger.error('Unable to open file for reading or unable to create PyPDF2.PdfFileReader! {}'.format(in_file_path))




# if __name__ == "__main__":
    # optional debugging; start at start of test execution
    # import pdb; pdb.set_trace()

    # set working folder

    # working_folder = '/Users/dalehunscher/Dropbox/DGH/github/DGH'
    # os.chdir(working_folder)

    # # declare subfolders, if any; if no subfolder, set to ""
    # # if there is a subfolder, must end in "/"
    # infile_subfolder = 'data/'
    # outfile_subfolder = 'data/'

    # _in_file_path = infile_subfolder+"2019_L4175.pdf"
    # _out_file_path = outfile_subfolder+"2019_L4175.fixed.pdf"

    # # declare instance of decrypter class
    # decrypter = DecryptPdf()
     
    # ret = decrypter.decrypt(in_file_path = _in_file_path,
    #                             out_file_path = _out_file_path)

    # print("result = "+str(ret))