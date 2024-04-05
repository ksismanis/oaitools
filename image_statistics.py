from PIL import Image
import os,shutil

orglist = [1002,1008,1018,1029,1030,1031,1045,1046,1049,1052]
# orglist = [1045]
# orglist = [1018]
# directory = os.fsencode("/data/data1/users/ksismanis/testoai/lala")
# directory = "/data/data1/users/ksismanis/testoai/lala/"
# tdir = "/data/data1/users/ksismanis/testoai/to.upscale/"
# print(directory)
# print('org',',','count',',','count_to_upscale',',','count_to_upscalee',',','tier0_count',',','tier1_count',',','out_tier0',',','out_tier1',',','out_tier2',',','out_tier3')
print('org',',','count',',','count_to_upscale',',','tier0_count',',','tier1_count',',','tier2_count',',','tier3_count',',','out_tier0',',','out_tier1',',','out_tier2',',','out_tier3')


to_remove = []
for org in orglist:
    directory = "/data/data1/users/ksismanis/testoai/" + str(org)
    tdir = "/data/data1/users/ksismanis/testoai/to.upscale/" + str(org)
    # outdir = '/data/data1/users/ksismanis/testoai/efha_upscaled/output_renamed'+ str(org)
    # # path = os.path.join(parent_dir, directory)
    # try:
    #     os.mkdir(tdir)
    # except OSError as error:
    #     print(error)
    # print(directory)
    # nprint(tdir)
    count  = 0 
    count_to_upscale  = 0
    count_to_upscalee = 0
    sizes = []
    tier0 = 0
    tier1 = 0
    tier2 = 0
    tier3 = 0
    out_tier0 = 0
    out_tier1 = 0 
    out_tier2 = 0
    out_tier3 = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # print(filename)
        if filename.endswith(".jpg") or filename.endswith(".JPEG") or filename.endswith(".0148jpg") or filename.endswith("0393jpg") or filename.endswith("jpg") or filename.endswith("JPG"): 
            imagefile = os.path.join(directory, filename)
            count = count+1
            try:
                im = Image.open(imagefile)
            except Exception:
                # print(filename)
                pass
            width, height = im.size
            size = width *  height

            # if width * height < 420000:
            #     count_to_upscalee = count_to_upscalee + 1
            # if width * height == 420000:
            #     to_remove.append((org,filename))   
            
            double = size * 4
            if size < 420000:
                count_to_upscale = count_to_upscale + 1
            if size < 100000:
                tier0 = tier0 + 1
            elif size >= 100000 and size < 420000:
                tier1 = tier1 + 1
            elif size >= 420000 and size < 950000:
                tier2 = tier2 + 1
            elif  size >= 950000:
                tier3 = tier3 + 1
            if double < 100000:
                out_tier0 = out_tier0 + 1
            elif double >= 100000 and double < 420000:
                out_tier1 = out_tier1 + 1
            elif double >= 420000 and double < 950000:
                out_tier2 = out_tier2 + 1
            elif  double >= 950000:
                out_tier3 = out_tier3 + 1


                # print(filename,' ', im.size)

                # shutil.copyfile(imagefile, os.path.join(tdir, filename))
                #copy to same dirname_to_upscale/
            continue
        else:
            continue
            # print(filename)
    
    # print('org','count','count_to_upscale','tier0_count','tier1_count')
    # print(org,',',count,',',count_to_upscale,',',count_to_upscalee,',',tier0,',',tier1,',',out_tier0,',',out_tier1,',',out_tier2,',',out_tier3)

    print(org,',',count,',',count_to_upscale,',',tier0,',',tier1,',',tier2,',',tier3,',',out_tier0,',',out_tier1,',',out_tier2,',',out_tier3)# tdir = '/data/data1/users/ksismanis/testoai/to.upscale/'
# for cp,file in to_remove:
#     target  = os.path.join(tdir,str(cp),file)
#     print(cp, file,target)
#     os.remove(target)

print('---------------------------------------------------------')
print('-------------------------Output---------------------------')
for org in orglist:
    out_tier0 = 0
    out_tier1 = 0 
    out_tier2 = 0
    out_tier3 = 0
    count = 0
    outdir = '/data/data1/users/ksismanis/testoai/efha_upscaled/output_renamed/'+ str(org)
    # outdir = '/data/data1/users/ksismanis/testoai/'+ str(org)

    for file in os.listdir(outdir):
        count = count+1
        filename = os.fsdecode(file)
        if filename.endswith(".jpg") or filename.endswith(".JPEG") or filename.endswith(".0148jpg") or filename.endswith("0393jpg") or filename.endswith("jpg") or filename.endswith("JPG"): 
            imagefile = os.path.join(outdir, filename)
            # try:
            im = Image.open(imagefile)
            # except Exception:
                # pass
            width, height = im.size
            size = width *  height
            if size < 100000:
                    out_tier0 = out_tier0 + 1
            elif size >= 100000 and size < 420000:
                out_tier1 = out_tier1 + 1
            
            elif size >= 420000 and size < 950000:
                out_tier2 = out_tier2 + 1
            
            elif  size >= 950000:
                out_tier3 = out_tier3 + 1

    print(org,',',count,',',out_tier0,',',out_tier1,',',out_tier2,',',out_tier3)
