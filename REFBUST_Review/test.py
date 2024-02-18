#!/usr/bin/env python
# coding: utf-8

# In[49]:





# In[17]:


def extract_text_from_pdf(pdf_path):
 with pdfplumber.open(pdf_path) as pdf:
     all_text = ""
     for page in pdf.pages:
         text = page.extract_text()
         all_text += text + '\n\n'
 return all_text


# In[18]:


def process_cite_functions(pdf_path):
#    italics_check=check_italics_in_et_al_citations(pdf_path)
    citation_text= extract_text_from_pdf(pdf_path)
#    matches = extract_pattern(citation_text)
    matches = citations.find_all_citations (citation_text)
    df = pd.DataFrame(matches, columns=['Citations'])
    df.drop_duplicates(subset='Citations', inplace=True)
    
    
    def extract_author_and_year(citation):
        # Define a regular expression pattern to match a year format '2000' or '(2000)'
        year_pattern = r'\b(?:\(\d{4}\)|\d{4})\b'
        year_match = re.search(year_pattern, citation)
        
        if year_match:
            year = year_match.group()
            author = citation.replace(year, '').strip()  # Extract author by removing year
  #          author = re.sub(r'\(\)', '', author)  # Remove remaining parentheses
            author = re.sub('\(', '', author)  # Remove remaining parentheses
            author = re.sub('\)', '', author)  # Remove remaining parentheses 
            author = re.sub('\,', '', author)  # Remove remaining parentheses
        else:
            year = None
            author = citation.strip()
        if (citation[0] == '('):
            form = 'end'
        else:
            form = 'in text'
        return {'Author': author, 'Year': year, 'Form': form}
    df[['Author', 'Year', 'Form']] = df['Citations'].apply(extract_author_and_year).apply(pd.Series)
    dfc = df.reset_index(drop=True)
    cita_year = dfc.dropna()
#############In Sentence POSITION OF CITATION ###############################
    def cite_sentence_position(citation):
             #Checking citation position in sentence
           # position = None
        if citation_text.find (citation + '.')!= -1:
                position = "At End of Sentence "
        else:
                position = "Not at end of sentence"
        return {'In Sentence Use': position}
    cita_year[['In Sentence Use']] = cita_year['Citations'].apply(cite_sentence_position).apply(pd.Series)
    specific_pattern = r"([A-Z][a-z]+) et al\.,? \(?(\d{4})\)?"
    generic_pattern = r"[A-Z][a-z]+ (?:et\,?\s?al\.,?|et al\.,?|et\,? al\.,?) \d{4}"

    def check_et_al_syntax(citation):
        if re.search(specific_pattern, citation):
            return '✔'
        elif re.search(generic_pattern, citation):
            return '❌'
        else:
            return 'n/a'

    # Applying the function to create the 'et_al syntax' column
    cita_year['et_al syntax'] = cita_year['Citations'].apply(check_et_al_syntax).apply(pd.Series)

    citedf=HTML(cita_year.to_html(classes='table table-stripped'))
    cita_year.to_csv('citation_data.csv', index=False)
    return { 'Citations in PDF': df}


# In[19]:


import citations
import fitz  # PyMuPDF
import pdfplumber
import re
import pandas as pd
from IPython.display import HTML, display


# In[20]:


global_pattern = r"\b(?!(?:Although|In|Furthermore|Additionally|Also)\b)(?!(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b)(?:[A-Z][A-Za-z'`-]+)(?:,? (?:(?:and |& )?(?:[Z-Z][A-Za-z'`-]+)|(?:et al.?)))*(?:,? *(?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?| *\((?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?\))"


# In[21]:


process_cite_functions("C:\\Users\\Glen\\OneDrive - Teesside University\\CIS4006 Advanced Practice\\External Students\\test.pdf")


# In[22]:


#process_cite_functions("C:\\Users\\u0037034\\OneDrive - Teesside University\\CIS4006 Advanced Practice\\External Students\\test.pdf")


# In[ ]:




