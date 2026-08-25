# dLFE_UTR_RTS_analysis  
The code for computational implementation of *"Metagenomic mining of translational coupling elements enables programmable gene expression of polycistronic systems in E. coli"*.  
This pipeline identifies the 5'-UTR/-CDS regions for all UTNI gene, TeRe gene, and Leading gene. It calculates ΔLFE (delta-LFE, RNA folding free energy offset), supports multispecies batch analysis and generates publication-ready visualization outputs.    

**Code origin note**: This pipeline is adapted from the computational method published in *Chemla, Y., et al. A possible universal role for mRNA secondary structure in bacterial translation revealed using a synthetic operon. Nat. Commun. 11, 4827 (2020). https://doi.org/10.1038/s41467-020-19291-1*. We reuse and refactor core algorithm logic; third-party dependency modules (codon_randomization.py) are directly imported without modification.  

# Project Structure   

dLFE_UTR_RTS_analysis/  
├── README.md                     # Documentation and usage guide    
├── config.py                     # Global configuration: file paths, window-parameters, plotting styles    
├── codon_randomization.py        # Synonymous-codon permutation for CDS, nucleotide permutation for UTR     
├── rnafold_vienna.py             # Wrapper for Vienna RNA RNAfold to compute local free energy (LFE)    
├── core_extract_allgene.py       # Core gene identification logic for UTNI-gene/Leading-gene/TeRe-gene    
├── utils_dlfe.py                 # Utility toolkit: gff/fasta parsing, sequence extraction, ΔLFE computation, plotting routines    
├── run_dLFE_allgene.py           # Main entry script: batch UTNI-gene/Leading-gene/TeRe-gene multispecies TCE analysis    
├── run_dLFE_allleadgeneRTS.py    # Independent entry script: Leading-RTS analysis (stop-codon-side 3'CDS-3'UTR)    
└── test_genome/                  # Input directory: stores paired `*.fasta` genome and `*.gff3` annotation files    
  
# Environment Setup  

For the convenience of researchers seeking seamless utilization, we have adhered to all environmental configurations as previously established in Michael Peeri's released RTS analysis toolkit (https://github.com/michaelpeeri/rnafold-rts-public).    
