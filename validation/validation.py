from treetoreads import TreeToReads
import dendropy
from dendropy.calculate import treecompare
import os
import subprocess


def perform_sims(config, dirstub, num):
    for i in range(num):
        i+=1
        ttr=TreeToReads(configfi=config,run=0)
        diri = "{}{}".format(dirstub,i)
        if not os.path.exists(diri):
          os.makedirs(diri) 
        ttr.outd = diri
        ttr.run_art()



def run_snppipe(dirstub, refloc, num):
    for i in range(num):
        i+=1
        diri = "{}{}".format(dirstub,i)
        print "run_snp_pipeline.sh -s {}/fastq -o {} {}".format(diri, diri, refloc)
        os.system("run_snp_pipeline.sh -s {}/fastq -o {} {}".format(diri, diri, refloc)) 




def perform_analyses(dirstub, num):
    inf_dict = {'Euclidean':[],
                       'RF':[],
                       'MutsSim':[],
                       'MutsCalled':[],
                       'freqA':[],
                       'freqC':[],
                       'freqG':[],
                       'freqT':[],
                       'ac':[],
                       'ag':[],
                       'at':[],
                       'cg':[],
                       'ct':[],
                       'gt':[]}
    for i in range(num):
        i+=1
        diri = "{}{}".format(dirstub,i)
        #diri = "{}{}/altref".format(dirstub,i)
        cwd = os.getcwd()
        os.chdir(diri)
        os.system("raxmlHPC -m ASC_GTRGAMMA --asc-corr=lewis -s snpma.fasta -p 1 -n val")
#        os.system("raxmlHPC -m GTRGAMMA -s snpma.fasta -p 1 -n val_noasc")
        os.chdir(cwd)
        print diri
        trestr =open("{}/RAxML_bestTree.val".format(diri)).readline().replace('sim_','')
#        trestr =open("{}/RAxML_bestTree.val_noasc".format(diri)).readline().replace('sim_','')
        tns = dendropy.TaxonNamespace()
        inputtree = dendropy.Tree.get_from_path("{}/scaledtree.tre".format(diri), 
                                                schema="newick", 
                                                taxon_namespace=tns)
        inferred = dendropy.Tree.get_from_string(trestr, 
                                               schema="newick",
                                               taxon_namespace=tns)
        inputtree.encode_bipartitions()
        inferred.encode_bipartitions()
        inf_dict['Euclidean'].append(treecompare.euclidean_distance(inputtree, inferred))
        inf_dict['RF'].append(treecompare.unweighted_robinson_foulds_distance(inputtree, inferred))
        freqs = subprocess.check_output(["grep", "Base frequencies:","{}/RAxML_info.val".format(diri)]).split()
#        freqs = subprocess.check_output(["grep", "Base frequencies:","{}/RAxML_info.val_noasc".format(diri)]).split()
        print(freqs)
        freqs = [float(val) for val in freqs[2:]]
        inf_dict['freqA'].append(freqs[0])
        inf_dict['freqC'].append(freqs[1])
        inf_dict['freqG'].append(freqs[2])
        inf_dict['freqT'].append(freqs[3])
        trans = subprocess.check_output(["grep", "ac ag at cg ct gt",  "{}/RAxML_info.val".format(diri)]).split()
#        trans = subprocess.check_output(["grep", "ac ag at cg ct gt",  "{}/RAxML_info.val_noasc".format(diri)]).split()
        trans = [float(val) for val in trans[9:]]
        inf_dict['ac'].append(trans[0])
        inf_dict['ag'].append(trans[1])
        inf_dict['at'].append(trans[2])
        inf_dict['cg'].append(trans[3])
        inf_dict['ct'].append(trans[4])
        inf_dict['gt'].append(trans[5])
        inf_dict['MutsCalled'].append(float(subprocess.check_output(["wc","{}/snplist.txt".format(diri)]).split()[0]))
        inf_dict['MutsSim'].append(float(subprocess.check_output(["wc","{}/mutsites.txt".format(diri)]).split()[0]))
    for key in inf_dict:
            mean = sum(inf_dict[key])/len(inf_dict[key])
            print(key)
            print(mean)
    return(inf_dict)


def perform_analyses_altref(dirstub, num):
    inf_dict = {'Euclidean':[],
                       'RF':[],
                       'MutsSim':[],
                       'MutsCalled':[],
                       'freqA':[],
                       'freqC':[],
                       'freqG':[],
                       'freqT':[],
                       'ac':[],
                       'ag':[],
                       'at':[],
                       'cg':[],
                       'ct':[],
                       'gt':[]}
    for i in range(num):
        i+=1
        odiri = "{}{}".format(dirstub,i)
        diri = "{}{}/altref".format(dirstub,i)
        cwd = os.getcwd()
        os.chdir(diri)
#        os.system("raxmlHPC -m ASC_GTRGAMMA --asc-corr=lewis -s snpma.fasta -p 1 -n val")
        os.system("raxmlHPC -m GTRGAMMA -s snpma.fasta -p 1 -n val_noasc")
        os.chdir(cwd)
        print diri
