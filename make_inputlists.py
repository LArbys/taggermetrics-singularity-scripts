import os,sys
sys.argv.append("-b")
import ROOT as rt

# MCC8 nue+MC cosmic: Tufts
#LARCV_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8/nue_intrinsics_fid10/supera"
#LARLITE_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8/nue_intrinsics_fid10/larlite"
#TAGGER_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8/nue_intrinsics_fid10/out_week0619/tagger"

# MCC8.1 nue+MC cosmic: Tufts
#LARCV_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/supera"
#LARLITE_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/larlite"
#TAGGER_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/out_week071017/tagger"

# MCC8 numu+MC cosmic
#LARCV_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/supera"
#LARLITE_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/larlite"
#TAGGER_SOURCE="/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/tagger"

# MCC8.1 numu_MC cosmic: MacCaffrey
LARCV_SOURCE="/home/taritree/larbys/data/mcc8.1/numu_1muNpfiltered/supera"
LARLITE_SOURCE="/home/taritree/larbys/data/mcc8.1/numu_1muNpfiltered/larlite"
TAGGER_SOURCE="/home/taritree/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/tagger"

# We parse folder contents for larcv and larlite files
# We keep them in a dictionary
job_dict = {} # key=jobid, value=dict{"larlite":[],"larcv":[]}

# PARSE LARCV_SOURCE
files = os.listdir(LARCV_SOURCE)
for f in files:
    f = f.strip()
    if ".root" not in f or "larcv" not in f:
        continue
    fpath = LARCV_SOURCE + "/" + f
    fileid = int(f.split(".")[-2].split("_")[-1])
    #print f.strip(),fileid
    if fileid not in job_dict:
        job_dict[fileid] = {"larcv":[],"larlite":[],"taggerlarcv":[],"taggerlarlite":[]}
    job_dict[fileid]["larcv"].append(fpath)

# PARSE LARLITE_SOURCE
files = os.listdir(LARLITE_SOURCE)
for f in files:
    f = f.strip()
    if ".root" not in f or "larlite" not in f:
        continue
    fpath = LARLITE_SOURCE + "/" + f
    fileid = int(f.split(".")[-2].split("_")[-1])
    #print f.strip(),fileid
    if fileid not in job_dict:
        continue
    job_dict[fileid]["larlite"].append(fpath)

# PARSE TAGGER OUTPUT FILES
files = os.listdir(TAGGER_SOURCE)
for f in files:
    f = f.strip()
    if ".root" not in f:
        continue
    try:
        fileid = int(f.split(".")[-2].split("_")[-1])
    except:
        print "[WARNING] Couldn't parse tagger output file ",f

    fpath = TAGGER_SOURCE + "/" + f
    rfile = rt.TFile(fpath)

    
    if "larlite" in f:
        job_dict[fileid]["taggerlarlite"].append(fpath)
    elif "larcv" in f:
        try:
            croitree = rfile.Get("partroi_croi_tree")
            nentries = croitree.GetEntries()
            print "Tagger larcv file entries: ",nentries
            job_dict[fileid]["taggerlarcv"].append(fpath)
        except:
            print "[WARNING] Error with tagger larcv file",f
    else:
        raise RuntimeError("Weird file. Could not classify: %s"%(f))


fileid_list = job_dict.keys()
fileid_list.sort()

jobidlist = open("jobidlist.txt",'w')
badidlist = open("bad_jobidlist.txt",'w')

combined_src_larcv = open("input_src_larcv.txt",'w')
combined_src_larlite = open("input_src_larlite.txt",'w')
combined_tagger_larcv = open("input_tagger_larcv.txt",'w')
combined_tagger_larlite = open("input_tagger_larlite.txt",'w')

os.system("mkdir -p inputlists")
os.system("rm -f inputlists/*")
for jobid,fileid in enumerate(fileid_list):

    if len(job_dict[fileid]["taggerlarcv"])==0:
        print >> badidlist,fileid
        continue

    flarcv = open("inputlists/input_src_larcv_%04d.txt"%(fileid),'w')
    for f in job_dict[fileid]["larcv"]:
        print >> flarcv,f
        print >> combined_src_larcv,f
    flarcv.close()

    flarlite = open("inputlists/input_src_larlite_%04d.txt"%(fileid),'w')
    for f in job_dict[fileid]["larlite"]:
        if "simch" in f:
            continue
        print >> flarlite,f
        print >> combined_src_larlite,f
    flarlite.close()

    flarcv = open("inputlists/input_tagger_larcv_%04d.txt"%(fileid),'w')
    for f in job_dict[fileid]["taggerlarcv"]:
        print >> flarcv,f
        print >> combined_tagger_larcv,f
    flarcv.close()

    flarlite = open("inputlists/input_tagger_larlite_%04d.txt"%(fileid),'w')
    for f in job_dict[fileid]["taggerlarlite"]:
        print >> flarlite,f
        print >> combined_tagger_larlite,f
    flarlite.close()
    
    print >> jobidlist,fileid

jobidlist.close()
badidlist.close()
combined_src_larcv.close()
combined_src_larlite.close()
combined_tagger_larcv.close()
combined_tagger_larlite.close()
