import os
import csv
import yake
import docx2txt
import pdfplumber
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from odt2txt import OpenDocumentTextFile


def read_pdf(path):
    """Extract the text in a pdf file

    :param path: path of the pdf file
    :type path: str
    :return: text in the pdf file
    :rtype: str
    """
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                text += page.extract_text()
    except:
        print(f'Cannot read pdf file {path}, skipping ')
    return text


def read_docx(path):
    """Extract the text in a docx file

    :param path: path of the docx file
    :type path: str
    :return: text in the docx file
    :rtype: str
    """
    return docx2txt.process(path)


def read_odt(path):
    """Extract the text in an odt file

    :param path: path of the odt file
    :type path: str
    :return: text in the odt file
    :rtype: str
    """
    return OpenDocumentTextFile(path).toString()


def save_keywords(keywords, file_name):
    """
    :param keywords: dictionnary keywords score pairs
    :type keywords: dict
    :param file_name: name of the csv file to save the keywords
    :type file_name: str
    """
    field_names = ['Keywords', 'Score']
    list_keywords = [{'Keywords': key, 'Score': value}
                     for key, value in keywords.items()]
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(list_keywords)


def extract_text(path='.'):
    """Extract and lowercase the text of all pdf,odt and docx documents in a
        folder

    :param path: path of the folder containing the documents
    :type path: str
    :return: lowercased text of all documents
    :rtype: str
    """
    text = ""
    for i, file in enumerate(os.listdir(path)):
        nb_files = len(os.listdir(path))
        file = os.path.join(path, file)
        print(f'Progression {i+1}/{nb_files}', end='\r')
        if file.endswith('.pdf'):
            text += read_pdf(file) + '\n'
        if file.endswith('.docx'):
            text += read_docx(file) + '\n'
        if file.endswith('.odt'):
            text += read_odt(file) + '\n'
    return text.lower()


def get_keywords(text,
                 max_nb_words=2,
                 nb_key_words=50,
                 anti_dict_file='antidictionnary.txt',
                 lan='en',
                 pdf_file='keywords.pdf',
                 csv_file='keywords.csv'):
    """Return the keywords of the text in input, display them as a word cloud
        and save the word clous in a pdf file

    :param text: text from which the keywords are to be extracted
    :type text: str
    :param max_nb_words: max number of words that make a keyword
    :type max_nb_words: int
    :param anti_dict_file: file containing the list of words to remove from
        the text
    :type anti_dict_file: str
    :param lan: language in the pdf files
    :type lan: str
    :param pdf_file: file where the wordcould will be saved
    :type pdf_file: str
    :param csv_file: file where the keywords will be saved
    :type csv_file: str
    :return: list of tuple(keyword, score) orderdes from most important
        keyword (lowest score) to least important
    :rtype: list
    """
    extractor = yake.KeywordExtractor(
        lan=lan,
        n=max_nb_words,
        top=nb_key_words
    )

    with open(anti_dict_file, 'r') as file:
        anti_dict = {word.lower().strip() for word in file}

    for a in anti_dict:
        text = text.replace(a, '')

    keywords = extractor.extract_keywords(text)
    keywords = {key: int(1/value) for key, value in keywords
                if len(set(key.split())) == len(key.split())}
    save_keywords(keywords, csv_file)
    wordcloud = WordCloud(
        width=2000,
        height=1000).generate_from_frequencies(keywords)
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud)
    plt.savefig(pdf_file)
    return keywords
