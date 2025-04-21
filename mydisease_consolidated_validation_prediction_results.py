
gliptins=[]
fs=open(r"gliptins.txt","r")
for line in fs:
    gliptins.append(line.strip())
fs.close()
print(len(gliptins))
count=0
l=[]
entities=[]
symb="`"
fs=open(r"FV_set.txt","r")
for line in fs:
    count+=1
    x=line.split(symb)
    l.append(len(x))
    entities.append(x[0])
    if count<=10:
       print(line)
fs.close()
print(count)
l=list(set(l))
print(l)
print(len(entities))

count=0
l=[]
symb="`"
fs=open(r"ID.txt","r")
for line in fs:
    count+=1
    x=line.split(symb)
    l.append(len(x))
    if count<=10:
       print(line)
fs.close()
print(count)
l=list(set(l))
print(l)




posi=5

synergy={}
symb="`"
count=0
#fs=open(r"gdrive/MyDrive/four-vgae/res_links_for_validation_PCOS_synergism_dp.txt","r")

fs=open(r"result_ss_tot_DDIs.txt","r")
for line in fs:
    count+=1
    if count==51:
       print(len(synergy.keys()))
    if count in range(52,5542):
       continue

    #if x[0]  in statins and x[1] in ah or x[1] in statins and x[0] in ah:
          #continue
    x=line.split(symb)
    ss=sorted((x[0],x[1]))
    s=""
    s=s+str(ss[0])+symb
    s=s+str(ss[1])+symb
    s=s.strip()
    if s in synergy.keys() and float(synergy[s])<float(x[posi]):
       synergy[s]=float(x[posi])
    if s not in synergy.keys():
       synergy[s]=float(x[posi])
fs.close()
print(len(synergy.keys()))

pcos={}
symb="`"
count=0
#fs=open(r"gdrive/MyDrive/four-vgae/res_links_for_validation_PCOS_synergism_dp.txt","r")

fs=open(r"result_pr_tot_DDIs.txt","r")
for line in fs:
    count+=1
    if count in range(52,5542):
       continue

    #if x[0]  in statins and x[1] in ah or x[1] in statins and x[0] in ah:
          #continue
    x=line.split(symb)
    ss=sorted((x[0],x[1]))
    s=""
    s=s+str(ss[0])+symb
    s=s+str(ss[1])+symb
    s=s.strip()
    if s in pcos.keys() and float(pcos[s])<float(x[posi]):
       pcos[s]=float(x[posi])
    if s not in pcos.keys():
       pcos[s]=float(x[posi])
fs.close()
print(len(pcos.keys()))



existence={}
symb="`"
count=0
#fs=open(r"gdrive/MyDrive/four-vgae/res_links_for_validation_PCOS_synergism_dp.txt","r")

fs=open(r"result_feasibility_tot_DDIs.txt","r")
for line in fs:
    count+=1
    if count in range(52,5542):
       continue

    #if x[0]  in statins and x[1] in ah or x[1] in statins and x[0] in ah:
          #continue
    x=line.split(symb)
    ss=sorted((x[0],x[1]))
    s=""
    s=s+str(ss[0])+symb
    s=s+str(ss[1])+symb
    s=s.strip()
    if s in existence.keys() and float(existence[s])<float(x[posi]):
       existence[s]=float(x[posi])
    if s not in existence.keys():
       existence[s]=float(x[posi])
fs.close()
print(len(existence.keys()))




