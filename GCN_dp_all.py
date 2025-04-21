# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 21:17:17 2024

@author: HP
"""






import pandas as pd



import stellargraph as sg
from stellargraph.data import EdgeSplitter
from stellargraph.mapper import FullBatchLinkGenerator
from stellargraph.layer import GCN, LinkEmbedding
from tensorflow import keras
from sklearn import preprocessing, feature_extraction, model_selection

from stellargraph import globalvar
from stellargraph import datasets
from IPython.display import display, HTML
import matplotlib.pyplot as plt

#filename=r"reduced-df-drug-protein.txt"
#fadj=r"spl-drug-protein-adjacency-matrix_a.txt"
#flabel=r"edge_labelling_existence_drug_protein.txt"




filename=r"FV_set.txt"
fadj=r"ID.txt"
flabel=r"edge-labelling-feasibility.txt"
square_node_data=pd.read_csv(filename,sep="`",header=None,index_col=0)
symb="`"
source=[]
target=[]
weight=[]
nodes=[]
fs=open(filename,"r")
for line in fs:
    x=line.split(symb)
    nodes.append(x[0])
fs.close()
fs=open(fadj,"r")
for line in fs:
    x=line.split(symb)
    source.append(x[0])
    target.append(x[1])
    if x[0].startswith("drug") and x[1].startswith("drug"):
        weight.append(0.2)
    #elif x[0].startswith("DB") and x[1].startswith("GeneId:"):
        #weight.append(0.305)
    elif x[0].startswith("drug"):
        weight.append(0.1)
    #else:
        #weight.append(0.3)
    #weight.append(float(x[2]))
fs.close()
square_edge_data=pd.DataFrame({"source":source,"target":target,"weight":weight,})
#square_edge_data=pd.read_csv(fadj,sep="`",names=['source','target'],header=None,index_col=False)

x=square_node_data.dropna(axis=1)
y=square_edge_data.dropna(axis=1)
print(x.shape)
print(y.shape)

import numpy as np
a=y.to_numpy()


b=[]
with open(flabel,"r") as ft:
    countpos=0
    countneg=0
    for line in ft:
        v=int(line.strip())
        #v=1
        b.append(v)
        if v==1:
            countpos+=1
        else:
            countneg+=1
        
        #b.append(1)
           
import numpy as np
b = np.array(b)

print(b)
print(countpos,countneg)

from sklearn.model_selection import StratifiedKFold
from stellargraph import StellarGraph
import numpy as np
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
methods=["l1"]
gcnhiddenlayersize=[128]
learningrate=[0.01]
dropoutrate=[0.3]


symb="`"
countnos=0


cvscores = []
ctscores=[]
cnfmat=[]
accuracy=[]
precision=[]
recall=[]
fonescore=[]
specificity=[]
mcc=[]
auroc=[]
auprc=[]
sensitivity=[]
newauroc=[]

ft=open("p_feasibility.txt","w")
fp=open("pr_feasibility.txt","w")
for itr in range(1):
    print("iteration number: ",itr+1)
    kfold = StratifiedKFold(n_splits=2, shuffle=True, random_state=seed)
    
    count=0
    
    
    for train, test in kfold.split(a,b):
        count+=1
        print("turn number: ",count)
        print(a[train][0])
        train_data=[]
        for ij in a[train]:
            temp=[]
            temp.append(ij[0])
            temp.append(ij[1])
            temp.append(float(ij[2]))
            train_data.append(temp)
        #train_data=pd.DataFrame(train_data)
        print(len(train_data),len(a[train]))
        ytr = pd.DataFrame(train_data, columns=['source','target','weight'])
        G= StellarGraph({"corner": x}, {"line": ytr})
        test_data=[]
        for ij in a[test]:
            temp=[]
            temp.append(ij[0])
            temp.append(ij[1])
            temp.append(float(ij[2]))
            test_data.append(temp)
        print(len(test_data),len(a[test]))
        yts = pd.DataFrame(test_data, columns=['source','target','weight'])
        Gts= StellarGraph({"corner": x}, {"line": yts})
        edge_splitter_test = EdgeSplitter(Gts)
        G_test, edge_ids_test, edge_labels_test = edge_splitter_test.train_test_split(p=0.1, method="global", keep_connected=True)
        edge_splitter_int = EdgeSplitter(G)
        G_int, edge_ids_int, edge_labels_int = edge_splitter_int.train_test_split(p=0.1, method="global", keep_connected=True)
        edge_splitter_train = EdgeSplitter(G)
        G_train, edge_ids_train, edge_labels_train = edge_splitter_int.train_test_split(p=0.1, method="global", keep_connected=True)
    
        temp=[]
        c=0
        for i in edge_labels_train:
            if i==0:
                afg=[1,0]
                temp.append(afg)
            elif i==1:
                afg=[0,1]
                temp.append(afg)
            else:
                c+=1
        import numpy as np
        abc=np.array(temp)
        edge_labels_train=abc


        temp=[]
        c=0
        for i in edge_labels_test:
            if i==0:
                afg=[1,0]
                temp.append(afg)
            elif i==1:
                afg=[0,1]
                temp.append(afg)
            else:
                c+=1
        
        ghi=np.array(temp)
        edge_labels_test=ghi
        


        for l in methods:
            for i in gcnhiddenlayersize:
                for j in dropoutrate:
                    for k in learningrate:
                        print(l,i,j,k)
                        epochs =600
                        from tensorflow.keras.callbacks import EarlyStopping
                        train_gen = FullBatchLinkGenerator(G_train, method="gcn")
                        train_flow = train_gen.flow(edge_ids_train, edge_labels_train)
                        test_gen = FullBatchLinkGenerator(G_test, method="gcn")
                        test_flow = train_gen.flow(edge_ids_test, edge_labels_test)
                        gcn = GCN(layer_sizes=[i, i], activations=["relu", "relu"], generator=train_gen, dropout=j)
                        x_inp, x_out = gcn.in_out_tensors()
                        prediction = LinkEmbedding(activation="relu", method=l)(x_out)
                        prediction = keras.layers.Dense(units=2, activation="softmax")(prediction)
                        model = keras.Model(inputs=x_inp, outputs=prediction)
                        model.compile(optimizer=keras.optimizers.Adam(learning_rate=k),loss=keras.losses.binary_crossentropy,metrics=["acc"],)
                        es_callback = EarlyStopping(monitor="val_acc", patience=30, restore_best_weights=True)
                        #history = model.fit(train_flow, epochs=epochs, validation_data=test_flow, verbose=2, shuffle=False)
                        history = model.fit(train_flow, epochs=epochs, validation_data=test_flow, verbose=0, shuffle=False,callbacks=[es_callback],)
                        val_acc_per_epoch = history.history['val_acc']
                        maximum=str(max(val_acc_per_epoch))
                        maxx=float(maximum)
                        print("maximum validation accuracy: ",maximum)
                        cvscores.append(maxx)
                        trn_acc_per_epoch = history.history['acc']
                        trmaximum=str(max(trn_acc_per_epoch))
                        trmaxx=float(trmaximum)
                        print("maximum train accuracy: ",trmaximum)
                        ctscores.append(trmaxx)
                        t=""
                        t=t+trmaximum+symb
                        t=t+maximum+symb
                        t=t.strip()
                        #ft.write(t)
                        #ft.write("\n")
                        s=""
                        s=s+str(itr+1)+"`"+str(count)+"`"+str(l)+"`"+str(i)+"`"+str(j)+"`"+str(k)+"`"+maximum+"`"
                        s=s.strip()
                        print(s)
                        acl=0
                        prt=0
                        actual=[]
                        predicted=[]
                        abcd=edge_ids_test.tolist()
                        toprd=model.predict(test_flow)
                        toprd=toprd.tolist()
                        for first in toprd:
                          for ids,labels,prd in zip(abcd,edge_labels_test,first):
                              
                              if ids[0].startswith("DB") and ids[1].startswith("DB"):
                                  s=""
                                  s=s+str(ids[0])+symb
                                  s=s+str(ids[1])+symb
                                  s=s+str(labels[0])+symb
                                  s=s+str(labels[1])+symb
                                  s=s+str(prd[0])+symb
                                  s=s+str(prd[1])+symb
                                  s=s.strip()
                                  fp.write(s)
                                  fp.write("\n")
                                  countnos+=1
                              if labels[0]==1  and labels[1]==0:
                                acl=0
                                actual.append(acl)
                             # if float(prd[1])>float(prd[0]) and float(prd[1])>=0.9:
                               
                              else:
                                acl=1
                                actual.append(acl)
                              if float(prd[0])>float(prd[1]) :
                                prt=0
                                predicted.append(prt)
                              else:
                                prt=1
                                predicted.append(prt)
                        import numpy as np
                        print(len(actual))
                        actual=np.array(actual)
                        predicted=np.array(predicted)
                        from sklearn.metrics import confusion_matrix
                        cnfmat.append(confusion_matrix(actual, predicted))
                        from sklearn.metrics import accuracy_score
                        accuracy.append(accuracy_score(actual, predicted))
                        from sklearn.metrics import precision_score
                        precision.append(precision_score(actual, predicted))
                        from sklearn.metrics import recall_score
                        recall.append(recall_score(actual, predicted))
                        from sklearn.metrics import f1_score
                        fonescore.append(f1_score(actual, predicted))
                        from imblearn.metrics import specificity_score
                        specificity.append(specificity_score(actual, predicted))
                        from sklearn.metrics import matthews_corrcoef
                        mcc.append(matthews_corrcoef(actual, predicted))
                        from sklearn.metrics import roc_auc_score
                        auroc.append(roc_auc_score(actual, predicted))
                        import sklearn.metrics               
                        auprc.append(sklearn.metrics.average_precision_score(actual, predicted))
                        from sklearn.metrics import confusion_matrix
                        cm=confusion_matrix(actual, predicted)
                        sense=cm[1,1]/(cm[1,0]+cm[1,1])
                        sensitivity.append(sense)
                        from sklearn import metrics
                        fpr, tpr, thresholds = metrics.roc_curve(actual, predicted)
                        roc_auc = metrics.auc(fpr, tpr)
                        newauroc.append(roc_auc)
                        display = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='ROC curve')
                        display.plot()
                        plt.show()
                        #print("accuracy",accuracy)
                        #print("precision",precision)
                        #print("recal",recall)
                        #print("fonescore",fonescore)
                        #print("specificity",specificity)
                        #print("MCC",mcc)
                        #print("AUROC",auroc)
                        #print("Another auroc",newauroc)
                        #print("auprc",auprc)

auroc

print("mean of validation scores: ",np.mean(cvscores),"standard deviation: ",np.std(cvscores),"min:",np.min(cvscores),"max:",np.max(cvscores))

print("mean of training scores: ",np.mean(ctscores),"standard deviation: ",np.std(ctscores),"min:",np.min(ctscores),"max:",np.max(ctscores))

print("mean of accuracy: ",np.mean(accuracy),"standard deviation: ",np.std(accuracy),"min:",np.min(accuracy),"max:",np.max(accuracy))

print("mean of precision: ",np.mean(precision),"standard deviation: ",np.std(precision),"min:",np.min(precision),"max:",np.max(precision))

print("mean of recall: ",np.mean(recall),"standard deviation: ",np.std(recall),"min:",np.min(recall),"max:",np.max(recall))

print("mean of fonescore: ",np.mean(fonescore),"standard deviation: ",np.std(fonescore),"min:",np.min(fonescore),"max:",np.max(fonescore))

print("mean of specificity: ",np.mean(specificity),"standard deviation: ",np.std(specificity),"min:",np.min(specificity),"max:",np.max(specificity))

print("mean of sensitivity: ",np.mean(sensitivity),"standard deviation: ",np.std(sensitivity),"min:",np.min(sensitivity),"max:",np.max(sensitivity))

print("mean of mcc: ",np.mean(mcc),"standard deviation: ",np.std(mcc),"min:",np.min(mcc),"max:",np.max(mcc))

print("mean of auroc: ",np.mean(auroc),"standard deviation: ",np.std(auroc),"min:",np.min(auroc),"max:",np.max(auroc))

print("mean of auroc: ",np.mean(newauroc),"standard deviation: ",np.std(newauroc),"min:",np.min(newauroc),"max:",np.max(newauroc))


print("mean of auprc: ",np.mean(auprc),"standard deviation: ",np.std(auprc),"min:",np.min(auprc),"max:",np.max(auprc))

s=""
s=s+"accuracy"+"="+str(np.mean(accuracy))+"`"+"std="+str(np.std(accuracy))+"`"+"min="+str(np.min(accuracy))+"`"+"max="+str(np.max(accuracy))+"`"+"\n"
s=s+"precision"+"="+str(np.mean(precision))+"`"+"std="+str(np.std(precision))+"`"+"min="+str(np.min(precision))+"`"+"max="+str(np.max(precision))+"`"+"\n"
s=s+"recall"+"="+str(np.mean(recall))+"`"+"std="+str(np.std(recall))+"`"+"min="+str(np.min(recall))+"`"+"max="+str(np.max(recall))+"`"+"\n"
s=s+"f1-score"+"="+str(np.mean(fonescore))+"`"+"std="+str(np.std(fonescore))+"`"+"min="+str(np.min(fonescore))+"`"+"max="+str(np.max(fonescore))+"`"+"\n"
s=s+"specificity"+"="+str(np.mean(specificity))+"`"+"std="+str(np.std(specificity))+"`"+"min="+str(np.min(specificity))+"`"+"max="+str(np.max(specificity))+"`"+"\n"
s=s+"mcc"+"="+str(np.mean(mcc))+"`"+"std="+str(np.std(mcc))+"`"+"min="+str(np.min(mcc))+"`"+"max="+str(np.max(mcc))+"`"+"\n"
s=s+"AUROC"+"="+str(np.mean(auroc))+"`"+"std="+str(np.std(auroc))+"`"+"min="+str(np.min(auroc))+"`"+"max="+str(np.max(auroc))+"`"+"\n"
s=s+"AUPRC"+"="+str(np.mean(auprc))+"`"+"std="+str(np.std(auprc))+"`"+"min="+str(np.min(auprc))+"`"+"max="+str(np.max(auprc))+"`"+"\n"
s=s.strip()
ft.write(s)
ft.write("\n")
fp.close()
ft.close()


fno=0
fileno=1
count=0
countmatch=0
countop=0
fs=open(r"result_feasibility_tot_DDIs.txt","w")


ff=r"total_DDIs.txt"
alllist=[ff]

for f,newfile in enumerate(alllist):
    square_node_data=pd.read_csv(filename,sep="`",header=None,index_col=0)
    x=square_node_data.dropna(axis=1)
    print(x.shape)
    source=[]
    target=[]
    weight=[]
    entries=0
    fval=open(newfile,"r")
    for line in fval:
        nodlst=line.split(symb)
        if nodlst[0] in nodes and nodlst[1] in nodes:
            source.append(nodlst[0])
            target.append(nodlst[1])
            weight.append(0.2)
            entries+=1
    fval.close()
    square_edge_data=pd.DataFrame({"source":source,"target":target,"weight":weight,})
    y=square_edge_data.dropna(axis=1)
    print(y.shape)
    G= StellarGraph({"corner": x}, {"line": y})
    temp=[]
    print("stellargraph formation done") 
    #if f==len(alllist)-1:
        #entries=607122
    #else:
    #entries=41
    for i in range(entries):
                
            afg=[0,1]
            temp.append(afg)
                
    import numpy as np
    abc=np.array(temp)
    edge_labels_val=abc
    pred_gen = FullBatchLinkGenerator(G, method="gcn")
    pred_flow = pred_gen.flow(G.edges(), edge_labels_val)
    x=model.predict(pred_flow)
    count=0
    for i,j,k in zip(G.edges(),edge_labels_val,x[0]):
        count+=1
        s=""
        s=s+str(i[0])+symb
        s=s+str(i[1])+symb
        s=s+str(j[0])+symb
        s=s+str(j[1])+symb
        s=s+str(k[0])+symb
        s=s+str(k[1])+symb
        s=s.strip()
        #print(s)
        fs.write(s)
        fs.write("\n")
        
        if float(k[1])>float(k[0]):
            #print(s)
            countmatch+=1
        if float(k[1])>float(k[0]) and float(k[1])==1:
            #print(s)
            countop+=1
            
    print("number of combinations",count)    
    print("number of positive predictions",countmatch)
    print("number of ones",countop)
    
    fno+=1
    print("number of file being read",fno)
    print("number of file being written",fileno)
    

fs.close()
print("file 0 closed")


print(countnos)




# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 21:17:17 2024

@author: HP
"""






