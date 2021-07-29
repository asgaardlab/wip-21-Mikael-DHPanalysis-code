### Importing Necessary Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import subprocess
from ruamel.yaml import YAML
import time 
import ddsl_load_tester as load_tester
from kubernetes import client, config
from tqdm.auto import tqdm
import math
from Wappalyzer import Wappalyzer , WebPage
import csv
tqdm.pandas()
loop_timer = load_tester.TimerClass()
total_timer = load_tester.TimerClass()
lt = load_tester.DdslLoadTester(hatch_rate=20, temp_stat_max_len=10, base='http://xxx.xxx.xxx.xxx:xxxxx/')

print("WORKS")
try:
    os.chdir(os.path.join(os.getcwd(), 'examples'))
    print(os.getcwd())
except:
    pass

config.load_kube_config()
#%%
DEPLOYMENT_NAME = 'wordpress'
DEPLOYMENT_NS = 'default'
########## Function to Apply the deployment
def app_apply(file,version):
    yaml=YAML(typ="safe")
    with open(file) as f:
        list_doc = yaml.load(f)
    list_doc['spec']['template']['spec']['containers'][0]['image'] = version
    with open(file,'w') as f:
        yaml.dump(list_doc,f)
    try : 
        output = subprocess.check_output('kubectl apply -f wordpress_only.yaml --insecure-skip-tls-verify=true', shell=True)
    except : 
        print("ERROR IN DEPLOYING")
    print(output , "Successfully Deployed Image : ",version)



#### Defining the Version Data for Software 
data = pd.read_csv("Image_Data2.csv") 
selected_index =[]
All_layers = []
place_holder=[]
Versions = []
web_data =[]
size = len(data)
for i in range(size):
    x = re.search("apache",data['Tag'][i])
    y = re.search("linux/amd64",data['Arch'][i])
    if x != None and y != None :
        selected_index.append(i)
Selected_Data = data.iloc[selected_index]
for i in selected_index :
    Versions.append((Selected_Data["Tag"][i].replace(" ","")))

########## Apply the Kubernetes Application 
for j in range(np.shape(Versions)[0]):
    print("Implementatio of ", j ,"out of :",np.shape(Versions)[0])
    lt.stop_test()
    app_apply(file="wordpress_only.yaml",version = Versions[j])
    time.sleep(150)
    try : 
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url('http://xxx.xxx.xxx.xxx:xxxxx/')
        Apache= webpage.headers['Server']
        Php = webpage.headers['X-Powered-By']
        Wordpress = webpage.meta['generator']
        web_data.append([Apache,Php,Wordpress,Versions[j]])
        print("Apache Version:  ", Apache)
        print("PHP Version :",Php)
        print(Wordpress)
    except:
        print("Couldn't Identify the Dependencies")
        web_data.append(["None","None","None",Versions[j]])
    #output = subprocess.check_output('kubectl get pods', shell=True)
    #print(output)
    loop_timer = load_tester.TimerClass()
    total_timer = load_tester.TimerClass()
    user_sequence = [20,20,20,20,20]
    lt.change_count(user_sequence[0])
    lt.start_capturing()
    loop_time_in_secs = load_tester.get_loop_time_in_secs('20s')
    loop_timer.tic()
    total_timer.tic()
    results = None
    for k in tqdm(range(len(user_sequence)*3)):
        user_count = user_sequence[math.floor(k/3)]
        lt.change_count(user_count)

        sleep_time = loop_time_in_secs - loop_timer.toc()
        if sleep_time > 0:
            time.sleep(sleep_time)

        loop_timer.tic()

        result = lt.get_all_stats()
        df_result = pd.DataFrame(data=result)

        if results is None:
            results = df_result
        else:
            results = results.append(df_result)



        #####Identification

        print("Response Time :", result['current_response_time_average'], "Throughput :",result['current_rps'],"Fails :",result['fail_ratio'],"Users :",result['user_count'] )

    lt.stop_test()

    results, filename = lt.prepare_results_from_df(results)
#     filename2 = './results2/{}.csv'.format(Versions[i])
    results.head()
    with open('./results/{}.csv'.format(Versions[j]), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([web_data])