#        trestr =open("{}/RAxML_bestTree.val".format(diri)).readline().replace('sim_','')
        trestr =open("{}/RAxML_bestTree.val_noasc".format(diri)).readline().replace('sim_','')
        tns = dendropy.TaxonNamespace()
        inputtree = dendropy.Tree.get_from_path("{}/scaledtree.tre".format(odiri), 
                                                schema="newick", 
                                                taxon_namespace=tns)
        inferred = dendropy.Tree.get_from_string(trestr, 
                                               schema="newick",
                                               taxon_namespace=tns)
        inputtree.encode_bipartitions()
        inferred.encode_bipartitions()
        inf_dict['Euclidean'].append(treecompare.euclidean_distance(inputtree, inferred))
        inf_dict['RF'].append(treecompare.unweighted_robinson_foulds_distance(inputtree, inferred))
#        freqs = subprocess.check_output(["grep", "Base frequencies:","{}/RAxML_info.val".format(diri)]).split()
        freqs = subprocess.check_output(["grep", "Base frequencies:","{}/RAxML_info.val_noasc".format(diri)]).split()
        print(freqs)
        freqs = [float(val) for val in freqs[2:]]
        inf_dict['freqA'].append(freqs[0])
        inf_dict['freqC'].append(freqs[1])
        inf_dict['freqG'].append(freqs[2])
        inf_dict['freqT'].append(freqs[3])
#        trans = subprocess.check_output(["grep", "ac ag at cg ct gt",  "{}/RAxML_info.val".format(diri)]).split()
        trans = subprocess.check_output(["grep", "ac ag at cg ct gt",  "{}/RAxML_info.val_noasc".format(diri)]).split()
        trans = [float(val) for val in trans[9:]]
        inf_dict['ac'].append(trans[0])
        inf_dict['ag'].append(trans[1])
        inf_dict['at'].append(trans[2])
        inf_dict['cg'].append(trans[3])
        inf_dict['ct'].append(trans[4])
        inf_dict['gt'].append(trans[5])
        inf_dict['MutsCalled'].append(float(subprocess.check_output(["wc","{}/snplist.txt".format(diri)]).split()[0]))
        inf_dict['MutsSim'].append(float(subprocess.check_output(["wc","{}/mutsites.txt".format(odiri)]).split()[0]))
    for key in inf_dict:
            mean = sum(inf_dict[key])/len(inf_dict[key])
            print(key)
            print(mean)
    return(inf_dict)

def check_indel_locs(workdir, prefix):
    os.system("cat {}/fasta_files/*_indel.fasta > {}/sim.aln".format(workdir, workdir))
    inferred_indel_dict = {}
    input_indel_dict = {}
    seqname = ''
    i = 0
    with open('{}/sim.aln'.format(workdir), 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if line.startswith('>'):
                seqname = line.lstrip('>').replace(prefix, '')
                inferred_indel_dict[seqname] = []
                i = 0
            else:
                for nuc in line:
                    i+=1
                    if nuc == '-':
                      inferred_indel_dict[seqname].append(i)
    imax = i
    with open('{}/TTRindelible_TRUE.fas'.format(workdir), 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if line.startswith('>'):
                print line
                seqname = line.lstrip('>')
                input_indel_dict[seqname] = []
                i = 0
            else:
                for nuc in line:
                    i+=1
                    if nuc == '-':
                        input_indel_dict[seqname].append(i)
                    if i >= imax:
                      break
    if set(input_indel_dict.keys()) != set(inferred_indel_dict.keys()):
         print  set(input_indel_dict.keys()) - set(inferred_indel_dict.keys())
         print  set(inferred_indel_dict.keys()) - set(input_indel_dict.keys())
    for key in input_indel_dict:
        if input_indel_dict[key] != inferred_indel_dict[key]:
          print key
          print input_indel_dict[key] 
          print inferred_indel_dict[key]




def collapse_short_analyses(dirstub, num):
    inf_dict = {'Euclidean':[],
                       'RF':[]}
    for i in range(num):
        i+=1
        diri = "{}{}".format(dirstub,i)
        tns = dendropy.TaxonNamespace()
        inputtree = dendropy.Tree.get_from_path("{}/scaledtree.tre".format(diri), 
                                                schema="newick", 
                                                taxon_namespace=tns)
        for edge in inputtree.postorder_edge_iter():
            if edge.length < 0.0000000001:
                edge.collapse()
        inferred = dendropy.Tree.get_from_string(trestr, 
                                               schema="newick",
                                               taxon_namespace=tns)
        for edge in inferredtree.postorder_edge_iter():
            if edge.length < 0.0000000001:
                edge.collapse()
        inputtree.encode_bipartitions()
        inferred.encode_bipartitions()
        inf_dict['Euclidean'].append(treecompare.euclidean_distance(inputtree, inferred))
        inf_dict['RF'].append(treecompare.unweighted_robinson_foulds_distance(inputtree, inferred))
    for key in inf_dict:
            mean = sum(inf_dict[key])/len(inf_dict[key])
            print(key)
            print(mean)
    return(inf_dict)



#perform_sims(dirstub = "validation/short_fix/run", refloc = "example/short_ref.fasta")
#perform_analyses("validation/short_fix/run")