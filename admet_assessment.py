


gliptins=['drug_1098', 'drug_2689', 'drug_3184', 'drug_2649', 'drug_2508']

count=0
symb='`'
drug=[]
interactors={}
fs=open(r"gliptin_interactions_final_a.txt","r")
for line in fs:
    count+=1
    x=line.split(symb)
    if x[0] not in gliptins:
       drug.append(x[0])
    else:
       drug.append(x[1])
    if x[0] in gliptins:
       interactors[x[0]]=["NA"]
    else:
       if x[0] not in interactors.keys():
          temp=[]
          temp.append(x[1])
          interactors[x[0]]=temp
       else:
          temp=interactors[x[0]]
          temp.append(x[1])
          interactors[x[0]]=temp
    if x[1] in gliptins:
       interactors[x[1]]=["NA"]
    else:
       if x[1] not in interactors.keys():
          temp=[]
          temp.append(x[0])
          interactors[x[1]]=temp
       else:
          temp=interactors[x[1]]
          temp.append(x[0])
          interactors[x[1]]=temp
    if count<=10:
       print(line)
fs.close()
drug=list(set(drug))
drug=drug+gliptins
print(len(drug))
print(drug[0])
interactors["drug_3184"]=["NA"]
print(len(interactors.keys()))

count=0
drug_adme=[]
lipo=[]
fs=open(r"consolidated_ADME_properties_a.txt","r")
for line in fs:
    count+=1
    #print(line)
    x=line.split(symb)
    if x[0] in drug:
       print(line)
       lipo.append(float(x[17-1]))
       print(x[17-1],x[21-1],x[25-1],x[29-1],x[30-1],x[31-1],x[32-1],x[33-1],x[34-1],x[35-1],x[36-1],x[37-1],x[39-1],x[40-1],x[41-1],x[42-1],x[43-1])
       s=""
       s=s+str(x[0])+symb
       s=s+str(x[17-1])+symb
       s=s+str(x[21-1])+","+str(x[25-1])+","+str(x[29-1])+symb
       s=s+str(x[30-1])+symb
       s=s+str(x[31-1])+symb
       s=s+str(x[32-1])+symb
       s=s+str(x[33-1])+","+str(x[34-1])+","+str(x[35-1])+","+str(x[36-1])+","+str(x[37-1])+symb
       s=s+str(x[39-1])+","+str(x[40-1])+","+str(x[41-1])+","+str(x[42-1])+","+str(x[43-1])+symb
       s=s+str(x[45-1])+symb
       s=s+str(x[46-1])+symb
       s=s+str(x[47-1])+symb
       s=s.strip()
       drug_adme.append(s)
       print(s)
    #if count<=10:
       #print(line)fs.close()
print(count)
print(len(drug_adme))
max_lipo=max(lipo)
print("maximum lipophilicity observed",max_lipo)

