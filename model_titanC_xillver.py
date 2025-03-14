#!/usr/bin/env python
# coding: utf-8

# In[11]:


from xspec import *
import numpy as np
import os
from collections import Counter


# In[12]:


#get_ipython().run_cell_magic('bash', '', 'pwd\n')


# In[39]:


path='/work/bpalit/Objects/AGN/POP_2018/'
os.chdir(path)

level2=np.loadtxt('level2dir.txt',dtype=str)
specfiles=np.loadtxt('specfiles.txt',dtype=str)
freq=np.loadtxt("objectnames.txt",delimiter="/",dtype=str)

# In[40]:


AllModels.lmod("relxill",dirPath="~/relxill/relxill_model_v2.3/")
m=Model("Tbabs*mtable{n5548A_wa_ext.fits}*(xillver+nthcomp+atable{TITAN_C_hd.mod})")


# In[41]:


def fitperform(x,galactic_nh,redshifts):

    AllData.clear()
    s1=Spectrum(x)
    
    Fit.statMethod='chi'
    Plot.xAxis='KeV'
    
    m=Model("Tbabs*mtable{n5548A_wa_ext.fits}*(xillver+nthcomp+atable{TITAN_C_hd.mod})")

    AllData(s1.fileName)
    AllData.ignore("1:**-.3")
    AllData.ignore("1:10.-**")
    AllData.ignore("bad")
    AllData.ignore("1:1.8-2.4")
    
    
        
    logxirange = "2.5,,1,1,3,3"
    logNHrange = "21.5,,19,19,23,23"
    phindx = "1.9,,1,1,4,4"
    #heatingrange = "-22.5,0.05769,-23,-23,-21.5,-21.5"
    heatingrange = ",0.01,-23,-23,-21.5,-21.5"
    #opacityrange ="17.5,0.9615,6,6,29,29"
    opacityrange =",0.1,5,5,30,30"
    #xillvernorm="1,,1e-7,1e-7,1e-2,1e-2"
    #TITANnorm="1,,1e-9,1e-9,1e-2,1e-2"
    #nthnorm="1,,1e-9,1e-9,1e-1,1e-1"
    
    
    m.TBabs.nH.values=galactic_nh
    m.TBabs.nH.frozen=True
    m.CLOUDY.logxi.values=logxirange
    m.CLOUDY.logvturb.values="2"
    m.CLOUDY.logvturb.frozen=True
    m.CLOUDY.logNH.values=logNHrange
    m.CLOUDY.z.values=redshifts
    m.CLOUDY.z.frozen=True
    #m.xillver.gamma.values="1.8"
    m.xillver.gamma.link=str(m.nthComp.Gamma.index)
    #m.xillver.gamma.frozen=True
    m.xillver.Afe.values="1.0"
    m.xillver.Afe.frozen=True
    m.xillver.Ecut.values="300"
    m.xillver.Ecut.frozen=True
    m.xillver.logxi.values="0.0"
    m.xillver.logxi.frozen=True
    m.xillver.z.values=redshifts
    m.xillver.z.frozen=True
    m.xillver.Incl.values="30"
    m.xillver.Incl.frozen=True
    m.xillver.norm.values="1"#xillvernorm
    m.nthComp.Gamma.values=phindx
    m.nthComp.kT_e.values="100"
    m.nthComp.kT_e.frozen=True
    m.nthComp.kT_bb.frozen=False
    m.nthComp.kT_bb.values=".004,,.001,0.001,.007,.007"
    #m.nthComp.kT_bb.frozen=True
    m.nthComp.inp_type.values="1"
    m.nthComp.inp_type.frozen=True
    m.nthComp.Redshift.values=redshifts
    m.nthComp.Redshift.frozen=True
    m.nthComp.norm.values="1"#nthnorm
    m.TITAN_C.logqh.values=heatingrange
    m.TITAN_C.tau.values=opacityrange
    m.TITAN_C.z.values=redshifts
    m.TITAN_C.z.frozen=True
    m.TITAN_C.norm.values="1"#TITANnorm

    

    

    Fit.query = "yes"   
    Fit.perform()
    

    #AllModels.calcFlux("0.2 5.0")
    #AllModels.calcFlux("2.0 10.0")
    #AllModels.eqwidth("3 4")
    Fit.steppar("2 0 4 100")
    Fit.steppar("4 19 24 100")
    Fit.steppar("14 1 3 100")
    Fit.steppar("20 -23 -21.5 100")
    Fit.steppar("21 5 30 100")
    Fit.perform()	
    Fit.perform()
    AllModels.show()
    #AllModels.calcFlux(".3 10.0 err 90 100")
    #AllModels.calcFlux(".3 2.0 err 90 100")
    #Plot.device = "/xs"
    #Plot.xLog = True
    #Plot.yLog = True
    #Plot("data","delchi")
    global c
    c=Fit.statistic/Fit.dof
    #print(c)
    global logxi_C,logxi_C_err,NH_C, NH_C_err, Gamma_hc,Gamma_hc_err, log_qh,log_qh_err, tau,tau_err, titannorm, titannorn_err
    
