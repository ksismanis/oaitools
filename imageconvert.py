import os,shutil
import subprocess

# orglist = [1002,1008,1031,1049,1046,1030,1029,1018,1045]
orglist = [1045]
# orglist = ['test']
for org in orglist:
    print(org)
    directory = "/data/data1/users/ksismanis/SwinIR/results/" + str(org)
    tdir = "/data/data1/users/ksismanis/SwinIR/results/output/" + str(org)
    try:
        os.mkdir(tdir)
    except OSError as error:
        print(error)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        targetfilename = os.path.join(tdir,filename.replace(".png",".jpg"))
        # print(filename, targetfilename)
        # print(targetfilename)
        FNULL = open(os.devnull, 'w')
        retcode = subprocess.call(["/home/ksismanis/magick.1", os.path.join(directory,filename), targetfilename], stdout=FNULL, stderr=subprocess.STDOUT)