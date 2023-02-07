from tqdm import tqdm
import time
 
 
for i in tqdm (range (1000),
               desc="Loading...",
               ascii=False, ncols=100):

    time.sleep(0.1)