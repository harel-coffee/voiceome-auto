'''
Load all model accuracies, names, and standard deviations
and output them in a spreadsheet.

This is intended for any model file directory using the nlx-model repository.'''

import json, os, xlsxwriter, getpass

os.chdir('/Users/'+getpass.getuser()+'/nlx-model/nlx-audiomodel/models')

listdir=os.listdir()

names=list()
accs=list()
stds=list()
modeltypes=list()

for i in range(len(listdir)):
    if listdir[i][-5:]=='.json':
        try:
            g=json.load(open(listdir[i]))
            acc=g['accuracy']
            name=g['model']
            std=g['deviation']
            modeltype=g['modeltype']

            names.append(name)
            accs.append(acc)
            stds.append(std)
            modeltypes.append(modeltype)
        except:
            print('error %s'%(listdir[i]))


workbook = xlsxwriter.Workbook('summary.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Model Name')
worksheet.write('B1', 'Accuracy')
worksheet.write('C1', 'Standard Deviation')
worksheet.write('D1', 'Modeltype')

for j in range(len(names)):
    worksheet.write('A%s'%(str(j+2)), names[j])
    worksheet.write('B%s'%(str(j+2)), accs[j])
    worksheet.write('C%s'%(str(j+2)), stds[j])
    worksheet.write('D%s'%(str(j+2)), modeltypes[j])

workbook.close()

os.system('open %s'%(os.getcwd()+'/summary.xlsx'))
