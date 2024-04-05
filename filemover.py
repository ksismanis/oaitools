import os,shutil
import subprocess

directory = '/data/data1/users/ksismanis/testoai/to.upscale/1046/'
tdir = '/data/data1/users/ksismanis/testoai/efha_upscaled/output_renamed/1046'
# orglist = [1002,1008,1031,1049,1046,1030,1029,1018]
# orglist=1018


# for org in orglist:
#         directory = '/data/data1/users/ksismanis/testoai/efha_upscaled/output/'+str(org)
#         tdir = '/data/data1/users/ksismanis/testoai/efha_upscaled/output_renamed/'+str(org)
#         try:os.mkdir(tdir)
#         except: print('exists')
for file in os.listdir(directory):
        filename = os.fsdecode(file)
        imagefile = os.path.join(directory, filename)
        if 'JPG' in imagefile:
                # print(filename)  
                source = os.path.join(tdir,filename.replace('JPG','jpg'))
                # print(source)
                target  = os.path.join(tdir,filename)
                # print(target)
                # targetfilename = os.path.join(tdir,filename.replace("artists_",""))
                shutil.move(source, target)