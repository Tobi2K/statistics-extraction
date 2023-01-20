# Reducing a Set of Regular Expressions and Analyzing Differences of Domain-specific Statistic Reporting

---
This repository provides the code for the paper 'Reducing a Set of Regular Expressions and Analyzing Differences of Domain-specific Statistic Reporting'.
This paper is an extension of [STEREO](https://arxiv.org/abs/2103.14124) ([Code](https://github.com/Foisunt/STEREO)), which was published in iiWAS2021.
STEREO is an statistics extraction tool, that uses regular expressions to extract statistics from scientific papers.

We provide code for finding a minimal set of regular expressions. In our case we apply this minimal set algorithm to the set of regular expressions used in STEREO to extract statistics.
STEREO was previously trained on papers from the life sciences and medical domain.
We extend STEREO to a new domain, namely Human-Computer-Interaction.
Here, we learn new rules and expand STEREO to be able to use PDF and LaTeX file as an input, instead of only JSON files.


## Getting Started
For the correct functionality, we recommend using Python 3.8. You can create a new virtual environment or use your global one.
Install the requirements by running:
``` shell
pip install -r requirements.txt
```
For the use of the interactive GUI for ActiveWrapper learning you need to install `tkinter`. For more information see [here](https://docs.python.org/3/library/tkinter.html).
Also, the package `pdftotext` is required for parsing PDF files. Follow the installation instructions [here](https://pypi.org/project/pdftotext/) to ensure the correct functionality.

Additionally, you should download the [CORD-19](https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge) and [arXiv](https://www.kaggle.com/datasets/Cornell-University/arxiv) datasets and place them in the folders `Cord-19` and `arXiv-papers` respectively.
For the arXiv papers, we recommend using a crawler, to crawl papers by URL, for example by adapting the 2Like [crawler](https://github.com/Data-Science-2Like/arXive-crawler) we used.
The folder [paper-gathering](paper-gathering) contains a notebook to generate a file containing arXiv URLs filtered by arXiv tag from the [metadata list](https://www.kaggle.com/datasets/Cornell-University/arxiv).

For more information see the [technical report](./Technical_Report.pdf).

## File structure

> See the READMEs in the sub-folders for more information on the respective features.

    .
    ├── arXiv-papers                # Contains the arXiv papers ...
    │   ├── pdf                     # ... as PDF
    │   └── tex                     # ... as LaTeX
    ├── Cord-19                     # Contains the CORD-19 papers.
    │   └── document_parses
    │       └── pdf_json            # This folder should contain a lot of .json files
    ├── inclusion-stats             # Contains a notebook that generates some plots for our inclusion algorithm.
    ├── paper-gathering             # Contains a notebook that filters papers by arXiv tag and generates a list of URLs.
    ├── regex-inclusion             # Contains the code for our regular expression inclusion algorithm
    ├── STEREO                      # Contains some general files for STEREO
    │   └── Code                    # Contains the code for our extended STEREO implementation
    ├── testing-playground          # Contains some unfinished tests, not that important
    └── Technical_Report.pdf        # Describes this project in more detail


## License
MIT License

Copyright (c) 2022 Tobias Kalmbach

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
