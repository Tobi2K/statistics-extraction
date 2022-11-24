# STEREO Extension
Here we describe, how to use the STEREO tool. For more details see the [original technical report](../Technical_Report_STEREO.pdf) and the [edited technical report](../../Technical_Report.pdf) for this project.

The main functionality can be found in [ActiveWrapper.py](ActiveWrapper.py) for the active wrapper learning of new rules and [StatExtraction.py](StatExtraction.py) for the statistics extraction and evaluation.

> Remember to install the packages found in [../../requirements.txt](../../requirements.txt) in your (virtual) environment.
## Active Wrapper 
The active wrapper learning can be started by simply running  
``` shell
python ActiveWrapper.py
```

`ActiveWrapper.py` has three optional parameters:
* `--path`: The location (a directory) containing the files on which to perform the active wrapper learning (default: `../../Cord-19/document_parses/pdf_json`)
* `--tex`: Directs the active wrapper to use tex (or more accurately .tar.gz) files (default: `False`)
* `--pdf`: Directs the active wrapper to use PDF files (default: `False`)

If neither `--tex` nor `--pdf` is True, the active wrapper automatically uses .json files.
If both are True, LaTeX files are used.

For example, to start the active wrapper learning on arXiv papers in .tar.gz files located at [../../arXiv-papers/tex](../../arXiv-papers/tex), run:
```shell
python ActiveWrapper.py --path '../../arXiv-papers/tex' --tex True
```

## Statistics Extraction
The stat extraction can be started by running  
``` shell
python StatExtraction.py -ex {source} {target} {fileExtension}
```

* `fileExtension` is the file type you wish to extract from. Possible values:
  * `.json`
  * `.pdf`
  * `.tar.gz`
* `source` needs to be a file of the type `fileExtension`
* `target` is the name of the file that the extracted stats will be saved in

Alternatively, you can add `-d` before `source` to extract from a directory (`source` then has to be a path to a directory instead)

For example, to extract statistics from .pdf files located at [../../arXiv-papers/pdf](../../arXiv-papers/pdf) and save the extracted statistics in a file called `extractedPdf.json`, run:
```shell
python StatExtraction.py -ex -d ../../arXiv-papers/pdf/ extractedPdf.json .pdf
```

## Statistics Evaluation
The evaluation of statistics can be started by running  
``` shell
python StatExtraction.py -ev {samplesize} {type} {source} {fileExtension?}
```

* `type`: the statistic type to be evaluated
* `samplesize`: number of statistics to be randomly sampled of the statistic type `type`
* `source`: location of a json file created by the extraction using the previous step
* `fileExtension`: only required for evaluation of R- rules. In this case `source` also has to be a directory

For example, to evaluate a sample of 200 Student t-Tests from a file containing extracted statistics located at `./extracted.json`, run:
```shell
python StatExtraction.py -ev 200 ttest extracted.json
```
