from Feature_extraction import Feature_extraction
import time
import warnings
warnings.filterwarnings('ignore')
import os
from tqdm import tqdm
from multiprocessing import Process
import numpy as np
import pandas as pd

if __name__ == '__main__':

    start = time.time()
    print("========== CIC IoT feature extraction ==========")
    
    pcapfiles = [
    "dump"
]
    subfiles_size = 10 # MB
    address =  "C:/Users/User/Documents/Final Year Project/NIDS-IoT/"#"../../"
    #address = "../../"
    split_directory = address + 'data/split_temp/'
    raw_pcap_directory = address + 'data/raw_pcap/'
    destination_directory = address + 'data/pre-processed_csv_files/'
    converted_csv_files_directory = address + 'data/pre-processed_csv_files/'
    n_threads = 8
    
    
    
        

    
    for i in range(len(pcapfiles)):
        lstart = time.time()
        pcap_filename = pcapfiles[i]
        pcap_file = raw_pcap_directory + pcapfiles[i]
        print(pcap_file)
        print(">>>> 1. splitting the .pcap file.")
        os.system('tcpdump -r '+ pcap_file +' -w ' + split_directory + 'split_temp -C ' + str(subfiles_size))
        subfiles = os.listdir(split_directory)
        
        print(">>>> 2. Converting (sub) .pcap files to .csv files.")
        processes = []
        errors = 0
        
        subfiles_threadlist = np.array_split(subfiles, (len(subfiles)/n_threads)+1)
        for f_list in tqdm(subfiles_threadlist):
            n_processes = min(len(f_list), n_threads)
            assert n_threads >= n_processes
            assert n_threads >= len(f_list)
            processes = []
            for i in range(n_processes):
                fe = Feature_extraction()
                f = f_list[i]
                subpcap_file = split_directory + f
                p = Process(target=fe.pcap_evaluation, args=(subpcap_file,destination_directory + f.split('.')[0]))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
        
        #fe = Feature_extraction()
        #subpcap_file = split_directory + "split_temp_test"
        #fe.pcap_evaluation(subpcap_file, destination_directory)
        print( str(len(subfiles)) + "  " + str(len(os.listdir(destination_directory))))
        
        assert len(subfiles)==len(os.listdir(destination_directory))
        print(">>>> 3. Removing (sub) .pcap files.")
        for sf in subfiles:
            os.remove(split_directory + sf)

        print(">>>> 4. Merging (sub) .csv files (summary).")
        
        csv_subfiles = os.listdir(destination_directory)
        mode = 'w'
        for f in tqdm(csv_subfiles):
            try:
                d = pd.read_csv(destination_directory + f)
                d.to_csv(destination_directory+pcap_filename + '.csv', header=mode=='w', index=False, mode=mode)
                mode='a'
            except:
                pass

        print(">>>> 5. Removing (sub) .csv files.")
        for cf in tqdm(csv_subfiles):
            os.remove(destination_directory + cf)
        print(f'done! ({destination_directory+pcap_filename})(' + str(round(time.time()-lstart, 2))+ 's),  total_errors= '+str(errors))
        
    end = time.time()
    print(f'Elapsed Time = {(end-start)}s')
    
    
    