import pandas as pd



import stellargraph as sg
from stellargraph.data import EdgeSplitter
from stellargraph.mapper import FullBatchLinkGenerator
from stellargraph.layer import GCN, LinkEmbedding
from tensorflow import keras
from sklearn import preprocessing, feature_extraction, model_selection

from stellargraph import globalvar
from stellargraph import datasets
from IPython.display import display, HTML
import matplotlib.pyplot as plt

#filename=r"reduced-df-drug-protein.txt"
#fadj=r"spl-drug-protein-adjacency-matrix_a.txt"
#flabel=r"edge_labelling_existence_drug_protein.txt"




filename=r"FV_set.txt"
fadj=r"ID.txt"
flabel=r"edge-labelling-pr.txt"
square_node_data=pd.read_csv(filename,sep="`",header=None,index_col=0)
symb="`"
source=[]
target=[]
weight=[]
nodes=[]
fs=open(filename,"r")
for line in fs:
    x=line.split(symb)
    nodes.append(x[0])
fs.close()
fs=open(fadj,"r")
for line in fs:
    x=line.split(symb)
    source.append(x[0])
    target.append(x[1])
    if x[0].startswith("drug") and x[1].startswith("drug"):
        weight.append(0.2)
    #elif x[0].startswith("DB") and x[1].startswith("GeneId:"):
        #weight.append(0.305)
    elif x[0].startswith("drug"):
        weight.append(0.1)
    #else:
        #weight.append(0.3)
    #weight.append(float(x[2]))
