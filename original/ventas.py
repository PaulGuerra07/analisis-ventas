import pandas as pd
import numpy as np
import os, sys, time
d = pd.read_csv("C:/Users/Ventas/Desktop/ventas_2026.csv")
l = []
t = 0
def proceso():
    global t
    for i, r in d.iterrows():
        if r["cantidad"] > 0:
            try:
                x = r["cantidad"] * r["precio_unitario"] - r["cantidad"] * r["precio_unitario"] * r["descuento"]
            except:
                x = 0
            l.append(x)
            t = t + x
        else:
            l.append(0)
    d["total"] = l
    # costa
    s1 = 0
    for i, r in d.iterrows():
        if r["region"] == "Costa" or r["region"] == "costa" or r["region"] == "COSTA":
            s1 = s1 + r["total"]
    print("Costa: " + str(s1))
    # sierra
    s2 = 0
    for i, r in d.iterrows():
        if r["region"] == "Sierra" or r["region"] == "sierra" or r["region"] == "SIERRA":
            s2 = s2 + r["total"]
    print("Sierra: " + str(s2))
    # amazonia
    s3 = 0
    for i, r in d.iterrows():
        if r["region"] == "Amazonia" or r["region"] == "amazonia" or r["region"] == "AMAZONIA":
            s3 = s3 + r["total"]
    print("Amazonia: " + str(s3))
    p = []
    for i, r in d.iterrows():
        if r["producto"] not in p:
            p.append(r["producto"])
    res = []
    for a in p:
        s = 0
        for i, r in d.iterrows():
            if r["producto"] == a:
                s = s + r["total"]
        res.append([a, s])
    res.sort(key=lambda z: z[1], reverse=True)
    print("TOP 5: " + str(res[0:5]))
    print("TOTAL: " + str(t))
    f = open("reporte.txt", "w")
    f.write("Costa " + str(s1) + "\n" + "Sierra " + str(s2) + "\n" + "Amazonia " + str(s3) + "\n" + str(res[0:5]))
proceso()
