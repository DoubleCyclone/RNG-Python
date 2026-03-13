from utils import app_data_path
import os
import csv
from defaults import HISTORY_HEADERS
import datetime

class HistoryHandler() :
    def __init__(self):
        self.base_directory = app_data_path("history")
        
        self.csv_path = os.path.join(self.base_directory, "history.csv")
        
        self.check_paths()
        
    def check_paths(self):
        # Create base dir if it does not exist
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
            
        # Create csv if it does not exist
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, mode="w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(HISTORY_HEADERS)
    
    def record(self, numbers, min, max):
        self.check_paths()
        
        with open(self.csv_path, mode="a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([numbers, min, max, f"{datetime.datetime.now().strftime('%X')} - {datetime.datetime.now().strftime('%x')}"])
        
        
        
        