fs.close()
square_edge_data=pd.DataFrame({"source":source,"target":target,"weight":weight,})
#square_edge_data=pd.read_csv(fadj,sep="`",names=['source','target'],header=None,index_col=False)

x=square_node_data.dropna(axis=1)
y=square_edge_data.dropna(axis=1)
print(x.shape)
print(y.shape)

import numpy as np
a=y.to_numpy()


b=[]
with open(flabel,"r") as ft:
    countpos=0
    countneg=0
    for line in ft:
        v=int(line.strip())
        #v=1
        b.append(v)
        if v==1:
            countpos+=1
        else:
            countneg+=1
        
        #b.append(1)
           
import numpy as np
b = np.array(b)

print(b)
print(countpos,countneg)

from sklearn.model_selection import StratifiedKFold
from stellargraph import StellarGraph
import numpy as np
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
methods=["l1"]
gcnhiddenlayersize=[128]
learningrate=[0.01]
dropoutrate=[0.3]


symb="`"
countnos=0


cvscores = []
ctscores=[]
cnfmat=[]
accuracy=[]
precision=[]
recall=[]
fonescore=[]
specificity=[]
mcc=[]
auroc=[]
auprc=[]
sensitivity=[]
newauroc=[]

ft=open("p_pr.txt","w")
fp=open("pr_pr.txt","w")
for itr in range(1):
    print("iteration number: ",itr+1)
    kfold = StratifiedKFold(n_splits=2, shuffle=True, random_state=seed)
    
    count=0
    
    
    for train, test in kfold.split(a,b):
        count+=1
        print("turn number: ",count)
        print(a[train][0])
        train_data=[]
        for ij in a[train]:
            temp=[]
            temp.append(ij[0])
            temp.append(ij[1])
            temp.append(float(ij[2]))
            train_data.append(temp)
        #train_data=pd.DataFrame(train_data)
        print(len(train_data),len(a[train]))
        ytr = pd.DataFrame(train_data, columns=['source','target','weight'])
        G= StellarGraph({"corner": x}, {"line": ytr})
        test_data=[]
        for ij in a[test]:
            temp=[]
            temp.append(ij[0])
            temp.append(ij[1])
            temp.append(float(ij[2]))
            test_data.append(temp)
        print(len(test_data),len(a[test]))
        yts = pd.DataFrame(test_data, columns=['source','target','weight'])
        Gts= StellarGraph({"corner": x}, {"line": yts})
        edge_splitter_test = EdgeSplitter(Gts)
        G_test, edge_ids_test, edge_labels_test = edge_splitter_test.train_test_split(p=0.1, method="global", keep_connected=True)
        edge_splitter_int = EdgeSplitter(G)
        G_int, edge_ids_int, edge_labels_int = edge_splitter_int.train_test_split(p=0.1, method="global", keep_connected=True)
        edge_splitter_train = EdgeSplitter(G)
        G_train, edge_ids_train, edge_labels_train = edge_splitter_int.train_test_split(p=0.1, method="global", keep_connected=True)
    
        temp=[]
        c=0
        for i in edge_labels_train:
            if i==0:
                afg=[1,0]
                temp.append(afg)
            elif i==1:
                afg=[0,1]
                temp.append(afg)
            else:
                c+=1
        import numpy as np
        abc=np.array(temp)
        edge_labels_train=abc


        temp=[]
        c=0
        for i in edge_labels_test:
            if i==0:
                afg=[1,0]
                temp.append(afg)
            elif i==1:
                afg=[0,1]
                temp.append(afg)
            else:
                c+=1
        
        ghi=np.array(temp)
        edge_labels_test=ghi
        


        for l in methods:
            for i in gcnhiddenlayersize:
                for j in dropoutrate:
                    for k in learningrate:
                        print(l,i,j,k)
                        epochs =600
                        from tensorflow.keras.callbacks import EarlyStopping
                        train_gen = FullBatchLinkGenerator(G_train, method="gcn")
                        train_flow = train_gen.flow(edge_ids_train, edge_labels_train)
                        test_gen = FullBatchLinkGenerator(G_test, method="gcn")
                        test_flow = train_gen.flow(edge_ids_test, edge_labels_test)
                        gcn = GCN(layer_sizes=[i, i], activations=["relu", "relu"], generator=train_gen, dropout=j)
                        x_inp, x_out = gcn.in_out_tensors()
                        prediction = LinkEmbedding(activation="relu", method=l)(x_out)
                        prediction = keras.layers.Dense(units=2, activation="softmax")(prediction)
                        model = keras.Model(inputs=x_inp, outputs=prediction)
                        model.compile(optimizer=keras.optimizers.Adam(learning_rate=k),loss=keras.losses.binary_crossentropy,metrics=["acc"],)
                        es_callback = EarlyStopping(monitor="val_acc", patience=30, restore_best_weights=True)
                        #history = model.fit(train_flow, epochs=epochs, validation_data=test_flow, verbose=2, shuffle=False)
                        history = model.fit(train_flow, epochs=epochs, validation_data=test_flow, verbose=0, shuffle=False,callbacks=[es_callback],)
                        val_acc_per_epoch = history.history['val_acc']
                        maximum=str(max(val_acc_per_epoch))
                        maxx=float(maximum)
                        print("maximum validation accuracy: ",maximum)
                        cvscores.append(maxx)
                        trn_acc_per_epoch = history.history['acc']
                        trmaximum=str(max(trn_acc_per_epoch))
                        trmaxx=float(trmaximum)
                        print("maximum train accuracy: ",trmaximum)
                        ctscores.append(trmaxx)
                        t=""
                        t=t+trmaximum+symb
                        t=t+maximum+symb
                        t=t.strip()
                        #ft.write(t)
                        #ft.write("\n")
                        s=""
                        s=s+str(itr+1)+"`"+str(count)+"`"+str(l)+"`"+str(i)+"`"+str(j)+"`"+str(k)+"`"+maximum+"`"
                        s=s.strip()
                        print(s)
                        acl=0
                        prt=0
                        actual=[]
                        predicted=[]
                        abcd=edge_ids_test.tolist()
                        toprd=model.predict(test_flow)
                        toprd=toprd.tolist()
                        for first in toprd:
                          for ids,labels,prd in zip(abcd,edge_labels_test,first):
                              
                              if ids[0].startswith("DB") and ids[1].startswith("DB"):
                                  s=""
                                  s=s+str(ids[0])+symb
                                  s=s+str(ids[1])+symb
                                  s=s+str(labels[0])+symb
                                  s=s+str(labels[1])+symb
                                  s=s+str(prd[0])+symb
                                  s=s+str(prd[1])+symb
                                  s=s.strip()
                                  fp.write(s)
                                  fp.write("\n")
                                  countnos+=1
                              if labels[0]==1  and labels[1]==0:
                                acl=0
                                actual.append(acl)
                             # if float(prd[1])>float(prd[0]) and float(prd[1])>=0.9:
                               
                              else:
                                acl=1
                                actual.append(acl)
                              if float(prd[0])>float(prd[1]) :
                                prt=0
                                predicted.append(prt)
                              else:
                                prt=1
                                predicted.append(prt)
                        import numpy as np
                        print(len(actual))
                        actual=np.array(actual)
                        predicted=np.array(predicted)
                        from sklearn.metrics import confusion_matrix
                        cnfmat.append(confusion_matrix(actual, predicted))
                        from sklearn.metrics import accuracy_score
                        accuracy.append(accuracy_score(actual, predicted))
                        from sklearn.metrics import precision_score
                        precision.append(precision_score(actual, predicted))
                        from sklearn.metrics import recall_score
                        recall.append(recall_score(actual, predicted))
                        from sklearn.metrics import f1_score
                        fonescore.append(f1_score(actual, predicted))
                        from imblearn.metrics import specificity_score
                        specificity.append(specificity_score(actual, predicted))
                        from sklearn.metrics import matthews_corrcoef
                        mcc.append(matthews_corrcoef(actual, predicted))
                        from sklearn.metrics import roc_auc_score
                        auroc.append(roc_auc_score(actual, predicted))
                        import sklearn.metrics               
                        auprc.append(sklearn.metrics.average_precision_score(actual, predicted))
                        from sklearn.metrics import confusion_matrix
                        cm=confusion_matrix(actual, predicted)
                        sense=cm[1,1]/(cm[1,0]+cm[1,1])
                        sensitivity.append(sense)
                        from sklearn import metrics
                        fpr, tpr, thresholds = metrics.roc_curve(actual, predicted)
                        roc_auc = metrics.auc(fpr, tpr)
                        newauroc.append(roc_auc)
                        display = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='ROC curve')
                        display.plot()
                        plt.show()
                        #print("accuracy",accuracy)
                        #print("precision",precision)
                        #print("recal",recall)
                        #print("fonescore",fonescore)
                        #print("specificity",specificity)
                        #print("MCC",mcc)
                        #print("AUROC",auroc)
                        #print("Another auroc",newauroc)
                        #print("auprc",auprc)