#     logxi_C=m.CLOUDY.logxi.values[0]
#     Fit.error("2.706 2")
#     logxi_C_err=m.CLOUDY.logxi.error
    
#     NH_C=m.CLOUDY.logNH.values[0]
#     Fit.error("2.706 4")
#     NH_C_err=m.CLOUDY.logNH.error
    
#     Gamma_hc=m.nthComp.Gamma.values[0]
#     Fit.error("2.706 14")
#     Gamma_hc_err=m.nthComp.Gamma.error
    
#     log_qh=m.TITAN_C.logqh.values[0]
#     Fit.error("2.706 20")
#     log_qh_err=m.TITAN_C.logqh.error
    
#     tau=m.TITAN_C.tau.values[0]
#     Fit.error("2.706 21")
#     tau_err=m.TITAN_C.tau.error
    
#     titannorm=m.TITAN_C.norm.values[0]
#     Fit.error("2.706 23")
#     titannorn_err=m.TITAN_C.norm.error
    
    
    logxi_C=m.CLOUDY.logxi.values[0]
    
    logxi_C_err=m.CLOUDY.logxi.sigma
    
    NH_C=m.CLOUDY.logNH.values[0]
    
    NH_C_err=m.CLOUDY.logNH.sigma
    
    Gamma_hc=m.nthComp.Gamma.values[0]
    
    Gamma_hc_err=m.nthComp.Gamma.sigma
    
    log_qh=m.TITAN_C.logqh.values[0]
    
    log_qh_err=m.TITAN_C.logqh.sigma
    
    tau=m.TITAN_C.tau.values[0]
    
    tau_err=m.TITAN_C.tau.sigma
    
    titannorm=m.TITAN_C.norm.values[0]
    
    titannorn_err=m.TITAN_C.norm.sigma
    
    
    
    
    #brke=m.bknpower.BreakE.values[0]
    #Fit.error("2.706 3")
    #brke_err=m.bknpower.BreakE.error
    
   # err=m.bknpower.BreakE.error
#     ec1=m.zgauss.LineE.values[0]
#     er1=m.zgauss.LineE.sigma
#     sig1=m.zgauss.Sigma.values[0]
#     sigerr1=m.zgauss.Sigma.sigma
    
#     ec2=m.zgauss_4.LineE.values[0]
#     er2=m.zgauss_4.LineE.sigma
#     sig2=m.zgauss_4.Sigma.values[0]
#     sigerr2=m.zgauss_4.Sigma.sigma


# In[42]:


# chistat,logxi_C1,logxi_C_err1,NH_C1, NH_C_err1, Gamma_hc1,Gamma_hc_err1, log_qh1,log_qh_err1, tau1,tau_err1, titannorm1, titannorn_err1=[],[],[],[],[],[],[],[],[],[],[],[],[]

