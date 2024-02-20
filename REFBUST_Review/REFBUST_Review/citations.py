
import re


def find_harvard_citations_one_author(text):
    pattern = r'\(\w+\s?,\s?\d{4}\)'  # Regular expression pattern for Harvard-style citations like (Author, Year)
    citations = re.findall(pattern, text)
    return citations

def find_harvard_citations_two_authors(text):
    pattern = r'\(\w+\s?&\s?\w+,\s?\d{4}\)'  # Regular expression pattern for Harvard-style citations with two authors like (Author1 & Author2, Year)
    citations = re.findall(pattern, text)
    return citations

def find_harvard_citations_three_authors(text):
    pattern = r'\(\w+\s?,\s?\w+\s?&\s?\w+,\s?\d{4}\)'  # Regular expression pattern for Harvard-style citations with three authors like (Author1, Author2 & Author3, Year)
    citations = re.findall(pattern, text)
    return citations

def find_harvard_citations_et_al(text):
    pattern = r'\(\w+\s?(?:,?\s?\w+)?(?:,?\s?\w+)?\s?et al.,\s?\d{4}\)'  # Regular expression pattern for Harvard-style citations with "et al." like (Author1 et al., Year)
    citations = re.findall(pattern, text)
    return citations

def find_author_year_citations(text):
    pattern = r'\b\w+\s?\(\d{4}\)'  # Regular expression pattern for citations in the format "Author (Year)"
    citations = re.findall(pattern, text)
    return citations

def find_author_and_author_year_citations(text):
    pattern = r'\b\w+\s?&\s?\w+\s?\(\d{4}\)'  # Regular expression pattern for citations in the format "Author & Author (Year)"
    citations = re.findall(pattern, text)
    return citations

def find_author_comma_author_and_author_year_citations(text):
    pattern = r'\b\w+\s?,\s?\w+\s?&\s?\w+\s?\(\d{4}\)'  # Regular expression pattern for citations in the format "Author, Author & Author (Year)"
    citations = re.findall(pattern, text)
    return citations

def find_author_et_al_year_citations(text):
    pattern = r'\b\w+\s?et\s?al\.\s?\(\d{4}\)'  # Regular expression pattern for citations in the format "Author et al. (Year)"
    citations = re.findall(pattern, text)
    return citations

def find_all_citations (text):
    citations = find_harvard_citations_one_author(text)
    citations = citations + find_harvard_citations_two_authors(text)
    citations = citations + find_harvard_citations_three_authors(text)
    citations = citations + find_harvard_citations_et_al(text)
    citations = citations + find_author_year_citations(text)
    citations = citations + find_author_and_author_year_citations(text)
    citations = citations + find_author_comma_author_and_author_year_citations(text)
    citations = citations + find_author_et_al_year_citations(text)
    return citations





