# W2V4IRA
Applying word embeddings to support Inter Rater Agreement 

This repository contains the scripts and word embedding models related to snomed ct. 
In order to generate new models you will need to provide the snomed ct full relationship file from the available distribution.

## Scripts
- generate_SCT_corpus_full_relationship.py

  This script uses the snomed ct Relationship file and produces a textual representation of the terminology.

- read_save_w2v_models.py

  This script read the textual representation of SCT and produces some word embedding models using gensim library.

-  read_coding_annotations.py

  This script parses the resulting annotations from INCEPTION project and extract the set of codes for the chunks with broad scope that includes all related codes. It uses cassis library to obtain the codes from the annotated texts.

## Models
- SCT_model_CBOW.model
- SCT_model_Skip.model

# Acknowledgemnts
This reposity contains work done during the research stay of Jose Antonio Miñarro Giménez at Shulz' group at the department of Medical informatics, statistics and documentation (Medical University of Graz).
Este trabajo es resultado de la estancia 22205/EE/23 financiada por la Fundación Séneca-Agencia de Ciencia y Tecnología de la Región de Murcia (https://www.fseneca.es/) con cargo al Programa Regional de Movilidad, Colaboración e Intercambio de Conocimiento “Jiménez de la Espada”.
![Fundación Séneca](https://www.fseneca.es/web/sites/all/themes/fuse17/img/fseneca-color.svg)