count=0
cc=0
dd=0
ff=0
val=0
ppcos=0
pot_pcos=0
novel=0
cd=0
#fv=open(r"gdrive/MyDrive/validated_interactions.txt","w")
#ft=open(r"gdrive/MyDrive/novel_predictions.txt","w")
fs=open(r"validation_results_consolidated.txt","w")
for gh in pcos.keys():
    count+=1
    a=pcos[gh]
    b=existence[gh]
    c=synergy[gh]
    #d=sensitivity[gh]
    s=""
    s=s+gh
    s=s+str(a)+symb
    s=s+str(b)+symb
    s=s+str(c)+symb
    #s=s+str(d)+symb
    f=float((a+b+c)/3)
    s=s+str(f)
    s=s.strip()
    sgh=gh.split(symb)
    if count==50:
       print("both drugs PCOS",count,cc,dd,ff)
    if sgh[0] in gliptins or sgh[1] in gliptins:
       #print(s)
       cd+=1
    if round(f,4)>=0.5:
       cc+=1
       #print(s)
    if round(f,4)>=0.8:
       dd+=1
    if round(f,4)>=0.9:
       ff+=1
       if count in range(1,52):
          ppcos+=1
          #print(s)
       elif count in range(52,2692):
          pot_pcos+=1
       else:
          novel+=1
    #if count<=10:
       #print(s)
    fs.write(s)
    fs.write("\n")
fs.close()
#ft.close()
#fv.close()
print(count,cc,dd,ff,cd)
print(ppcos, pot_pcos,novel)
print(ppcos+pot_pcos)

synergy={}
symb="`"
count=0
#fs=open(r"gdrive/MyDrive/four-vgae/res_links_for_validation_PCOS_synergism_dp.txt","r")

#fs=open(r"gdrive/MyDrive/vgae-dpp4-inhibitors/result_ss_pot_pcos_DDI_for_validation.txt","r")
fs=open(r"result_ss_tot_DDIs.txt","r")
for line in fs:
    count+=1
    if count not in range(52,5542):
       continue
    x=line.split(symb)
    ss=sorted((x[0],x[1]))
    s=""
    s=s+str(ss[0])+symb
    s=s+str(ss[1])+symb
    s=s.strip()
    if s in synergy.keys() and float(synergy[s])<float(x[posi]):
       synergy[s]=float(x[posi])
    if s not in synergy.keys():
       synergy[s]=float(x[posi])
fs.close()
print(len(synergy.keys()))




pcos={}
symb="`"
count=0
#fs=open(r"gdrive/MyDrive/four-vgae/res_links_for_validation_PCOS_synergism_dp.txt","r")

#fs=open(r"gdrive/MyDrive/vgae-dpp4-inhibitors/result_ss_pot_pcos_DDI_for_validation.txt","r")
fs=open(r"result_pr_tot_DDIs.txt","r")
for line in fs:
    count+=1
    if count not in range(52,5542):
       continue
    x=line.split(symb)
    ss=sorted((x[0],x[1]))
    s=""
    s=s+str(ss[0])+symb
    s=s+str(ss[1])+symb
    s=s.strip()
    if s in pcos.keys() and float(pcos[s])<float(x[posi]):
       pcos[s]=float(x[posi])
    if s not in pcos.keys():
       pcos[s]=float(x[posi])
fs.close()
print(len(pcos.keys()))



existence={}
symb="`"
count=0
#fs=open(r"gdrive/MyDrive/four-vgae/res_links_for_validation_PCOS_synergism_dp.txt","r")

#fs=open(r"gdrive/MyDrive/vgae-dpp4-inhibitors/result_ss_pot_pcos_DDI_for_validation.txt","r")
fs=open(r"result_feasibility_tot_DDIs.txt","r")
for line in fs:
    count+=1
    if count not in range(52,5542):
       continue
    x=line.split(symb)
    ss=sorted((x[0],x[1]))
    s=""
    s=s+str(ss[0])+symb
    s=s+str(ss[1])+symb
    s=s.strip()
    if s in existence.keys() and float(existence[s])<float(x[posi]):
       existence[s]=float(x[posi])
    if s not in existence.keys():
       existence[s]=float(x[posi])
fs.close()
print(len(existence.keys()))




