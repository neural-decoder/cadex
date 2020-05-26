# -*- coding: utf-8 -*-

# =============================================================================
# Created By  : Damien Depannemaecker
# Created Date: Wednesday 26th February 2020
# =============================================================================



from brian2 import *


start_scope()

#integration step
DT=0.001
defaultclock.dt = DT*ms


#simulation duration
TotTime=500
duration = TotTime*ms

#number of neuron
N1=1

eqs='''
dv/dt = (-gl*(v-El)+ gl*Dt*exp((v-Vt)/Dt)-ga*(v-Ea) + Is)/Cm : volt (unless refractory)
dga/dt = (ga_max/(1.0+exp((-Va-v)/Da))-ga)/tau_a:siemens
Is:ampere
Cm:farad
gl:siemens
El:volt
ga_max:siemens
tau_a:second
Dt:volt
Vt:volt
Va:volt
Da:volt
Ea:volt
'''


Dga = 3.0*nS

G1 = NeuronGroup(N1, eqs, threshold='v > -40.*mV', reset='v = -65*mV; ga += Dga', refractory='5*ms', method='heun')
#init:
G1.v = -65*mV
G1.ga = 0.0*nS

#parameters
G1.Cm = 200.*pF
G1.gl = 10.*nS
G1.El = -60.*mV
G1.Vt = -50.*mV
G1.Dt = 2.*mV
G1.tau_a = 500.0*ms
G1.Va = 65.*mV
G1.Da = 5.*mV
G1.ga_max = 0.0*nS
G1.Ea = -70.*mV
G1.Is = 1.0*nA

# record variables
Mon_v  = StateMonitor(G1, 'v', record=range(N1))
Mon_ga = StateMonitor(G1, 'ga', record=range(N1))

print('--##Start simulation##--')
run(duration)


#plot
fig=plt.figure(figsize=(12,4))
fig.suptitle('CAdEx')
ax1=fig.add_subplot(121)
ax2=fig.add_subplot(122)
ax1.set_title("V")
ax1.set_title("ga")
ax1.plot(Mon_v.t/ms, Mon_v[0].v/mV)
ax2.plot(Mon_ga.t/ms, Mon_ga[0].ga/nS)

plt.show()