# for i in range(2):
#     path=os.chdir(level2[i])
#     fitperform(specfiles[i],"0.0159","0.03")
#     chistat.append(c)
#     logxi_C1.append(logxi_C)
#     logxi_C_err1.append(logxi_C_err)
#     NH_C1.append(NH_C)
#     NH_C_err1.append(NH_C_err)
#     Gamma_hc1.append(Gamma_hc)
#     Gamma_hc_err1.append(Gamma_hc_err)
#     log_qh1.append(log_qh)
#     log_qh_err1.append(log_qh_err)
#     tau1.append(tau)
#     tau_err1.append(tau_err)
#     titannorm1.append(titannorm)
#     titannorn_err1.append(titannorn_err)


# In[7]:


#converting all the tuples to paramters
# chistat=np.asarray(chistat)
# logxi_C1=np.asarray(logxi_C1)
# logxi_C_err1=np.asarray(logxi_C_err1)
# logxi_C_err1=logxi_C_err1[:, 0:2]
# NH_C1=np.asarray(NH_C1)
# NH_C_err1=np.asarray(NH_C_err1)
# NH_C_err1=NH_C_err1[:, 0:2]
# Gamma_hc1=np.asarray(Gamma_hc1)
# Gamma_hc_err1=np.asarray(Gamma_hc_err1)
# Gamma_hc_err1=Gamma_hc_err1[:, 0:2]
# log_qh1=np.asarray(log_qh1)
# log_qh_err1=np.asarray(log_qh_err1)
# log_qh_err1=log_qh_err1[:, 0:2]
# tau1=np.asarray(tau1)
# tau_err1=np.asarray(tau_err1)
# tau_err1=tau_err1[:, 0:2]
# titannorm1=np.asarray(titannorm1)
# titannorn_err1=np.asarray(titannorn_err1)
# titannorn_err1=titannorn_err1[:, 0:2]

# chistat=np.reshape(np.asarray(chistat),(2,1))
# logxi_C1=np.reshape(np.asarray(logxi_C1),(2,1))
# logxi_C_err1=np.reshape(np.asarray(logxi_C_err1),(2,1))
# NH_C1=np.reshape(np.asarray(NH_C1),(2,1))
# NH_C_err1=np.reshape(np.asarray(NH_C_err1),(2,1))
# Gamma_hc1=np.reshape(np.asarray(Gamma_hc1),(2,1))
# Gamma_hc_err1=np.reshape(np.asarray(Gamma_hc_err1),(2,1))
# log_qh1=np.reshape(np.asarray(log_qh1),(2,1))
# log_qh_err1=np.reshape(np.asarray(log_qh_err1),(2,1))
# tau1=np.reshape(np.asarray(tau1),(2,1))
# tau_err1=np.reshape(np.asarray(tau_err1),(2,1))
# titannorm1=np.reshape(np.asarray(titannorm1),(2,1))
# titannorn_err1=np.reshape(np.asarray(titannorn_err1),(2,1))

# #final=np.insert(logxi_C1, 0,chistat, axis=1)
# #final=[chistat,logxi_C1];
# final=np.column_stack((chistat,logxi_C1,logxi_C_err1,NH_C1,NH_C_err1,Gamma_hc1,Gamma_hc_err1,log_qh1,log_qh_err1,tau1,tau_err1,titannorm1,titannorn_err1))


# In[8]:


#print(chistat)
#print(logxi_C1)
# print(final.shape)


# In[12]:


#("chistat","logxi_C1","logxi_C_err1","NH_C1","NH_C_err1","Gamma_hc1","Gamma_hc_err1","log_qh1","log_qh_err1","tau1","tau_err1","titannorm1","titannorn_err1")
# path='/vol1/Objects/AGN/POP_2018/'
# os.chdir(path)
# np.savetxt("res_titan.txt",(final), delimiter=',',header="chistat,logxi_C1,logxi_C_err1,NH_C1,NH_C_err1,Gamma_hc1,Gamma_hc_err1,log_qh1,log_qh_err1,tau1,tau_err1,titannorm1,titannorn_err1",fmt='%.9f')


# In[18]:


