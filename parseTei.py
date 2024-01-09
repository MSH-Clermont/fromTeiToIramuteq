#!/usr/bin/env python
# coding:utf-8
"""
Name : parseTei.py
Author : Aurelia Vasile, MSH, UCA

Created on : 30/10/2023 09:42

"""
import xml.etree.ElementTree as ET
import re
NAMESPACES = {
            "tei": "http://www.tei-c.org/ns/1.0"
        }

# récupère la racine
tree = ET.parse("data/teiCorpus_V1.xml")
root = tree.getroot()
#print (root)

with open("data/iramuteqFormat_teiCorpus_V1.txt", "w") as fichier:

    # le préfixe tei est un ns par défaut; il faut le rajouter à chaque path
    for entretien in root.findall('.//tei:TEI', NAMESPACES):
        # chaque entretien doit commencer par les ****
        fichier.write("**** ")
        # liste qui va regrouper les métadonnées: les valeurs des attributs ana des balises rs
        listAttribPerformance =[]
        for rs in entretien.findall(".//tei:performance//tei:rs", NAMESPACES):
            attribPerformance = rs.attrib.get("ana").replace("#", "")
            listAttribPerformance.append(attribPerformance)
        # parcourir la liste de métadonnées et les écrire sur une ligne avec un espace entre elles
        for eachElement in listAttribPerformance:
            fichier.write("*attrib_"+eachElement+ " ")
        # le texte de l'entretien qui regroupe tous les textes directs et imbriqués de la balise U pour chaque personne interwieuvée
        cleanTextEntretien = ""
        # Pour chaque replique u
        for u in entretien.findall(".//tei:u", NAMESPACES):
            if u.attrib.get("who") != '#MD':
                # utilisation de itertext pour récupérer tous les textes imbriqués ou pas de chaque replique (u)
                repliqueInterview = "".join(u.itertext())
                # pour chaque réplique on supprime les espaces vides multiples et les retours à la ligne multiples
                multipleEmptyLinesRemoved = re.sub(r'[\n]{2,}', "", repliqueInterview)
                multipleSpacesRemoved = re.sub(r'[\s]{2,}', "", multipleEmptyLinesRemoved)
                # on concatène tous les u de l'entretien de la personne pour ne créer qu'un texte par personne
                cleanTextEntretien= cleanTextEntretien + multipleSpacesRemoved
        fichier.write("\n"+cleanTextEntretien+"\n\n")