auroc

print("mean of validation scores: ",np.mean(cvscores),"standard deviation: ",np.std(cvscores),"min:",np.min(cvscores),"max:",np.max(cvscores))

print("mean of training scores: ",np.mean(ctscores),"standard deviation: ",np.std(ctscores),"min:",np.min(ctscores),"max:",np.max(ctscores))

print("mean of accuracy: ",np.mean(accuracy),"standard deviation: ",np.std(accuracy),"min:",np.min(accuracy),"max:",np.max(accuracy))

print("mean of precision: ",np.mean(precision),"standard deviation: ",np.std(precision),"min:",np.min(precision),"max:",np.max(precision))

print("mean of recall: ",np.mean(recall),"standard deviation: ",np.std(recall),"min:",np.min(recall),"max:",np.max(recall))

print("mean of fonescore: ",np.mean(fonescore),"standard deviation: ",np.std(fonescore),"min:",np.min(fonescore),"max:",np.max(fonescore))

print("mean of specificity: ",np.mean(specificity),"standard deviation: ",np.std(specificity),"min:",np.min(specificity),"max:",np.max(specificity))

print("mean of sensitivity: ",np.mean(sensitivity),"standard deviation: ",np.std(sensitivity),"min:",np.min(sensitivity),"max:",np.max(sensitivity))

