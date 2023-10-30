#!/usr/bin/env python
# coding:utf-8
"""
Name : parseTei.py
Author : Aurelia Vasile, MSH, UCA

Created on : 30/10/2023 09:42

"""
import xml.etree.ElementTree as ET
import string
NAMESPACES = {
            "tei": "http://www.tei-c.org/ns/1.0"
        }

# récupère la racine
tree = ET.parse("data/teiCorpus_TestMeline_V1.xml")
root = tree.getroot()
#print (root)

with open("data/iramuteqFormat.txt", "w") as fichier:

    # le préfixe tei est un ns par défaut; il faut le rajouter à chaque path
    for entretien in root.findall('.//tei:TEI', NAMESPACES):
        fichier.write("**** ")
        dictionnairesThemes ={}
        for person in entretien.findall(".//tei:listPerson/tei:person", NAMESPACES):
            sexe = person.attrib.get("sex")
            age = person.attrib.get("age")
            fichier.write("*sexe_"+sexe+ " " + "*age_"+age+"\n")
        for replique in entretien.findall(".//tei:u", NAMESPACES):
            if replique.attrib.get("who") != '#MD':
                segments = replique.findall(".//tei:seg", NAMESPACES)
                for seg in segments:
                    theme = seg.attrib.get("ana").replace("#", "-*")
                    if theme in dictionnairesThemes:
                        texteTheme = seg.text.replace("  ", "").replace("\n", " ")
                        dictionnairesThemes[theme].append(texteTheme)
                    else:
                        texteTheme = seg.text.replace("  ", "").replace("\n", " ")
                        dictionnairesThemes[theme] = [texteTheme]

        for key, val in dictionnairesThemes.items():
            fichier.write(key + "\n" + " ".join(val) +'\n')
    print(dictionnairesThemes)