count=0
cc=0
dd=0
ff=0
val=0
ppcos=0
pot_pcos=0
novel=0
#fv=open(r"gdrive/MyDrive/validated_interactions.txt","w")
#ft=open(r"gdrive/MyDrive/novel_predictions.txt","w")
fs=open(r"prediction_results_consolidated.txt","w")
for gh in pcos.keys():
    count+=1
    a=pcos[gh]
    b=existence[gh]
    c=synergy[gh]
    #d=sensitivity[gh]
    s=""
    s=s+gh
    s=s+str(a)+symb
    s=s+str(b)+symb
    s=s+str(c)+symb
    #s=s+str(d)+symb
    f=float((a+b+c)/3)
    s=s+str(f)
    s=s.strip()
    sgh=gh.split(symb)
    #if count in range(1,52):
    if sgh[0] in gliptins or sgh[1] in gliptins:
       print(s)
    if f>=0.5:
       cc+=1
    if f>=0.8:
       dd+=1
    if f>=0.9:
       ff+=1
       if count in range(1,52):
          ppcos+=1
          #print(s)
       elif count in range(52,2692):
          pot_pcos+=1
       else:
          novel+=1
    #if count<=10:
       #print(s)
    fs.write(s)
    fs.write("\n")
fs.close()
#ft.close()
#fv.close()
print(count,cc,dd,ff)
print(ppcos, pot_pcos,novel)
print(ppcos+pot_pcos)


drg=[]
fs=open(r"TWS_drugs.txt","r")
for line in fs:
    drg.append(line.strip())
fs.close()
print(len(drg))
pcos=[]
fs=open(r"all-drugs-PCOS-a.txt","r")
for line in fs:
    pcos.append(line.strip())
fs.close()
pcos=list(set(pcos))
print(len(pcos))
print(len(set(pcos).difference(set(entities))))



count=0
symb="`"
drg_pro=[]
fs=open(r"ID.txt","r")
for line in fs:
    count+=1
    x=line.split(symb)
    if x[0].startswith("drug") and x[1].startswith("prot"):
       drg_pro.append(line.strip())
fs.close()

drg_pro=list(set(drg_pro))
print(len(drg_pro))

nov_drg_dic={}
for line in drg_pro:
    x=line.split(symb)
    if x[0] in nov_drg_dic.keys():
          temp=nov_drg_dic[x[0]]
          temp.append(x[1])
          nov_drg_dic[x[0]]=temp
    else:
          nov_drg_dic[x[0]]=[x[1]]
print(len(nov_drg_dic.keys()))




