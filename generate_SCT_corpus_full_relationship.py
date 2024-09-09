
from optparse import IndentedHelpFormatter
import os
from pydoc import getpager
from re import T
from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings

warnings.filterwarnings(action='ignore')

## Script to parse SCT Relationship file and obtain a data structure with all relationships stored. 
# The resulting data structure follows this representatiom -> {source_concept:{group_in_cronce:{realti_concept:[target_concept]}}}
# For 766705006 we can have -> {
#                                   766705006:{
#                                       0:{
#                                           116680003:[414030009, 234632005, 36138009],
#                                           42752001:[409709004]
#                                       },
#                                       1:{
#                                           363698007:[116003000],
#                                           246454002:[255399007]
#                                       },
#                                       2:{
#                                           42752001:[409709004]
#                                       }
#                                   }
#                               }


input_file = "sct_Relationship_Full_20240301.txt"
output_file = "sct_corpus_randomWalks_v2.txt"
is_a = "116680003"

def parse_sct_rel(file):
    dict_root = {}
    firstLine=True

    with open(file) as f:
        for line in f.readlines():
            if firstLine:
                firstLine=False
                continue
        
            a = line.split("\t")
            if a[2] == '1':
                source_concept = a[4]
                target_concept = a[5]
                group_in_conce = a[6]
                relati_concept = a[7]
                dict_source = {}
                if source_concept in dict_root.keys():
                    dict_source = dict_root[source_concept]
                else:
                    dict_root[source_concept]=dict_source
                
                dict_group = {}
                if group_in_conce in dict_source.keys():
                    dict_group = dict_source[group_in_conce]
                else:
                    dict_source[group_in_conce] = dict_group

                list_rel = []
                if relati_concept in dict_group.keys():
                    list_rel = dict_group[relati_concept]
                else:
                    dict_group[relati_concept]=list_rel

                if target_concept not in list_rel:
                    list_rel.append(target_concept)
    return dict_root

def get_parents(child, data):
    result = []
    if child in data:
        dict_source = data[child]
        for key_group in dict_source:
            dict_group = dict_source[key_group]
            for key_rel in dict_group:
                if key_rel == is_a:
                    list_targets = dict_group[is_a]
                    for target in list_targets:
                        if target not in result:
                            result.append(target)

    return result


def get_children(parent, data):
    result=[]
    for key_source in data:
        dict_source = data[key_source]
        for key_group in dict_source:
            dict_group = dict_source[key_group]
            for key_rel in dict_group:
                if key_rel == '116680003':
                    list_targets = dict_group[key_rel]
                    for target in list_targets:
                        if target == parent:
                            result.append(key_source)
    return result

def parser_hierarchy_file(file):
    data={}
    with open(file) as f:
       for line in f.readlines():
           a = line.split("\t")
           data[a[0]] = a[1:]
    return data


def generate_hierarchy(w,data,hierarchy,parent):
    if parent not in hierarchy.keys():
        children = get_children(parent, data)
        hierarchy[parent] = children
        if len(children) != 0:
            w.write(parent)
            for child in children:
                w.write("\t"+child)
            w.write("\n")
        #print(parent+"\t"+str(hierarchy[parent]))
        for child in children:
            if child not in hierarchy.keys():
                generate_hierarchy(w,data,hierarchy,child)


def permutations(elements):
    if len(elements) <= 1:
        yield elements
        return
    for perm in permutations(elements[1:]):
        for i in range(len(elements)):
            # nb elements[0:1] works in both string and list contexts
            yield perm[:i] + elements[0:1] + perm[i:]


def getExpression(dict_group):
    elements = []
    for group in dict_group.keys():
        dict_rel = dict_group[group]
        for rel in dict_rel:
            list_target = dict_rel[rel]
            expression = ""
            for target in list_target:
                expression = rel+" "+target
                if expression not in elements:
                    elements.append(expression)
    return elements



def parse_tree_hierarchy(sct_rel_data, file):
    data = {}
    for key_source in sct_rel_data:
        dict_source = sct_rel_data[key_source]
        for key_group in dict_source:
            dict_group = dict_source[key_group]
            for key_rel in dict_group:
                if key_rel == '116680003':
                    list_targets = dict_group[key_rel]
                    for target in list_targets:
                        if target not in data.keys():
                            data[target] = []
                        data[target].append(key_source)

    with open(file,"w") as w:
        for k in data.keys():
            w.write(k)
            for v in data[k]:
                w.write("\t"+v)
            w.write("\n")
    return data

def parse_inv_tree_hierarchy(sct_rel_data):
    data = {}
    for key_source in sct_rel_data:
        data[key_source] = []
        dict_source = sct_rel_data[key_source]
        for key_group in dict_source:
            dict_group = dict_source[key_group]
            for key_rel in dict_group:
                if key_rel == '116680003':
                    list_targets = dict_group[key_rel]
                    for target in list_targets:
                        data[key_source].append(target)
    """
    with open(file,"w") as w:
        for k in data.keys():
            w.write(k)
            for v in data[k]:
                w.write("\t"+v)
            w.write("\n")
    """
    return data