count=0
symb="`"
adme_tot={}
BBB_spl=['drug_3322', 'drug_872', 'drug_277', 'drug_174', 'drug_511', 'drug_190', 'drug_2702', 'drug_835', 'drug_3182', 'drug_2660', 'drug_659', 'drug_2648', 'drug_2491']
#['Vortioxetine','Guanfacine','Triamterene','Olmesartan','Dexmedetomidine','Etomidate','Armodafinil','Ramelteon','Teriflunomide','Lacosamide', 'Primidone', 'Rufinamide', 'Tetrabenazine']
ft=open(r"ADME_properties_main_paper_a.txt","w")
#fs=open(r"gdrive/MyDrive/PCOS-DDI-fet-adj/ADMET_properties_main_paper.txt","r")
s=""
s=s+"Drug"+symb
s=s+"Lipophilicity"+symb
s=s+"Hydrophilicity"+symb
s=s+"GI absorption"+symb
s=s+"BBB-permeation"+symb
s=s+"P-gp substrate"+symb
s=s+"Enzyme inhibition"+symb
s=s+"Druglikeness"+symb
s=s+"PAINS alert"+symb
s=s+"BRENK alert"+symb
s=s+"Leadlikeness"+symb
#s=s+"Tox21 nuclear receptor signalling pathways"+symb
#s=s+"Tox21 stress response pathways"+symb
#s=s+"Molecular initiating events"+symb
s=s+"ADME score"+symb
s=s.strip()
ft.write(s)
ft.write("\n")
print(s)
for line in drug_adme:
    count+=1
    print(line)
    x=line.split(symb)
    print(len(x))
    tot=0
    temp=(float(x[1])/max_lipo)*1
    tot+=temp
    y=x[2].split(",")
    temp=0
    for i in range(3):
        if y[i]=='Insoluble':
           temp+=0.2
        if y[i]=='Poorly soluble':
           temp+=0.4
        if y[i]=='Moderately soluble':
           temp+=0.6
        if y[i]=='Soluble':
           temp+=0.8
        if y[i]=='Very soluble':
           temp+=0.9
        else:
           temp+=1
    temp=temp/3
    tot+=temp
    if x[3]=="High":
        tot+=1
    else:
        tot+=0
    if x[0] in BBB_spl and x[4]=="Yes":
        tot+=1
    elif x[0] not in BBB_spl and x[4]=="No":
        tot+=1
    else:
        tot+=0
    if x[5]=="No":
        tot+=1
    else:
        tot+=0
    y=x[6].split(",")
    temp=0
    for i in y:
        if i=="Yes":
           temp+=1
        else:
           temp+=0
    temp=temp/5
    tot+=temp
    y=x[7].split(",")
    temp=0
    for i in y:
        if i=="0":
           temp+=1
        else:
           temp+=0
    temp=temp/5
    tot+=temp
    if float(x[8])>=1:
       tot+=0
    else:
       tot+=1
    if float(x[9])>=1:
       tot+=0
    else:
       tot+=1
    if float(x[10])>=1:
       tot+=0
    else:
       tot+=1
    print("initial tot",tot)
    tot=round((tot/10)*100,4)
    print("normalised tot",tot)
    adme_tot[x[0]]=tot
    s=""
    s=s+line.strip()+str(tot)+symb
    ft.write(s)
    ft.write("\n")
    print(s)
    #if count<=10:
       #print(line)
#fs.close()
print(count)
ft.close()

count=0
symb="`"
tox_dic={}
ft=open(r"consolidated-toxicity_a.txt","r")
for line in ft:
    count+=1
    x=line.split(symb)
    print(line)
    tot=0
    s=""
    d=0
    for i in range(1,6):
        if float(x[i])>=0.5:
           d+=1
    s=s+str(d)+symb
    tot+=(d/5)
    d=0
    for i in range(6,14):
        if float(x[i])>=0.5:
           d+=1
    s=s+str(d)+symb
    tot+=(d/8)
    d=0
    for i in range(14,21):
        if float(x[i])>=0.5:
           d+=1
    s=s+str(d)+symb
    tot+=(d/7)
    d=0
    for i in range(21,26):
        if float(x[i])>=0.5:
           d+=1
    s=s+str(d)+symb
    tot+=(d/5)
    d=0
    for i in range(26,40):
        if float(x[i])>=0.5:
           d+=1
    s=s+str(d)+symb
    tot+=(d/14)
    s=s.strip()
    print("tot",tot)
    tot=round(((tot/5)*100),4)
    print("normalised tot",tot)
    s=s+str(adme_tot[x[0]])+symb
    s=s+str(tot)+symb
    admet=round(((tot+adme_tot[x[0]])/2),4)
    print("ADME",adme_tot[x[0]])
    print("ADMET",admet)
    s=s+str(admet)+symb
    partners=""
    for e in interactors[x[0]]:
        partners+=str(e)+","
    partners=partners[:-1]
    s=s+partners+symb
    print(s)
    tox_dic[x[0]]=s
ft.close()
print(count)
print(len(tox_dic.keys()))

fs=open(r"ADMET_properties_main_paper_a.txt","w")
s=""
s=s+"Drug"+symb
s=s+"Organ toxicity"+symb
s=s+"toxicity end points"+symb
s=s+"Tox21 nuclear receptor signalling pathways"+symb
s=s+"Tox21 stress response pathways"+symb
s=s+"Molecular initiating events"+symb
s=s+"ADME score"+symb
s=s+"Toxicity score"+symb
s=s+"ADMET score"+symb
s=s+"gliptins interactors"+symb
s=s.strip()
fs.write(s)
fs.write("\n")
print(s)
count=0
for d in tox_dic.keys():
    count+=1
    #print(d)
    #print(drug_adme[d])
    #print(tox_dic[d])
    s=""
    s=s+d+symb
    #s=s+str(drug_adme[d])
    s=s+str(tox_dic[d])
    s=s.strip()
    print(s)
    fs.write(s)
    fs.write("\n")
fs.close()
print(count)