# for d in ./*/*;do [[ -d "$d" ]] && echo "${d##./}" >> objectnames.txt; done       ---> to get object names list
#freq=np.loadtxt("objectnames.txt",delimiter="/",dtype=str)
freq=Counter(freq[:,0])  #frequency of observations per source
freq=list(freq.values())
galactic_nh=["1.31e-2","3.26e-2","4.16e-2","6.82e-2","1.41e-2","2.60e-2","1.59e-2","4.09e-2","5.16e-2","2.93e-2","4.44e-2","2.05e-2","5.93e-2","3.51e-2","3.22e-2","1.85e-2","1.46e-2","2.10e-2","1.44e-2","1.08e-2","1.94e-2","1.36e-2","6.61e-2"]
redshifts=[".1040",".0455",".5725","0.0858",".0435",".2362",".0304",".0257",".0343",".0263",".0374",".0090","0.01627",".1",".0640",".1438",".1765",".0882",".1640",".0790",".1641",".0424",".0221"]


# In[25]:


k,indx=0,0
chistat,logxi_C1,logxi_C_err1,NH_C1, NH_C_err1, Gamma_hc1,Gamma_hc_err1, log_qh1,log_qh_err1, tau1,tau_err1, titannorm1, titannorn_err1=[],[],[],[],[],[],[],[],[],[],[],[],[]
for i in range(len(level2)):
    
    path=os.chdir(level2[i])
    fitperform(specfiles[i],galactic_nh[indx],redshifts[indx])
    chistat.append(c)
    
    logxi_C1.append(logxi_C)
    logxi_C_err1.append(logxi_C_err)
    NH_C1.append(NH_C)
    NH_C_err1.append(NH_C_err)
    Gamma_hc1.append(Gamma_hc)
    Gamma_hc_err1.append(Gamma_hc_err)
    log_qh1.append(log_qh)
    log_qh_err1.append(log_qh_err)
    tau1.append(tau)
    tau_err1.append(tau_err)
    titannorm1.append(titannorm)
    titannorn_err1.append(titannorn_err)
    
    
    k+=1
    if k==freq[indx]:
        indx+=1
        k=0


# In[26]:


chistat=np.reshape(np.asarray(chistat),(len(level2),1))
logxi_C1=np.reshape(np.asarray(logxi_C1),(len(level2),1))
logxi_C_err1=np.reshape(np.asarray(logxi_C_err1),(len(level2),1))
NH_C1=np.reshape(np.asarray(NH_C1),(len(level2),1))
NH_C_err1=np.reshape(np.asarray(NH_C_err1),(len(level2),1))
Gamma_hc1=np.reshape(np.asarray(Gamma_hc1),(len(level2),1))
Gamma_hc_err1=np.reshape(np.asarray(Gamma_hc_err1),(len(level2),1))
log_qh1=np.reshape(np.asarray(log_qh1),(len(level2),1))
log_qh_err1=np.reshape(np.asarray(log_qh_err1),(len(level2),1))
tau1=np.reshape(np.asarray(tau1),(len(level2),1))
tau_err1=np.reshape(np.asarray(tau_err1),(len(level2),1))
titannorm1=np.reshape(np.asarray(titannorm1),(len(level2),1))
titannorn_err1=np.reshape(np.asarray(titannorn_err1),(len(level2),1))

#final=np.insert(logxi_C1, 0,chistat, axis=1)
#final=[chistat,logxi_C1];
final=np.column_stack((chistat,logxi_C1,logxi_C_err1,NH_C1,NH_C_err1,Gamma_hc1,Gamma_hc_err1,log_qh1,log_qh_err1,tau1,tau_err1,titannorm1,titannorn_err1))


# In[24]:


#print(log_qh1)


# In[ ]:


path='/work/bpalit/Objects/AGN/POP_2018/'
os.chdir(path)
#np.savetxt("res_titan_Gammatied_noinitial_chi_2.txt",(final), delimiter=',',header="chistat,logxi_C1,logxi_C_err1,NH_C1,NH_C_err1,Gamma_hc1,Gamma_hc_err1,log_qh1,log_qh_err1,tau1,tau_err1,titannorm1,titannorn_err1",fmt='%.9f')
print("FINISHED")