def recurrsive_tree(tree, inferred_tree, parents, current):
    if current not in tree.keys():
        return
    ancestors = [current]
    ancestors.extend(parents)
    for child in tree[current]:
        if child not in inferred_tree:
            inferred_tree[child] = []
        inferred_tree[child].extend(ancestors)
        recurrsive_tree(tree,inferred_tree, ancestors, child)
        
    return parents

def get_inferred_inv_tree(inv_tree):
    inferred_inv_tree = {}
    for concept in inv_tree:
        inferred_inv_tree[concept] = get_parents(inv_tree,concept)
    return inferred_inv_tree

def get_parents(inv_tree, concept):
    to_visit = []
    visited = []
    to_visit.extend(inv_tree[concept])
    
    while len(to_visit) > 0:
        parent = to_visit[0]
        to_visit.remove(parent)
        if parent in visited:
            continue
       
        visited.append(parent)

        if parent in inv_tree:
            to_visit.extend(inv_tree[parent])
    
    return visited

def get_inferred_tree_expressions(inferred_tree, concept_expression, inferred_concept_expressions):
    for concept in inferred_tree:
        expressions = []
        if concept in concept_expression:
            expressions.extend(concept_expression[concept])
        
        ancestors = inferred_tree[concept]
        for parent in ancestors:
            if parent in concept_expression:
                expressions.extend(concept_expression[parent])

        inferred_concept_expressions[concept] = expressions



sct_rel_data = parse_sct_rel(input_file)
tree_hierarchy = parse_tree_hierarchy(sct_rel_data,"sct_tree_hierarchy.txt")
inv_tree_hierarchy = parse_inv_tree_hierarchy(sct_rel_data)
root_concept = '138875005' # 138875005 |SNOMED CT Concept (SNOMED RT+CTV3)|
inferred_inv_tree_hierarchy = {}
inferred_inv_tree_hierarchy = get_inferred_inv_tree(inv_tree_hierarchy)
#recurrsive_tree(tree_hierarchy,inferred_inv_tree_hierarchy,[],root_concept)
concept_expression = {}
for concept in sct_rel_data:
    expression = getExpression(sct_rel_data[concept])
    concept_expression[concept] = expression

inferred_concept_expressions = {}
get_inferred_tree_expressions(inferred_inv_tree_hierarchy, concept_expression, inferred_concept_expressions)


with open(output_file, 'w') as w:
    to_visit = [root_concept]
    visited = []
    while len(to_visit) > 0:
        parent = to_visit[0]
        to_visit.remove(parent)
        if parent in visited:
            continue
        visited.append(parent)
        if parent not in tree_hierarchy:
            continue
       
        ###
        children = tree_hierarchy[parent]
        for child in children:
            if child not in visited:
                to_visit.append(child)
            w.write(parent+" 116680003 "+child+"\n")

            if child in tree_hierarchy:
                subChildren = tree_hierarchy[child]
                for subChild in subChildren:
                    w.write(parent+" 116680003 "+child+ " 116680003 "+subChild+"\n")
        
    to_visit = [root_concept]
    visited = []
    while len(to_visit) > 0:
        parent = to_visit[0]
        to_visit.remove(parent)
        if parent in visited:
            continue
        visited.append(parent)
        
        if parent in inferred_concept_expressions:
            for expression in inferred_concept_expressions[parent]:
                w.write(parent+" "+expression+"\n")

        if parent not in tree_hierarchy:
            continue

        children = tree_hierarchy
        for child in children:
            if child not in visited:
                to_visit.append(child)



"""
with open(output_file, 'w') as w:
    to_visit = [root_concept]
    visited = []
    while len(to_visit) > 0:
        parent = to_visit[0]
        to_visit.remove(parent)
        visited.append(parent)
        if parent not in tree_hierarchy:
            continue

        children = tree_hierarchy[parent]
        for child in children:
            if child not in visited:
                to_visit.append(child)
        
        res = permutations(children)
        for perm in res:
            expression = str(parent)+" 116680003"
            for item in perm:
                expression += " "+str(item)
                if item in tree_hierarchy:
                    subChildren = tree_hierarchy[item]
                    for subChild in subChildren:
                        expression += " 116680003 "+str(subChild)
            w.write(expression)    

    to_visit = [root_concept]
    visited = []
    while len(to_visit) > 0:
        parent = to_visit[0]
        to_visit.remove(parent)
        visited.append(parent)
        if parent not in sct_rel_data:
            continue

        expression = str(parent)+ " 116680003"
        expression += " "+getExpression(sct_rel_data[parent])
        
        if parent not in tree_hierarchy:
            continue
        children = tree_hierarchy
        for child in children:
            if child not in visited:
                to_visit.append(child)
"""