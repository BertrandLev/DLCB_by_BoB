from datetime import datetime
from utils.Log_box import Log_box
from PyQt6.QtWidgets import QApplication
import subprocess
import os
import re


class Bob_simulation():

    def __init__(self, log:Log_box, chemical_params:dict = {}, componant_count:int = 0, componant_list:list = []) -> None:
        self.log = log
        self.Bob_folder = os.path.abspath("app/data/Bob")
        self.result_folder = os.path.abspath("app/data/Results")
        self.input_file = "inputBob.dat"
        self.chemical_params = chemical_params
        self.componant_count = componant_count
        self.componant_list = componant_list

    def set_chemical_params(self, value:dict):
        if value:
            self.chemical_params = value
        else:
            raise ValueError("Fail to set chemical parameters")

    def set_componant_count(self, value:int):
        if value:
            self.componant_count = value
        else:
            raise ValueError("Fail to set componant count")

    def set_componant_list(self, value:int):
        if value:
            self.componant_list = value
        else:
            raise ValueError("Fail to set componant list")

    def start_simulation(self):
        self.log.appendLogMessage("Simulation Start...")
        try:
            self.log.appendLogMessage("Input File generation...")
            self.generate_input_file()
            QApplication.processEvents()
            self.log.appendLogMessage("Launch of bob2P5.exe...")
            self.launch_application()
            QApplication.processEvents()
            self.log.appendLogMessage("Treatment of the results...")
            self.files_post_treatment()
            QApplication.processEvents()
            self.log.appendLogMessage("Simulation finished.")
        except Exception as e:
            self.log.appendErrorMessage("Simulation failed. Error :",e)

    def launch_application(self):
        try:
            Bob_exe = os.path.join(self.Bob_folder,"bob2P5.exe")
            command = [Bob_exe,'-i', self.input_file]
            subprocess.run(command, cwd = self.Bob_folder)
            return True
        except Exception as e:
            self.log.appendErrorMessage("An error append while launching Bob. Error :",e)
            return False
    
    def generate_input_file(self):
        output_file = os.path.join("app/data/Bob","inputBob.dat")
        try:
            with open(output_file, "w") as file:
                file.write("50000 500000\n")
                file.write("1.0\n")
                file.write("1\n")
                file.write(f"{self.chemical_params['Mo']} {self.chemical_params['Ne']} {self.chemical_params['rho']}\n")
                file.write(f"{self.chemical_params['tau']} {self.chemical_params['T']}\n")
                file.write(f"{str(self.componant_count)}\n")
                for i in range(0,self.componant_count):
                    bob_comp_params = self.componant_list[i].get_comp_param()
                    file.write(bob_comp_params['f']+"\n")
                    file.write(bob_comp_params['params'])
            return True
        except Exception as e:
            self.log.appendErrorMessage("Fail to write inputBob.dat file. Error:",e)
            return False

    def files_post_treatment(self):
        today_date = datetime.today().date().strftime("%Y%m%d")
         # Creation of output folder name
        pattern = rf"{today_date}_\d{{3}}$"
        simu_num = 1
        try:
            for item in os.listdir(self.result_folder):
                if os.path.isdir(os.path.join(self.result_folder,item)):
                    if bool(re.match(pattern, item)):
                        num_tmp = int(item[-3:])+1
                        simu_num = num_tmp if num_tmp > simu_num else simu_num
            output_folder = os.path.join(self.result_folder, today_date + "_" + "{:03d}".format(simu_num))
            os.makedirs(output_folder)
        except Exception as e:
            self.log.appendErrorMessage("Error while creating the result folder. Error :", e)
        # Transfering file to output folder
        files = ("gt.dat","gtp.dat","info.txt","maxwell.dat","polyconf.dat","supertube.dat")
        try:
            for file in files:
                source_file = os.path.join(self.Bob_folder,file)
                if os.path.exists(source_file):
                    os.rename(source_file, os.path.join(output_folder,file))
        except Exception as e:
            self.log.appendErrorMessage("Error while moving results files. Error :", e)