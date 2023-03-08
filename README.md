# testing branch 

# LoadDataGenerator

Generates CSV files to be used in LoadData module (CellProfiler).

When analysing images with [CellProfiler](https://github.com/CellProfiler/CellProfiler) (1), you might want to use LoadData to replace the Input modules. We have used LoadData together with [Distributed-CellProfiler](https://github.com/DistributedScience/Distributed-CellProfiler) (2) to run analysis inside AWS. 

With this notebook you can:

1. Generate LoadData CSVs with FileName, PathName, Metadata such as Well, Site and Plate names;
2. Generate command to upload the CSVs and local images into AWS S3 bucket using AWS cli.

## Requirements

Create an Anaconda Environment and pip install the following libraries:

```
conda create --name loaddata python=3.9
```

```
pip install easygui
pip install ipywidgets
pip install pyperclip
```

## Use

1. Clone this repository on your local computer. Open an Anaconda prompt inside the cloned folder and activate the environment:

```
conda activate loaddata
```

2. Open the notebook and follow the instructions there.


## References
(1) Stirling DR, Swain-Bowden MJ, Lucas AM, Carpenter AE, Cimini BA, Goodman A (2021). CellProfiler 4: improvements in speed, utility and usability. BMC Bioinformatics, 22 (1), 433. . PMID: 34507520 PMCID: PMC8431850.

(2) https://arxiv.org/abs/2210.01073