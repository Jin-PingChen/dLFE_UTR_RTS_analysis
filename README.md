# dLFE_UTR_RTS_analysis  
The code for computational implementation of *"Metagenomic mining of translational coupling elements enables programmable gene expression of polycistronic systems in E. coli"*.  

**Code origin note**: This pipeline is adapted from the computational method published in Chemla et al., Nature Communications, 2020, *A possible universal role for mRNA secondary structure in bacterial translation revealed using a synthetic operon*. We reuse and refactor core algorithm logic; third?party dependency modules are directly imported without modification.  

This pipeline identifies the 5'-UTR and 5'-cds regions of UTNI gene, TeRe gene, and Leading?gene. It calculates ΔLFE (delta-LFE, RNA folding free energy offset), supports multi?species batch analysis and generates publication?ready visualization outputs.  

# Project Structure   

dLFE_UTR_RTS_analysis/
├── README.md                     # Documentation and usage guide  
├── config.py                     # Global configuration: file paths, gene-call thresholds, window-parameters, plotting styles  
├── codon_randomization.py        # Sequence randomization module: synonymous-codon permutation for CDS, nucleotide permutation for UTR, used for ΔLFE background control  
├── rnafold_vienna.py             # Wrapper for Vienna?RNA RNAfold to compute local free energy (LFE)  
├── core_extract_allgene.py       # Core gene?identification logic for UTNI-gene/Leading-gene/TeRe-gene  
├── utils_dlfe.py                 # Utility toolkit: gff/fasta parsing, sequence extraction, ΔLFE computation, plotting routines  
├── run_dLFE_allgene.py           # Main entry script: batch UTNI-gene/Leading-gene/TeRe-gene multispecies TCE analysis  
├── run_dLFE_allleadgeneRTS.py    # Independent entry script: Leading-RTS analysis (stop-codon-side 3'CDS-3'UTR)  
└── test_genome/                  # Input directory: stores paired `*.fasta` genome and `*.gff3` annotation files  
  
# Environment Setup  

For the convenience of researchers seeking seamless utilization, we have adhered to all environmental configurations as previously established in Chemla's released RTS analysis toolkit(https://github.com/michaelpeeri/rnafold-rts-public).    
