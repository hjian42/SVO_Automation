# SVO Triplet Automation of Narrative Stories for Social Sciences 

The goal of the project is to build the pipeline to automate the process of generating SVO triplets for the use of social science research. For example, character relationships can be visualized using networks in Gephi based on SVO triplets. In the end, we want to integrate the pipeline into the NLP software [PC-ACE](https://pc-ace.com/) developed by Professor Roberto Franzosi at Emory from Sociology Department.

The whole pipeline is composed of three steps:
  - Data Cleaning 
  - Anaphora Resolution 
  - SVO Triplets Extraction
 
## Data Cleaning
  - Clean data converted from pdf format
  - Extract titles and contents of Emory Lynching articles and separate them into two parts 
 
## Anaphora Resolution: Stanford CoreNLP 
  - Replace mentions of entities (e.g. pronouns like "he" and "she") with their most representative representations using Stanford CoreNLP's coreference (anaphora) resolution
  - Used to maximize and validate SVO extraction by correctly identifying actors
  
  For example: 
  
  `Bill Cato Attempted to Assault Mrs. Vickers. He was shot to death.` will look like 
  `Bill Cato Attempted to Assault Mrs. Vickers. Bill Cato was shot to death.` after anaphora resolution.

## SVO Extraction: ClausIE 
  - Format Emory Lynching Corpus `cleaned_corenlp_lynching.txt` into `clausie_input.txt` to be ready for ClausIE in order to get triplets
  - Extract only SVO's from `sentences-test-out.txt` to `svo.txt`
  - Filter SVO sets into `terminal_svo.txt` by preserving only triplets with a confirmed social actor as the subject
  
  The SVO results will look like the following (verbs are converted into stem, so `estim` means `estimate`):
      
      S: mob            , V: estimate       , O: shooting       
      S: girl           , V: protect        , O: negro          
      S: prisoner       , V: have            , O: neck 

## Data Visualization
  - output file is ready to be seen by Gephi

            Node1     Edge      Node2
        0   people     have      wrath
        1   people     have      hands
        2   county     have       duty
        3  sheriff  convene      court
        4  sheriff      try  criminals
      
##  Dependencies:
  - Stanford CoreNlp 
  - NLTK
  - ClausIE
  - enchant

## Version 
Alpha Version. It is still up to changes in the future. Welcome any comments and advice. 
