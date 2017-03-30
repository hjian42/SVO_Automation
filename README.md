# SVO Triplet Automation of Narrative Stories for Social Sciences 

The goal of the project is to build the pipeline to automate the process of generating the SVO triplets for the use of social science. 
For example, character relatioonships can be visualized using networks in Ghephi based on SVO triplets. 

The whole pipeline is composed of three steps:
  - Data Cleaning 
  - Anaphora Resolution 
  - SVO Triplets Extraction
 
## Data Cleaning
  - Clean data converted from pdf format
  - Extract titles and contents of Emory Lynching articles and separate them into two parts 
 
## Anaphora Resolution 
  - Replace mentions of entities with their most possible representations in the Emory Lyching Dataset based on the result of Stanford CoreNlp Anaphora Resolution
  
  For example: 
  
  `Bill Cato Attempted to Assault Mrs. Vickers. He was shot to death.` will look like 
  `Bill Cato Attempted to Assault Mrs. Vickers. Bill Cato was shot to death.` after anaphora resolution.

## SVO Extraction 
  - Format Emory Lynching Corpus `cleaned_corenlp_lynching.txt` into `clausie_input.txt` to be ready for ClausIE in order to get triplets
  - Extract only SVO's from `sentences-test-out.txt` to `svo.txt`
  - Filter SVO sets by preserving the ones only confirmed verbs and actors of our interest into `terminal_svo.txt`
  
  The SVO results will look like the following:
      
      V: attempt, S: negress, O: murder
      V: enter, S: mob, O: cell
      V: shot, S: winslow, O: winslow
  
##  Dependencies:
  - Stanford CoreNlp 
  - NLTK
  - ClausIE
  - enchant
  