count=0
#val=[]
#pos=30
done=[]
GI_absorption=[]
BBB_permeant=[]
Pgp_substrate=[]
CYP1A2_inhibitor=[]
CYP2C19_inhibitor=[]
CYP2C9_inhibitor=[]
CYP2D6_inhibitor=[]
CYP3A4_inhibitor=[]
log_kp=[]
lipinski_violations=[]
ghose_violations=[]
veber_violations=[]
egan_violations=[]
muegge_violations=[]
bioavailability=[]
PAINS=[]
Brenk=[]
leadlikeness=[]
synthetic_accessibility=[]
symb="`"
dif=[]
dif_dic={}
violations=[]
entities=[]
smiles_dic={}
fs=open(r"consolidated_ADME_properties_a.txt","r")
for line in fs:
    count+=1
    print(line.strip())
    x=line.split(symb)
    done.append(x[0])
    if float(x[39])>1:
       violations.append(x[0])
    for i in range(40,44):
        if float(x[i])!=0:
           violations.append(x[0])
    #for i in [45,46,47]:
       #if float(x[i])!=0:
         #violations.append(x[0])
    entities.append(x[0])
    smiles_dic[x[0]]=x[1]
    s=""
    for i in range(30,49):
        s=s+str(x[i])+symb
    s=s.strip()
    print(s)
    if x[30].strip()=='High':
       x[30]=1
    else:
       x[30]=0
    for i in range(31,33):
       if x[i]=='Yes':
          x[i]=1
       else:
          x[i]=0
    for i in range(33,38):
       if x[i]=='Yes':
          x[i]=0
       else:
          x[i]=1
    for i in [39,40,41,42,43,47]:
       if int(x[i])==0:
          x[i]=1
       else:
          x[i]=1-0.1*int(x[i])
    for i in [45,46]:
       if int(x[i])==0:
          x[i]=0
       else:
          x[i]=0.1*int(x[i])
    x[48]=(10-float(x[48]))*0.1
    temp=""
    for i in range(30,49):
        temp=temp+str(x[i])+symb
    temp=temp.strip()
    tot=0
    for i in range(30,49):
        tot=tot+float(x[i])
    dif.append(tot)
    dif_dic[tot]=x[0]

    GI_absorption.append(x[30])
    BBB_permeant.append(x[31])
    Pgp_substrate.append(x[32])
    CYP1A2_inhibitor.append(x[33])
    CYP2C19_inhibitor.append(x[34])
    CYP2C9_inhibitor.append(x[35])
    CYP2D6_inhibitor.append(x[36])
    CYP3A4_inhibitor.append(x[37])
    log_kp.append(x[38])
    lipinski_violations.append(x[39])
    ghose_violations.append(x[40])
    veber_violations.append(x[41])
    egan_violations.append(x[42])
    muegge_violations.append(x[43])
    bioavailability.append(x[44])
    PAINS.append(x[45])
    Brenk.append(x[46])
    leadlikeness.append(x[47])
    synthetic_accessibility.append(x[48])
    #if count<=10:
    print(temp)
    print(tot)
    #print(x[pos])
fs.close()
print(count)
print(GI_absorption)
print(BBB_permeant)
print(Pgp_substrate)
print(CYP1A2_inhibitor)
print(CYP2C19_inhibitor)
print(CYP2C9_inhibitor)
print(CYP2D6_inhibitor)
print(CYP3A4_inhibitor)
print(log_kp)
print(lipinski_violations)
print(ghose_violations)
print(veber_violations)
print(egan_violations)
print(muegge_violations)
print(bioavailability)
print(PAINS)
print(Brenk)
print(leadlikeness)
print(synthetic_accessibility)
dif=list(set(dif))
print(len(dif))
print(dif[0])
dif=sorted(dif, reverse=True)
for i in dif:
    print(dif_dic[i],i)
violations=list(set(violations))
for i in entities:
    if i not in violations:
       print(i)
       print(smiles_dic[i])
       print("\n")
print(len(violations))
#print(len(set(violations).difference(set(protox))))

derived=[]
fs=open(r"finalised_swisssimilarity_a.txt","r")
for line in fs:
    for g in gliptins:
        s=""
        s=s+str(g)+symb
        s=s+str(line.strip())+symb
        s=s.strip()
        derived.append(s)
        t=""
        t=t+str(line.strip())+symb
        t=t+str(g)+symb
        t=t.strip()
        derived.append(t)
fs.close()
derived=list(set(derived))
print(len(derived))

already=[]
fs=open(r"pcos-DDI-for-validation-a.txt","r")
for line in fs:
    x=line.split(symb)
    s=""
    s=s+x[1]+symb
    s=s+x[0]+symb
    s=s.strip()
    already.append(line.strip())
    already.append(s)
fs.close()
already=list(set(already))
print(len(already))

pot=[]
fs=open(r"pot-pcos-DDI-for-validation-a.txt","r")
for line in fs:
    x=line.split(symb)
    s=""
    s=s+x[1]+symb
    s=s+x[0]+symb
    s=s.strip()
    pot.append(line.strip())
    pot.append(s)
fs.close()
pot=list(set(pot))
print(len(pot))

