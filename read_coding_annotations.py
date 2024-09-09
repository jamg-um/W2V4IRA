from cassis import *
from zipfile import ZipFile
import pprint
import os
import sys
import os.path

def read_files(dir,annotator,f):
    if not os.path.exists('./annotation/'+dir.strip()+'/'+annotator+'.zip'):
        return
    with ZipFile('./annotation/'+dir.strip()+'/'+annotator+'.zip') as zf:
        with zf.open("TypeSystem.xml") as xml:
            typesystem = load_typesystem(xml)
        if not annotator+".xmi" in zf.namelist():
            return
        with zf.open(annotator+".xmi") as xmi:
            cas = load_cas_from_xmi(xmi, typesystem=typesystem)
    visited=[]
    lista = cas.select('webanno.custom.Relation')
    for i1 in range(len(lista)):
        rel1 = lista[i1]
        if rel1 in visited:
            continue
        pairRel=[rel1]
        impairRel=[rel1]
        for i2 in range(i1+1,len(lista)):
            rel2 = lista[i2]
            if (not rel1.get_covered_text().strip()) or (not rel2.get_covered_text().strip()):
                continue
            if rel2.Governor.xmiID == rel1.Governor.xmiID and rel2.Relation == rel1.Relation and rel2.Dependent.xmiID != rel1.Dependent.xmiID:
                pairRel.append(rel2)
            if rel2.Governor.xmiID != rel1.Governor.xmiID and rel2.Relation == rel1.Relation and rel2.Dependent.xmiID == rel1.Dependent.xmiID:
                impairRel.append(rel2)

        if len(pairRel) > 1:
            startBegin = rel1.Governor.begin
            if startBegin > rel1.Dependent.begin :
                startBegin = rel1.Dependent.begin
            endFinish = rel1.Governor.end
            if endFinish < rel1.Dependent.end :
                endFinish = rel1.Dependent.end
                
            for r in pairRel:
                if startBegin > r.Governor.begin:
                    startBegin = r.Governor.begin
                if startBegin > r.Dependent.begin:
                    startBegin = r.Dependent.begin
                if endFinish < r.Governor.end:
                    endFinish = r.Governor.end
                if endFinish < r.Dependent.end:
                    endFinish = r.Dependent.end

            text = cas.sofa_string[startBegin:endFinish+1]
            for r in pairRel:
                f.write(text+"\t"+r.Governor.Concept+"\t"+r.Relation+"\t"+r.Dependent.Concept+"\n")
            visited.extend(pairRel)
            pairRel=[]
        if len(impairRel) > 1:
            startBegin = rel1.Governor.begin
            if startBegin > rel1.Dependent.begin :
                startBegin = rel1.Dependent.begin
            endFinish = rel1.Governor.end
            if endFinish < rel1.Dependent.end :
                endFinish = rel1.Dependent.end
                
            for r in impairRel:
                if startBegin > r.Governor.begin:
                    startBegin = r.Governor.begin
                if startBegin > r.Dependent.begin:
                    startBegin = r.Dependent.begin
                if endFinish < r.Governor.end:
                    endFinish = r.Governor.end
                if endFinish < r.Dependent.end:
                    endFinish = r.Dependent.end

            text = cas.sofa_string[startBegin:endFinish+1]
            for r in impairRel:
                f.write(text+"\t"+r.Governor.Concept+"\t"+r.Relation+"\t"+r.Dependent.Concept+"\n")
            visited.extend(pairRel)
            impairRel=[]


with open('annotations.txt', 'w') as f:
    for root, dirs, files in os.walk(r'./annotation'):
        for dir in dirs:
            read_files(dir,"heba",f)
            read_files(dir,"admin",f)
            read_files(dir,"jennifer",f)
            read_files(dir,"sareh",f)            

            """
            with ZipFile("./annotation/"+dir+'/heba.zip') as zf:
                with zf.open("TypeSystem.xml") as xml:
                    typesystem = load_typesystem(xml)
                with zf.open("heba.xmi") as xmi:
                    cas = load_cas_from_xmi(xmi, typesystem=typesystem)
            visited=[]
            lista = cas.select('webanno.custom.Relation')
            for i1 in range(len(lista)):
                rel1 = lista[i1]
                if rel1 in visited:
                    continue
                pairRel=[rel1]
                for i2 in range(i1+1,len(lista)):
                    rel2 = lista[i2]
                    if (not rel1.get_covered_text().strip()) or (not rel2.get_covered_text().strip()):
                        continue
                    
                    if rel2.Governor.xmiID == rel1.Governor.xmiID and rel2.Relation == rel1.Relation and rel2.Dependent.xmiID != rel1.Dependent.xmiID:
                        pairRel.append(rel2)
                
                if len(pairRel) < 2:
                    continue
                print("pairRel=",end="")
                for i in pairRel:
                    print(str(i.xmiID)+",",end="")
                print("")

                startBegin = rel1.Governor.begin
                if startBegin > rel1.Dependent.begin :
                    startBegin = rel1.Dependent.begin
                endFinish = rel1.Governor.end
                if endFinish < rel1.Dependent.end :
                    endFinish = rel1.Dependent.end
                
                for r in pairRel:
                    if startBegin > r.Governor.begin:
                        startBegin = r.Governor.begin
                    if startBegin > r.Dependent.begin:
                        startBegin = r.Dependent.begin
                    if endFinish < r.Governor.end:
                        endFinish = r.Governor.end
                    if endFinish < r.Dependent.end:
                        endFinish = r.Dependent.end

                text = cas.sofa_string[startBegin:endFinish+1]
                for r in pairRel:
                    f.write(text+"\t"+r.Governor.Concept+"\t"+r.Relation+"\t"+r.Dependent.Concept+"\n")
                visited.extend(pairRel)
                pairRel=[]
               """ 
sys.exit(0)

with open('typesystem.xml', 'rb') as f:
    typesystem = load_typesystem(f)

with open('heba.xmi', 'rb') as f:
   cas = load_cas_from_xmi(f, typesystem=typesystem)



# Written to file
#cas.to_json("my_cas.json")
"""
print('\n\nvalores:\n')
for type in cas.typesystem.get_types():
    print(type.name)
"""

for att in cas.select('webanno.custom.CustomMCN'):
    print(att.get_covered_text())
    #pprint.pp(att)
    print('att:id={0} Concept={1}, Conceptcoverage={2}'.format(att.xmiID, att.Concept, att.Conceptcoverage))

for rel in cas.select('webanno.custom.Relation'):
    print(rel.get_covered_text())
    print('rel:id={0} Domain={1}, Range={2}'.format(rel.xmiID, rel.Governor.Concept, rel.Dependent.Concept))


"""
for token in cas.select('de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token'):
    print(token.get_covered_text())
    print('Token: begin={0}, end={1}, id={2}, order={3}'.format(token.begin, token.end, token.id, token.order))
    #print("begin="+token.begin)
    #print("end="+token.end)
"""