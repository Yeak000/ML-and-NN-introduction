import numpy as np
from numpy import (max,min,pi,exp,log)
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
gna, gk, gl = 120, 36, 0.3
vna, vk, vl = 50, -77, -54.5


def get_am(v):
    return 0.1*(v+40)/(1-exp(-0.1*(v+40)))


def get_ah(v):
    return 0.07*exp(-0.05*(v+65))


def get_an(v):
    return 0.01*(v+55)/(1-exp(-0.1*(v+55)))


def get_bm(v):
    return 4*exp(-(v+65)/18)


def get_bh(v):
    return 1/(1+exp(-0.1*(v+35)))


def get_bn(v):
    return 0.125*exp(-(v+65)/80)


def get_m(v):
    return get_am(v) / (get_am(v)+get_bm(v))


def get_h(v):
    return get_ah(v) / (get_ah(v) + get_bh(v))


def get_n(v):
    return get_an(v) / (get_an(v) + get_bn(v))


def get_i(v):
    return gna*get_m(v)**3*get_h(v)*(v-vna)+gk*get_n(v)**4*(v-vk)+gl*(v-vl)


def two_divide(left=-100,right=-20,i=0.0):
    nl = get_i(left)
    nr = get_i(right)
    nm = get_i((left+right)/2)
    while abs(nm-i)>1e-6:
        if nm-i > 0:
            right = (left+right)/2
        else:
            left = (left+right)/2
        nm = get_i((left+right)/2)
        # print(nm)
        # print(left,right)
    return (left+right)/2

def get_jac(v):
    m=get_m(v)
    h=get_h(v)
    n=get_n(v)

    df1_dv = -gna*m**3*h-gk*n**4-gl
    df1_dm = -3*m**2*gna*h*(v-vna)
    df1_dh = -gna*m**3*(v-vna)
    df1_dn = -4*gk*n**3*(v-vk)

    dam_dv = (0.1-(0.5+0.01*v)*exp(-0.1*(v+40)))/(1-exp(-0.1*(v+40)))**2
    dbm_dv = -4/18*exp(-(v+65)/18)
    dah_dv = -0.05*0.07*exp(-0.05*(v+65))
    dbh_dv = -0.1*exp(0.1*(v+35))/(1+exp(0.1*(v+35)))**2
    dan_dv = (0.1-(0.65+0.01*v)*exp(-0.1*(v+55)))/(1-exp(-0.1*(v+55)))**2
    dbn_dv = -1/640*exp(-(65+v)/80)

    df2_dv = (1-m)*dam_dv-m*dbm_dv
    df2_dm = -(get_am(v)+get_bm(v))

    df3_dv = (1-h)*dah_dv - h*dbh_dv
    df3_dh = -(get_ah(v)+get_bh(v))

    df4_dv = (1-n)*dan_dv - n*dbn_dv
    df4_dn = -(get_an(v)+get_bn(v))

    jac = np.zeros((4, 4))
    jac[0,0] = df1_dv
    jac[0,1] = df1_dm
    jac[0,2] = df1_dh
    jac[0,3] = df1_dn

    jac[1,0] = df2_dv
    jac[1,1] = df2_dm

    jac[2,0] = df3_dv
    jac[2,2] = df3_dh

    jac[3,0] = df4_dv
    jac[3,3] = df4_dn
    return jac
# df = []
# for k in np.arange(6.24,6.25,0.0001):
#     v0 = two_divide(i=k)
#     if v0 in [-40,-65,-55]:
#         v0 += 0.02
#     jac = get_jac(v0)
#     eig = np.linalg.eigvals(jac)
#     df.append(eig)
# df1 = pd.DataFrame(df)
def simu(i):
    v0 = two_divide(i=0)
    am = get_am(v0)
    bm = get_bm(v0)
    ah = get_ah(v0)
    bh = get_bh(v0)
    an = get_an(v0)
    bn = get_bn(v0)
    m = get_m(v0)
    h = get_h(v0)
    n = get_n(v0)
    delta = 0.01
    v0_l = [v0]
    for j in range(19999):
        # print(v0)
        v0 += (i-(gna*m**3*h*(v0-vna)+gk*n**4*(v0-vk)+gl*(v0-vl)))*delta
        v0_l.append(v0)
        am = get_am(v0)
        bm = get_bm(v0)
        ah = get_ah(v0)
        bh = get_bh(v0)
        an = get_an(v0)
        bn = get_bn(v0)
        m += delta*(-(am+bm)*m+am)
        h += delta*(-(ah+bh)*h+ah)
        n += delta*(-(an+bn)*n+an)


    return v0_l
i = 6.245
l = simu(i)
plt.subplot(2,2,1)
plt.plot(0.01*np.arange(20000),l)
plt.xlabel(f'I={i}mA/cm2')
plt.ylabel('V(mV)')

plt.subplot(2,2,2)
i = 6.255
l = simu(i)
plt.plot(0.01*np.arange(20000),l)
plt.xlabel(f'I={i}mA/cm2')
plt.ylabel('V(mV)')

plt.subplot(2,2,3)
i = 100
l = simu(i)
plt.plot(0.01*np.arange(20000),l)
plt.xlabel(f'I={i}mA/cm2')
plt.ylabel('V(mV)')

plt.subplot(2,2,4)
i = 158
l = simu(i)
plt.plot(0.01*np.arange(20000),l)
plt.xlabel(f'I={i}mA/cm2')
plt.ylabel('V(mV)')
def get_iv():
    v_l=[]
    for k in tqdm(np.arange(0,180,0.5)):
        l = simu(k)
        v_l.append(max(l[-3000:])-min(l[-3000:]))
    return v_l

# v_l = get_iv()