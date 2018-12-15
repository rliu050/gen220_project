#!usr/bin/env python

import sys,getopt,re,os
print(sys.argv)

opts,args=getopt.getopt(sys.argv[1:],"i:o:g:p:f:s:l:")
infile=""
outfile=""
group=""
FDR=""
FC=""
s=""
gene_list=""

for op,value in opts:
	if op=="-s":
		s=value
	elif op=="-p":
		FDR=value
	elif op=="-o":
		outfile=value
def filter_group(group):
	with open (infile,'r') as f:
		first_line=f.readline()
		first_line=first_line.strip("\n")
		fl=first_line.split("\t")
		i=0
		col=[0]
		for str in fl:
			m=re.search(group,str)
			if m:
				col.append(i)
			i+=1
	g_file_name=group+".txt"
	g_file=open(g_file_name,"w")
	with open (infile, 'r') as f:	
		for line in f:
			line=line.strip("\n")
			line=line.split('\t')
			line_f=[]
			for n in col:
				line_f.append(line[n])
			line_f="\t".join(line_f)
			g_file.write(line_f)
			g_file.write("\n")
			

def filter_FDR(FDR):
	g_file_name=group+".txt"
	with open (g_file_name,'r') as f:
		first_line=f.readline()
		first_line=first_line.strip("\n")
		fl=first_line.split("\t")
		i=0
		col=[]
		for str in fl:
			m=re.search("FDR",str)
			if m:
				col.append(i)
			i+=1
	fdr_filter=[]
	with open (g_file_name,'r') as f:
		line_num=0
		for line in f:
			line_num+=1
			if (line_num!=1):
				line=line.strip("\n")
				line_n=line.split("\t")
				a=line_n[col[0]]
				if a!='NA':
					a=float(a)
					FDR_f=float(FDR)
					if a<FDR_f:
						fdr_filter.append(line_n)
	if s=="1":
		# print(s)
		fdr_s_filter=sorted(fdr_filter,key=lambda fdr_filter:fdr_filter[col[0]])
		fdr_s_filter.insert(0,fl)
		fdr_file_name=group+"_s_FDR"+FDR+".txt"
		fdr_file=open(fdr_file_name,"w")
		for line in fdr_s_filter:
			line="\t".join(line)
			fdr_file.write(line)
			fdr_file.write("\n")
	else:
		fdr_filter.insert(0,fl)
		fdr_file_name=group+"_FDR"+FDR+".txt"
		fdr_file=open(fdr_file_name,"w")
		for line in fdr_filter:
			line="\t".join(line)
			fdr_file.write(line)
			fdr_file.write("\n")


def filter_FC(FC):
	fc_infile_name=group+".txt"
	if not FDR=="":
		if s=="1":
			fc_infile_name=group+"_s_FDR"+FDR+".txt"
		else:
			fc_infile_name=group+"_FDR"+FDR+".txt"
	with open (fc_infile_name,"r") as f:
		first_line=f.readline()
		first_line=first_line.strip("\n")
		fl=first_line.split("\t")
		i=0
		col=[]
		for str in fl:
			m=re.search("logFC",str)
			if m:
				col.append(i)
			i+=1
	fc_filter=[]
	with open (fc_infile_name,'r') as f:
		line_num=0
		for line in f:
			line_num+=1
			if (line_num!=1):
				line=line.strip("\n")
				line_n=line.split("\t")
				a=line_n[col[0]]
				if a!='NA':
					a=float(a)
					FC_f=float(FC)
					if (FC_f>0):
						a_e=2**a
						if a_e>FC_f:
							fc_filter.append(line_n)
					else:
						a_e=-1/(2**a)
						if a_e<FC_f:
							fc_filter.append(line_n)
	if s=="1":
		fc_s_filter=sorted(fc_filter,key=lambda fc_filter:fc_filter[col[0]])
		fc_s_filter.reverse()
		fc_s_filter.insert(0,fl)
		fc_file_name="FC"+FC+"_"+fc_infile_name
		fc_file=open(fc_file_name,"w")
		for line in fc_s_filter:
			line="\t".join(line)
			fc_file.write(line)
			fc_file.write("\n")
	else:
		fc_filter.insert(0,fl)
		fc_file_name="FC"+FC+"_"+fc_infile_name
		fc_file=open(fc_file_name,"w")
		for line in fc_filter:
			line="\t".join(line)
			fc_file.write(line)
			fc_file.write("\n")					


	#fc_infile_name=""
	#fc_infile_name=group+".txt"
	#if os.path.exists(group+"_s_FDR"+FDR+".txt"):
	#	fc_infile_name=group+"_s_FDR"+FDR+".txt"
	#elif os.path.exists(group+"_FDR"+FDR+".txt"):
	#	fc_infile_name=group+"_FDR"+FDR+".txt"
	#else:
		#fc_infile_name=group+".txt"
	#print(fc_infile_name)


def filter_genes(gene_list):
	with open(gene_list,"r") as f:
		gene_f=[]
		for line in f:
			line=line.strip("\n")
			gene_f.append(line)
	gene_infile_name=infile
	if not group=="":
		gene_infile_name=group+".txt"
	with open(gene_infile_name,"r") as f:
		first_line=f.readline()
		fl=first_line.strip("\n")
		gene_filter=[]
		for line in f:
			line=line.strip("\n")
			line_split=line.split("\t")
			for str in gene_f:
				if str==line_split[0]:
					gene_filter.append(line)
	gene_filter.insert(0,fl)
	gene_file_name=outfile
	gene_file=open(gene_file_name,"w")
	for line in gene_filter:
		gene_file.write(line)
		gene_file.write("\n")		


for op,value in opts:
	if op=="-i":
		infile=value
	elif op=="-o":
		outfile=value
	elif op=="-g":
		group=value
		filter_group(group)
	elif op=="-p":
		FDR=value
		filter_FDR(FDR)
	elif op=="-f":
		FC=value
		filter_FC(FC)
	elif op=="-l":
		gene_list=value
		filter_genes(gene_list)