print("mean of mcc: ",np.mean(mcc),"standard deviation: ",np.std(mcc),"min:",np.min(mcc),"max:",np.max(mcc))

print("mean of auroc: ",np.mean(auroc),"standard deviation: ",np.std(auroc),"min:",np.min(auroc),"max:",np.max(auroc))

print("mean of auroc: ",np.mean(newauroc),"standard deviation: ",np.std(newauroc),"min:",np.min(newauroc),"max:",np.max(newauroc))


print("mean of auprc: ",np.mean(auprc),"standard deviation: ",np.std(auprc),"min:",np.min(auprc),"max:",np.max(auprc))

s=""
s=s+"accuracy"+"="+str(np.mean(accuracy))+"`"+"std="+str(np.std(accuracy))+"`"+"min="+str(np.min(accuracy))+"`"+"max="+str(np.max(accuracy))+"`"+"\n"
s=s+"precision"+"="+str(np.mean(precision))+"`"+"std="+str(np.std(precision))+"`"+"min="+str(np.min(precision))+"`"+"max="+str(np.max(precision))+"`"+"\n"
s=s+"recall"+"="+str(np.mean(recall))+"`"+"std="+str(np.std(recall))+"`"+"min="+str(np.min(recall))+"`"+"max="+str(np.max(recall))+"`"+"\n"
s=s+"f1-score"+"="+str(np.mean(fonescore))+"`"+"std="+str(np.std(fonescore))+"`"+"min="+str(np.min(fonescore))+"`"+"max="+str(np.max(fonescore))+"`"+"\n"
s=s+"specificity"+"="+str(np.mean(specificity))+"`"+"std="+str(np.std(specificity))+"`"+"min="+str(np.min(specificity))+"`"+"max="+str(np.max(specificity))+"`"+"\n"
s=s+"mcc"+"="+str(np.mean(mcc))+"`"+"std="+str(np.std(mcc))+"`"+"min="+str(np.min(mcc))+"`"+"max="+str(np.max(mcc))+"`"+"\n"
s=s+"AUROC"+"="+str(np.mean(auroc))+"`"+"std="+str(np.std(auroc))+"`"+"min="+str(np.min(auroc))+"`"+"max="+str(np.max(auroc))+"`"+"\n"
s=s+"AUPRC"+"="+str(np.mean(auprc))+"`"+"std="+str(np.std(auprc))+"`"+"min="+str(np.min(auprc))+"`"+"max="+str(np.max(auprc))+"`"+"\n"
s=s.strip()
ft.write(s)
ft.write("\n")
fp.close()
ft.close()


fno=0
fileno=1
count=0
countmatch=0
countop=0
fs=open(r"result_pr_tot_DDIs.txt","w")


ff=r"total_DDIs.txt"
alllist=[ff]

