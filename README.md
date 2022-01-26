# README

## Presentation
A python script to extract keywords from pdf, odt and docx documents

## Installation
```
git clone https://github.com/Jibril-Frej/keywords.git
cd keywords
pip install -r requirements.txt
git clone https://github.com/LIAAD/yake.git
cd yake
python setup.py install
sed -i '137s/.*/            if ( cdigit > 3 and calpha > 0 ) or (cdigit == 0 and calpha == 0) or len([c for c in word if c in self.exclude]) > 1:/' yake/datarepresentation.py
```