symb="`"
count=0
pcos_dic={}
c=0
noteds=[]
d=0
e=0
f=0
g=0
not_done=[]
entry_dict={}
perf_dict={}
#fv=open(r"gdrive/MyDrive/metformin_interactions_all_SSSPF.txt","w")
ft=open(r"gliptin_interactions_final.txt","w")
fs=open(r"prediction_results_consolidated.txt","r")
for line in fs:
    count+=1
    x=line.split(symb)
    s=""
    s=s+x[0]+symb
    s=s+x[1]+symb
    s=s.strip()
    if s not in already and s not in pot and s not in derived:
       continue
    if float(x[5])<0.5:
       continue
    d+=1
    if x[0] not in nov_drg_dic.keys() or x[1] not in nov_drg_dic.keys():
       continue
    e+=1
    if x[0] in drg  or x[1] in drg:
       continue
    f+=1
    #print(line)
    if x[0] in gliptins or x[1] in gliptins:
       #print(line)
       #print(id_name[x[0]],id_name[x[1]])
       c+=1


       if x[0] not in violations and x[1] not in violations:
          g+=1
          idlist=""
          idlist=idlist+str(x[0])+symb
          idlist=idlist+str(x[1])+symb
          idlist=idlist.strip()
          entry_dict[idlist]=line.strip()
          perf_dict[idlist]=x[5]
          noteds.append(x[0])
          noteds.append(x[1])
          ft.write(line.strip())
          ft.write("\n")
       
    if x[0] in pcos:
       if x[0] in pcos_dic.keys():
          pcos_dic[x[0]]+=1
       else:
          pcos_dic[x[0]]=1
    if x[1] in pcos:
       if x[1] in pcos_dic.keys():
          pcos_dic[x[1]]+=1
       else:
          pcos_dic[x[1]]=1
     #if count<=10:
       #print(line)
fs.close()
print(len(pcos_dic.keys()))
print("gliptin containing safe interactions",c)
print("gliptin-based refined safe interactions",g)
noteds=list(set(noteds))
print(len(noteds))
ft.close()
#fv.close()
print(c,d,e,f)
#print("final existing safe interactions involving Saxagliptin",c)
not_done=list(set(not_done))
print(len(not_done))
for i in not_done:
    print(i)



count=0
symb="`"
drug_simi={}
fs=open(r"consolidated_swisssimilarity_validation_data_a.txt","r")
for line in fs:
    count+=1
    x=line.split(symb)
    if x[0] in drug_simi.keys():
       if float(x[1])>drug_simi[x[0]]:
          drug_simi[x[0]]=float(x[1])
    else:
       if x[1]!="":
          drug_simi[x[0]]=float(x[1])
    if count<=10:
       print(line)
fs.close()
print(count)
print(len(drug_simi.keys()))

tot=0
pot_ddi=0
derived_ddi=0
finalised=0
#fs=open(r"gdrive/MyDrive/PCOS-DDI-fet-adj/gliptin_interactions_final.txt","w")
for p in perf_dict.keys():
       tot+=1
       if p in pot:
             pot_ddi+=1
             finalised+=1
             twoids=p.split(symb)
             print("repurposed",p,twoids[0], twoids[1], perf_dict[p])
             #fs.write(str(entry_dict[p]))
             #fs.write("\n")
       elif p in derived:
          twoids=p.split(symb)
          otherid=""
          if twoids[0] in gliptins:
             otherid=twoids[1]
          if twoids[1] in gliptins:
             otherid=twoids[0]
          if float(drug_simi[otherid])>=0.9:
             finalised+=1
             derived_ddi+=1
             print("derived",p,twoids[0], twoids[1], drug_simi[otherid],perf_dict[p])
             print(entry_dict[p])
             #fs.write(str(entry_dict[p]))
             #fs.write("\n")
print(tot,finalised, pot_ddi,derived_ddi)
#fs.close()

noteds=list(set(noteds))
for y in noteds:
    if y not in gliptins:
        print(y)
print(len(noteds))