for f,newfile in enumerate(alllist):
    square_node_data=pd.read_csv(filename,sep="`",header=None,index_col=0)
    x=square_node_data.dropna(axis=1)
    print(x.shape)
    source=[]
    target=[]
    weight=[]
    entries=0
    fval=open(newfile,"r")
    for line in fval:
        nodlst=line.split(symb)
        if nodlst[0] in nodes and nodlst[1] in nodes:
            source.append(nodlst[0])
            target.append(nodlst[1])
            weight.append(0.2)
            entries+=1
    fval.close()
    square_edge_data=pd.DataFrame({"source":source,"target":target,"weight":weight,})
    y=square_edge_data.dropna(axis=1)
    print(y.shape)
    G= StellarGraph({"corner": x}, {"line": y})
    temp=[]
    print("stellargraph formation done") 
    #if f==len(alllist)-1:
        #entries=607122
    #else:
    #entries=41
    for i in range(entries):
                
            afg=[0,1]
            temp.append(afg)
                
    import numpy as np
    abc=np.array(temp)
    edge_labels_val=abc
    pred_gen = FullBatchLinkGenerator(G, method="gcn")
    pred_flow = pred_gen.flow(G.edges(), edge_labels_val)
    x=model.predict(pred_flow)
    count=0
    for i,j,k in zip(G.edges(),edge_labels_val,x[0]):
        count+=1
        s=""
        s=s+str(i[0])+symb
        s=s+str(i[1])+symb
        s=s+str(j[0])+symb
        s=s+str(j[1])+symb
        s=s+str(k[0])+symb
        s=s+str(k[1])+symb
        s=s.strip()
        #print(s)
        fs.write(s)
        fs.write("\n")
        
        if float(k[1])>float(k[0]):
            #print(s)
            countmatch+=1
        if float(k[1])>float(k[0]) and float(k[1])==1:
            #print(s)
            countop+=1
            
    print("number of combinations",count)    
    print("number of positive predictions",countmatch)
    print("number of ones",countop)
    
    fno+=1
    print("number of file being read",fno)
    print("number of file being written",fileno)
    

fs.close()
print("file 0 closed")


print(countnos)

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 21:17:17 2024

