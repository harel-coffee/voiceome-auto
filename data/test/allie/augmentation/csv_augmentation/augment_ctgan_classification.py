'''
              AAA               lllllll lllllll   iiii                      
              A:::A              l:::::l l:::::l  i::::i                     
             A:::::A             l:::::l l:::::l   iiii                      
            A:::::::A            l:::::l l:::::l                             
           A:::::::::A            l::::l  l::::l iiiiiii     eeeeeeeeeeee    
          A:::::A:::::A           l::::l  l::::l i:::::i   ee::::::::::::ee  
         A:::::A A:::::A          l::::l  l::::l  i::::i  e::::::eeeee:::::ee
        A:::::A   A:::::A         l::::l  l::::l  i::::i e::::::e     e:::::e
       A:::::A     A:::::A        l::::l  l::::l  i::::i e:::::::eeeee::::::e
      A:::::AAAAAAAAA:::::A       l::::l  l::::l  i::::i e:::::::::::::::::e 
     A:::::::::::::::::::::A      l::::l  l::::l  i::::i e::::::eeeeeeeeeee  
    A:::::AAAAAAAAAAAAA:::::A     l::::l  l::::l  i::::i e:::::::e           
   A:::::A             A:::::A   l::::::ll::::::li::::::ie::::::::e          
  A:::::A               A:::::A  l::::::ll::::::li::::::i e::::::::eeeeeeee  
 A:::::A                 A:::::A l::::::ll::::::li::::::i  ee:::::::::::::e  
AAAAAAA                   AAAAAAAlllllllllllllllliiiiiiii    eeeeeeeeeeeeee  

 / _ \                                 | |      | | (_)            
/ /_\ \_   _  __ _ _ __ ___   ___ _ __ | |_ __ _| |_ _  ___  _ __  
|  _  | | | |/ _` | '_ ` _ \ / _ \ '_ \| __/ _` | __| |/ _ \| '_ \ 
| | | | |_| | (_| | | | | | |  __/ | | | || (_| | |_| | (_) | | | |
\_| |_/\__,_|\__, |_| |_| |_|\___|_| |_|\__\__,_|\__|_|\___/|_| |_|
              __/ |                                                
             |___/                                                 
  ___  ______ _____       _____  _____  _   _ 
 / _ \ | ___ \_   _|  _  /  __ \/  ___|| | | |
/ /_\ \| |_/ / | |   (_) | /  \/\ `--. | | | |
|  _  ||  __/  | |       | |     `--. \| | | |
| | | || |    _| |_   _  | \__/\/\__/ /\ \_/ /
\_| |_/\_|    \___/  (_)  \____/\____/  \___/ 
                                              
'''
import os
try:
    from ctgan import CTGANSynthesizer
except:
    os.system('pip3 install ctgan==0.2.1')
    from ctgan import CTGANSynthesizer
import time, random
import pandas as pd
import numpy as np

def find_nearestval(value,values):
    distances=list()
    for i in range(len(values)):
        newvalue=values[i]-value
        distances.append(newvalue)
    minimum=min(distances)
    minind=distances.index(minimum)
    newvalue=values[minind]
    # print('value --> newvalue')
    # print(value)
    # print(newvalue)

    return newvalue

def get_index_positions(list_of_elems, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list


def augment_ctgan_classification(csvfile):
    data=pd.read_csv(csvfile)

    ctgan = CTGANSynthesizer()
    ctgan.fit(data,epochs=10) #15

    percent_generated=1
    df_gen = ctgan.sample(int(len(data)*percent_generated))
    df_gen['class_']=df_gen['class_'].apply(np.floor)

    values=list(set(list(data['class_'])))
    newclass=df_gen['class_']
    newclass2=list()

    for i in range(len(newclass)):
        if newclass[i] not in values:
            newvalue=find_nearestval(newclass[i], values)
            newclass2.append(newvalue)
        else:
            newclass2.append(newclass[i])

    df_gen['class_']=newclass2

    # now count each value and balance
    classcol=list(df_gen['class_'])
    unique_classes=list(set(df_gen['class_']))
    counts=list()
    for i in range(len(unique_classes)):
        counts.append(classcol.count(unique_classes[i]))
    minval=min(counts)
    print(minval)

    # now balance out the classes by removing all to minimum value 
    for i in range(len(unique_classes)):
        print(unique_classes[i])
        index_pos_list=get_index_positions(classcol,unique_classes[i])
        while len(index_pos_list) >= minval:
            index_pos_list=get_index_positions(classcol,unique_classes[i])
            random_ind=random.choice(index_pos_list)
            df_gen=df_gen.drop(df_gen.index[random_ind])
            classcol=list(df_gen['class_'])

    print('augmented with %s samples'%(str(len(unique_classes)*minval)))
    print(df_gen)
    # now add both togrther to make new .CSV file
    newfile1='augmented_'+csvfile
    df_gen.to_csv(newfile1, index=0)

    # now combine augmented and regular dataset
    data2=pd.read_csv('augmented_'+csvfile)
    frames = [data, data2]
    result = pd.concat(frames)
    newfile='augmented_combined_'+csvfile
    result.to_csv(newfile, index=0)
    return [csvfile, newfile1, newfile2]