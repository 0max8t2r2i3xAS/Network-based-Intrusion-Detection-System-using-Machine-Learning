import pandas as pd
#import seaborn as sns 
import numpy as np
import os
from joblib import load
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from Feature_extraction.Data_cleaning import Data_cleaning


if __name__ == "__main__":
#Variable Declaration zone
    working_directory = "C:/Users/User/Documents/Final Year Project/NIDS-IoT/"
    model = load("C:/Users/User/Documents/Final Year Project/NIDS-IoT/detection/Models/LogisticRegression_model_8_CICIoT.joblib")
    
    csv_directory = working_directory + "data/pre-processed_csv_files/"
    csv_files = os.listdir(csv_directory)
    X_columns = [
    'flow_duration', 'Header_Length', 'Protocol Type', 'Duration',
       'Rate', 'Srate', 'Drate', 'fin_flag_number', 'syn_flag_number',
       'rst_flag_number', 'psh_flag_number', 'ack_flag_number',
       'ece_flag_number', 'cwr_flag_number', 'ack_count',
       'syn_count', 'fin_count', 'urg_count', 'rst_count', 
    'HTTP', 'HTTPS', 'DNS', 'Telnet', 'SMTP', 'SSH', 'IRC', 'TCP',
       'UDP', 'DHCP', 'ARP', 'ICMP', 'IPv', 'LLC', 'Tot sum', 'Min',
       'Max', 'AVG', 'Std', 'Tot size', 'IAT', 'Number', 'Magnitue',
       'Radius', 'Covariance', 'Variance', 'Weight', 
]
    y_column = 'label'
    
#Pre-process raw_pcap to pre-processed_csv_files

    #call clean_data module to output desired csv

#detection logic
    

    #load csv from pre-processed_csv_files and predict
    scaler = StandardScaler()
    scaler.fit(pd.read_csv(csv_directory + csv_files[0])[X_columns])
    data = pd.read_csv(csv_directory + csv_files[0])
    data[X_columns] = scaler.transform(data[X_columns])
    detection = list(model.predict(data[X_columns]))
    


    print(detection)
    #if (not 'Normal') then 
    # transform file name, suspicious_{device}_{datetime}.csv 
    # parse to abnormal_traffics_csv and call Reciever.update(file) to update(sub and pub)

    