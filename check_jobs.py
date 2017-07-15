import os,sys
import ROOT as rt

# Check job id list. Check output folder. Check that tagger output files have entries (and same number of entries)
# based on checks, will produce rerun list

# MCC8.1 nue+cosmic: tufts
#PIXANA_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/out_week071017/pixana_dilate"

# MCC8.1 nue+cosmics: maccaffery
#PIXANA_FOLDER="/home/taritree/larbys/data/mcc8.1/nue_1eNpfiltered/out_week0626/tagger"

# MCC8.1 nue only: tufts
#PIXANA_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_nocosmic_1eNpfiltered/out_week0626/tagger"

# MCC8.1 numu+cosmic: tufts
#PIXANA_FOLDER="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/tagger_dilate"

# MCC8.1 numu+cosmic: Mccaffrey
PIXANA_FOLDER="/home/taritree/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/pixana/"

files = os.listdir(PIXANA_FOLDER)

file_dict = {}
for f in files:
    f.strip()
    idnum = int(f.split("_")[-1].split(".")[0])
    if idnum not in file_dict:
        file_dict[idnum] = {"pixana":None}
    if "output_pixana" in f:
        file_dict[idnum]["pixana"] = PIXANA_FOLDER+"/"+f

ids = file_dict.keys()
ids.sort()

rerun_list = []
good_list = []
for fid in ids:
    try:
        rfile_larcv = rt.TFile( file_dict[fid]["pixana"] )
        tree = rfile_larcv.Get("pixana")
        nentries_larcv = tree.GetEntries()
        rfile_larcv.Close()
                
        if nentries_larcv==0:
            raise runtime_error("not the same")
        good_list.append(fid)
    except:
        rerun_list.append(fid)
        continue

print "Goodlist: ",len(good_list)
print "Rerunlist: ",len(rerun_list)

# read in jobidlist
fjobid = open("jobidlist.txt",'r')
ljobid = fjobid.readlines()
for l in ljobid:
    jobid = int(l.strip())
    if jobid in good_list or jobid in rerun_list:
        continue
    else:
        rerun_list.append(jobid)
fjobid.close()

print "Remaining: ",len(rerun_list)

frerun = open("rerunlist.txt",'w')
for jobid in rerun_list:
    print >> frerun,jobid
frerun.close()