@author: HP
"""






import pandas as pd



import stellargraph as sg
from stellargraph.data import EdgeSplitter
from stellargraph.mapper import FullBatchLinkGenerator
from stellargraph.layer import GCN, LinkEmbedding
from tensorflow import keras
from sklearn import preprocessing, feature_extraction, model_selection

from stellargraph import globalvar
from stellargraph import datasets
from IPython.display import display, HTML
import matplotlib.pyplot as plt

#filename=r"reduced-df-drug-protein.txt"
#fadj=r"spl-drug-protein-adjacency-matrix_a.txt"
#flabel=r"edge_labelling_existence_drug_protein.txt"




filename=r"FV_set.txt"
fadj=r"ID.txt"
flabel=r"edge-labelling-ss.txt"
square_node_data=pd.read_csv(filename,sep="`",header=None,index_col=0)
symb="`"
source=[]
target=[]
weight=[]
nodes=[]
fs=open(filename,"r")
for line in fs:
    x=line.split(symb)
    nodes.append(x[0])
fs.close()
fs=open(fadj,"r")
for line in fs:
    x=line.split(symb)
    source.append(x[0])
    target.append(x[1])
    if x[0].startswith("drug") and x[1].startswith("drug"):
        weight.append(0.2)
    #elif x[0].startswith("DB") and x[1].startswith("GeneId:"):
        #weight.append(0.305)
    elif x[0].startswith("drug"):
        weight.append(0.1)
    #else:
        #weight.append(0.3)
    #weight.append(float(x[2]))
fs.close()
square_edge_data=pd.DataFrame({"source":source,"target":target,"weight":weight,})
#square_edge_data=pd.read_csv(fadj,sep="`",names=['source','target'],header=None,index_col=False)

x=square_node_data.dropna(axis=1)
y=square_edge_data.dropna(axis=1)
print(x.shape)
print(y.shape)

import numpy as np
a=y.to_numpy()


b=[]
with open(flabel,"r") as ft:
    countpos=0
    countneg=0
    for line in ft:
        v=int(line.strip())
        #v=1
        b.append(v)
        if v==1:
            countpos+=1
        else:
            countneg+=1
        
        #b.append(1)
           
import numpy as np
b = np.array(b)

print(b)
print(countpos,countneg)

from sklearn.model_selection import StratifiedKFold
from stellargraph import StellarGraph
import numpy as np
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
methods=["l1"]
gcnhiddenlayersize=[128]
learningrate=[0.01]
dropoutrate=[0.3]


symb="`"
countnos=0


cvscores = []
ctscores=[]
cnfmat=[]
accuracy=[]
precision=[]
recall=[]
fonescore=[]
specificity=[]
mcc=[]
auroc=[]
auprc=[]
sensitivity=[]
newauroc=[]

ft=open("p_ss.txt","w")
fp=open("pr_ss.txt","w")
for itr in range(1):
    print("iteration number: ",itr+1)
    kfold = StratifiedKFold(n_splits=2, shuffle=True, random_state=seed)
    
    count=0
    
    
    for train, test in kfold.split(a,b):
        count+=1
        print("turn number: ",count)
        print(a[train][0])
        train_data=[]
        for ij in a[train]:
            temp=[]
            temp.append(ij[0])
            temp.append(ij[1])
            temp.append(float(ij[2]))
            train_data.append(temp)
        #train_data=pd.DataFrame(train_data)
        print(len(train_data),len(a[train]))
        ytr = pd.DataFrame(train_data, columns=['source','target','weight'])
        G= StellarGraph({"corner": x}, {"line": ytr})
        test_data=[]
        for ij in a[test]:
            temp=[]
            temp.append(ij[0])
            temp.append(ij[1])
            temp.append(float(ij[2]))
            test_data.append(temp)
        print(len(test_data),len(a[test]))
        yts = pd.DataFrame(test_data, columns=['source','target','weight'])
        Gts= StellarGraph({"corner": x}, {"line": yts})
        edge_splitter_test = EdgeSplitter(Gts)
        G_test, edge_ids_test, edge_labels_test = edge_splitter_test.train_test_split(p=0.1, method="global", keep_connected=True)
        edge_splitter_int = EdgeSplitter(G)
        G_int, edge_ids_int, edge_labels_int = edge_splitter_int.train_test_split(p=0.1, method="global", keep_connected=True)
        edge_splitter_train = EdgeSplitter(G)
        G_train, edge_ids_train, edge_labels_train = edge_splitter_int.train_test_split(p=0.1, method="global", keep_connected=True)
    
        temp=[]
        c=0
        for i in edge_labels_train:
            if i==0:
                afg=[1,0]
                temp.append(afg)
            elif i==1:
                afg=[0,1]
                temp.append(afg)
            else:
                c+=1
        import numpy as np
        abc=np.array(temp)
        edge_labels_train=abc


        temp=[]
        c=0
        for i in edge_labels_test:
            if i==0:
                afg=[1,0]
                temp.append(afg)
            elif i==1:
                afg=[0,1]
                temp.append(afg)
            else:
                c+=1
        
        ghi=np.array(temp)
        edge_labels_test=ghi
        


        for l in methods:
            for i in gcnhiddenlayersize:
                for j in dropoutrate:
                    for k in learningrate:
                        print(l,i,j,k)
                        epochs =600
                        from tensorflow.keras.callbacks import EarlyStopping
                        train_gen = FullBatchLinkGenerator(G_train, method="gcn")
                        train_flow = train_gen.flow(edge_ids_train, edge_labels_train)
                        test_gen = FullBatchLinkGenerator(G_test, method="gcn")
                        test_flow = train_gen.flow(edge_ids_test, edge_labels_test)
                        gcn = GCN(layer_sizes=[i, i], activations=["relu", "relu"], generator=train_gen, dropout=j)
                        x_inp, x_out = gcn.in_out_tensors()
                        prediction = LinkEmbedding(activation="relu", method=l)(x_out)
                        prediction = keras.layers.Dense(units=2, activation="softmax")(prediction)
                        model = keras.Model(inputs=x_inp, outputs=prediction)
                        model.compile(optimizer=keras.optimizers.Adam(learning_rate=k),loss=keras.losses.binary_crossentropy,metrics=["acc"],)
                        es_callback = EarlyStopping(monitor="val_acc", patience=30, restore_best_weights=True)
                        #history = model.fit(train_flow, epochs=epochs, validation_data=test_flow, verbose=2, shuffle=False)
                        history = model.fit(train_flow, epochs=epochs, validation_data=test_flow, verbose=0, shuffle=False,callbacks=[es_callback],)
                        val_acc_per_epoch = history.history['val_acc']
                        maximum=str(max(val_acc_per_epoch))
                        maxx=float(maximum)
                        print("maximum validation accuracy: ",maximum)
                        cvscores.append(maxx)
                        trn_acc_per_epoch = history.history['acc']
                        trmaximum=str(max(trn_acc_per_epoch))
                        trmaxx=float(trmaximum)
                        print("maximum train accuracy: ",trmaximum)
                        ctscores.append(trmaxx)
                        t=""
                        t=t+trmaximum+symb
                        t=t+maximum+symb
                        t=t.strip()
                        #ft.write(t)
                        #ft.write("\n")
                        s=""
                        s=s+str(itr+1)+"`"+str(count)+"`"+str(l)+"`"+str(i)+"`"+str(j)+"`"+str(k)+"`"+maximum+"`"
                        s=s.strip()
                        print(s)
                        acl=0
                        prt=0
                        actual=[]
                        predicted=[]
                        abcd=edge_ids_test.tolist()
                        toprd=model.predict(test_flow)
                        toprd=toprd.tolist()
                        for first in toprd:
                          for ids,labels,prd in zip(abcd,edge_labels_test,first):
                              
                              if ids[0].startswith("DB") and ids[1].startswith("DB"):
                                  s=""
                                  s=s+str(ids[0])+symb
                                  s=s+str(ids[1])+symb
                                  s=s+str(labels[0])+symb
                                  s=s+str(labels[1])+symb
                                  s=s+str(prd[0])+symb
                                  s=s+str(prd[1])+symb
                                  s=s.strip()
                                  fp.write(s)
                                  fp.write("\n")
                                  countnos+=1
                              if labels[0]==1  and labels[1]==0:
                                acl=0
                                actual.append(acl)
                             # if float(prd[1])>float(prd[0]) and float(prd[1])>=0.9:
                               
                              else:
                                acl=1
                                actual.append(acl)
                              if float(prd[0])>float(prd[1]) :
                                prt=0
                                predicted.append(prt)
                              else:
                                prt=1
                                predicted.append(prt)
                        import numpy as np
                        print(len(actual))
                        actual=np.array(actual)
                        predicted=np.array(predicted)
                        from sklearn.metrics import confusion_matrix
                        cnfmat.append(confusion_matrix(actual, predicted))
                        from sklearn.metrics import accuracy_score
                        accuracy.append(accuracy_score(actual, predicted))
                        from sklearn.metrics import precision_score
                        precision.append(precision_score(actual, predicted))
                        from sklearn.metrics import recall_score
                        recall.append(recall_score(actual, predicted))
                        from sklearn.metrics import f1_score
                        fonescore.append(f1_score(actual, predicted))
                        from imblearn.metrics import specificity_score
                        specificity.append(specificity_score(actual, predicted))
                        from sklearn.metrics import matthews_corrcoef
                        mcc.append(matthews_corrcoef(actual, predicted))
                        from sklearn.metrics import roc_auc_score
                        auroc.append(roc_auc_score(actual, predicted))
                        import sklearn.metrics               
                        auprc.append(sklearn.metrics.average_precision_score(actual, predicted))
                        from sklearn.metrics import confusion_matrix
                        cm=confusion_matrix(actual, predicted)
                        sense=cm[1,1]/(cm[1,0]+cm[1,1])
                        sensitivity.append(sense)
                        from sklearn import metrics
                        fpr, tpr, thresholds = metrics.roc_curve(actual, predicted)
                        roc_auc = metrics.auc(fpr, tpr)
                        newauroc.append(roc_auc)
                        display = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='ROC curve')
                        display.plot()
                        plt.show()
                        #print("accuracy",accuracy)
                        #print("precision",precision)
                        #print("recal",recall)
                        #print("fonescore",fonescore)
                        #print("specificity",specificity)
                        #print("MCC",mcc)
                        #print("AUROC",auroc)
                        #print("Another auroc",newauroc)
                        #print("auprc",auprc)

auroc

print("mean of validation scores: ",np.mean(cvscores),"standard deviation: ",np.std(cvscores),"min:",np.min(cvscores),"max:",np.max(cvscores))

print("mean of training scores: ",np.mean(ctscores),"standard deviation: ",np.std(ctscores),"min:",np.min(ctscores),"max:",np.max(ctscores))

print("mean of accuracy: ",np.mean(accuracy),"standard deviation: ",np.std(accuracy),"min:",np.min(accuracy),"max:",np.max(accuracy))

print("mean of precision: ",np.mean(precision),"standard deviation: ",np.std(precision),"min:",np.min(precision),"max:",np.max(precision))

print("mean of recall: ",np.mean(recall),"standard deviation: ",np.std(recall),"min:",np.min(recall),"max:",np.max(recall))

print("mean of fonescore: ",np.mean(fonescore),"standard deviation: ",np.std(fonescore),"min:",np.min(fonescore),"max:",np.max(fonescore))

print("mean of specificity: ",np.mean(specificity),"standard deviation: ",np.std(specificity),"min:",np.min(specificity),"max:",np.max(specificity))

print("mean of sensitivity: ",np.mean(sensitivity),"standard deviation: ",np.std(sensitivity),"min:",np.min(sensitivity),"max:",np.max(sensitivity))

print("mean of mcc: ",np.mean(mcc),"standard deviation: ",np.std(mcc),"min:",np.min(mcc),"max:",np.max(mcc))

print("mean of auroc: ",np.mean(auroc),"standard deviation: ",np.std(auroc),"min:",np.min(auroc),"max:",np.max(auroc))

print("mean of auroc: ",np.mean(newauroc),"standard deviation: ",np.std(newauroc),"min:",np.min(newauroc),"max:",np.max(newauroc))


print("mean of auprc: ",np.mean(auprc),"standard deviation: ",np.std(auprc),"min:",np.min(auprc),"max:",np.max(auprc))

s=""
s=s+"accuracy"+"="+str(np.mean(accuracy))+"`"+"std="+str(np.std(accuracy))+"`"+"min="+str(np.min(accuracy))+"`"+"max="+str(np.max(accuracy))+"`"+"\n"
s=s+"precision"+"="+str(np.mean(precision))+"`"+"std="+str(np.std(precision))+"`"+"min="+str(np.min(precision))+"`"+"max="+str(np.max(precision))+"`"+"\n"
s=s+"recall"+"="+str(np.mean(recall))+"`"+"std="+str(np.std(recall))+"`"+"min="+str(np.min(recall))+"`"+"max="+str(np.max(recall))+"`"+"\n"
s=s+"f1-score"+"="+str(np.mean(fonescore))+"`"+"std="+str(np.std(fonescore))+"`"+"min="+str(np.min(fonescore))+"`"+"max="+str(np.max(fonescore))+"`"+"\n"
s=s+"specificity"+"="+str(np.mean(specificity))+"`"+"std="+str(np.std(specificity))+"`"+"min="+str(np.min(specificity))+"`"+"max="+str(np.max(specificity))+"`"+"\n"
s=s+"mcc"+"="+str(np.mean(mcc))+"`"+"std="+str(np.std(mcc))+"`"+"min="+str(np.min(mcc))+"`"+"max="+str(np.max(mcc))+"`"+"\n"
s=s+"AUROC"+"="+str(np.mean(auroc))+"`"+"std="+str(np.std(auroc))+"`"+"min="+str(np.min(auroc))+"`"+"max="+str(np.max(auroc))+"`"+"\n"
s=s+"AUPRC"+"="+str(np.mean(auprc))+"`"+"std="+str(np.std(auprc))+"`"+"min="+str(np.min(auprc))+"`"+"max="+str(np.max(auprc))+"`"+"\n"
s=s.strip()
ft.write(s)
ft.write("\n")
fp.close()
ft.close()


fno=0
fileno=1
count=0
countmatch=0
countop=0
fs=open(r"result_ss_tot_DDIs.txt","w")


ff=r"total_DDIs.txt"
alllist=[ff]

for f,newfile in enumerate(alllist):
    square_node_data=pd.read_csv(filename,sep="`",header=None,index_col=0)
    x=square_node_data.dropna(axis=1)
    print(x.shape)
    source=[]
    target=[]
    weight=[]
    entries=0
    fval=open(newfile,"r")
    for line in fval:
        nodlst=line.split(symb)
        if nodlst[0] in nodes and nodlst[1] in nodes:
            source.append(nodlst[0])
            target.append(nodlst[1])
            weight.append(0.2)
            entries+=1
    fval.close()
    square_edge_data=pd.DataFrame({"source":source,"target":target,"weight":weight,})
    y=square_edge_data.dropna(axis=1)
    print(y.shape)
    G= StellarGraph({"corner": x}, {"line": y})
    temp=[]
    print("stellargraph formation done") 
    #if f==len(alllist)-1:
        #entries=607122
    #else:
    #entries=41
    for i in range(entries):
                
            afg=[0,1]
            temp.append(afg)
                
    import numpy as np
    abc=np.array(temp)
    edge_labels_val=abc
    pred_gen = FullBatchLinkGenerator(G, method="gcn")
    pred_flow = pred_gen.flow(G.edges(), edge_labels_val)
    x=model.predict(pred_flow)
    count=0
    for i,j,k in zip(G.edges(),edge_labels_val,x[0]):
        count+=1
        s=""
        s=s+str(i[0])+symb
        s=s+str(i[1])+symb
        s=s+str(j[0])+symb
        s=s+str(j[1])+symb
        s=s+str(k[0])+symb
        s=s+str(k[1])+symb
        s=s.strip()
        #print(s)
        fs.write(s)
        fs.write("\n")
        
        if float(k[1])>float(k[0]):
            #print(s)
            countmatch+=1
        if float(k[1])>float(k[0]) and float(k[1])==1:
            #print(s)
            countop+=1
            
    print("number of combinations",count)    
    print("number of positive predictions",countmatch)
    print("number of ones",countop)
    
    fno+=1
    print("number of file being read",fno)
    print("number of file being written",fileno)
    

fs.close()
print("file 0 closed")


print(countnos)