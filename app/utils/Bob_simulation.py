from datetime import datetime
from utils.Log_box import Log_box
from PyQt6.QtWidgets import QApplication
import subprocess
import os
import re

class Bob_simulation():

    def __init__(self, log:Log_box, chemical_params:dict = {}, componant_list:list = []) -> None:
        self.log = log
        self.Bob_folder = os.path.abspath("app/data/Bob")
        self.result_folder = os.path.abspath("app/data/Results")
        self.input_file = "inputBob.dat"
        self.chemical_params = chemical_params
        self.componant_list = componant_list
        if self.componant_list:
            self.componant_count = len(self.componant_list)

    def set_chemical_params(self, value:dict):
        if value:
            self.chemical_params = value
        else:
            raise ValueError("Fail to set chemical parameters")

    def set_componant_list(self, value:list):
        if value:
            self.componant_count = len(value)
            self.componant_list = value
        else:
            raise ValueError("Fail to set componant list")

    def start_simulation(self):
        
        def nested_iteration(iterators_list):
            # Base case: if there are no more iterators, yield an empty tuple
            if not iterators_list:
                yield ()
            else:
                # Get the first iterator in the list
                current_iterator = iterators_list[0]
                # Recursively iterate over the remaining iterators
                for nested_result in nested_iteration(iterators_list[1:]):
                    # Iterate over the elements of the current iterator
                    for item in current_iterator:
                        # Yield the combination of the current element and the nested result
                        yield (item,) + nested_result

        self.log.appendLogMessage("Simulations Start...")
        iterators = [list(item.poly_model.iterate_model()) for item in self.componant_list]
        simu_num = 1
        for item in iterators:
            simu_num *= len(item)
        try:
            i = 1
            for models_params in nested_iteration(iterators):
                self.log.appendLogMessage(f"Simulation {i}/{simu_num}")
                start_time = datetime.now()
                self.generate_input_file(models_params)
                QApplication.processEvents()
                self.launch_application()
                QApplication.processEvents()
                self.files_post_treatment()
                end_time = datetime.now()
                self.log.appendLogMessage(f"Simulation {i} done in {end_time-start_time}s.")
                QApplication.processEvents()
                i += 1
        except Exception:
            raise
        self.log.appendLogMessage("Simulations finished.")

    def launch_application(self) -> None:
        try:
            Bob_exe = os.path.join(self.Bob_folder,"bob2P5.exe")
            command = [Bob_exe,'-i', self.input_file]
            subprocess.run(command, cwd = self.Bob_folder)
        except Exception:
            raise
    
    def generate_input_file(self, models_params) -> None:
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
                    fraction = self.componant_list[i].fraction.text()
                    file.write(fraction+"\n")
                    file.write(models_params[i])
        except Exception:
            raise

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
        except Exception:
            raise
        # Transfering file to output folder
        files = ("gt.dat","gtp.dat","info.txt","maxwell.dat","polyconf.dat","supertube.dat")
        try:
            for file in files:
                source_file = os.path.join(self.Bob_folder,file)
                if os.path.exists(source_file):
                    os.rename(source_file, os.path.join(output_folder,file))
        except Exception:
            raise