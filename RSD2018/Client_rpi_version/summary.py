#!/usr/bin/python

import mes_api

print("\n \n \n ")
print("###########")
print("# SUMMARY #")
print("########### \n")

file = open("start_time.txt", "r")
print (file.readline())

ft = mes_api.get_time(9)
print("The system was stopped " + ft + "\n")