#Question to answer
#1.	How many times is each reference cited? Specifically how many References have 0 citations?
#2.	What citations don’t have a matching Reference?
#3.	What References are not in alphabetical order by first author?
#4.	What Citations use et al. incorrectly?
#5.	What Citations incorrect syntax. E.g. (Hopkinson, 2023) states…or .(Hopkinson, 2023) rather than (Hopkinson, 2023).
#6.	What References are not perfect Harvard syntax, such as , & or mixture of & and and etc. 
#7      Mismatch in year
#table
#citation 1 End of sentence
#Citation 2 body of text
#Correct citation column 3 or more put et al

#search where text(column)in dataframe rows is on page then seach
#check italics in et al, if not italicized its wrong or no fullstop

#column:process text citation 1 and 2 in text
#found:found in references
#interested in ones with zero (Present/ not present)
####
#ADD ET AL ITALICS AND EXTRACTED CITATIONS

#Two table References/ TEXT


from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import pdfplumber
import tempfile
import pandas as pd
from refextract import extract_references_from_file
import tkinter as tk
from tkinter import filedialog
from IPython.display import HTML, display
import re
import fitz  # PyMuPDF
import numpy as np
import nltk

app = Flask(__name__)
app.secret_key = 'Ref_Buster_2023'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
pattern = r"\b(?!(?:Although|Also)\b)(?:[A-Z][A-Za-z'`-]+)(?:,? (?:(?:and |& )?(?:[A-Z][A-Za-z'`-]+)|(?:et al.?)))*(?:,? *(?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?| *\((?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?\))"
#global_pattern = r'\b(?!(?:Although|In|Furthermore|Additionally|Also|In\s\d{4})\b)(?!(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b)(?:[A-Z][A-Za-z\'`-]+)(?:,? (?:(?:and |& )?(?:[A-Z][A-Za-z\'`-]+)|(?:et al.?)))*(?:,? *(?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?| *\((?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?\))'
global_pattern = r"\b(?!(?:Although|In|Furthermore|Additionally|Also)\b)(?!(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b)(?:[A-Z][A-Za-z'`-]+)(?:,? (?:(?:and |& )?(?:[Z-Z][A-Za-z'`-]+)|(?:et al.?)))*(?:,? *(?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?| *\((?:19|20)[0-9][0-9](?:, p\.? [0-9]+)?\))"
           

################################################################################################################################################################


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            all_text += text + '\n\n'
    return all_text

def extract_citations_from_pdf(pdf_path):
    try:
        cite_text =''
        pdf_document = fitz.open(pdf_path)

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            cite_text += page.get_text("text")#concatinate text from each page
        pdf_document.close()
        return cite_text
    except fitz.FileNotFoundError:
        return "File not found or inaccessible"
#################################################################################

def check_references_alphabetical_order(text):
    #basic pattern
    references = re.findall(r'\. (.*\([A-Za-z]+ .* [0-9]+\)\.+?)|\. (.*\([A-Za-z]+ .* [0-9]+\)[^\.]+\.+?)', text)
    # Sorting the references and comparing them to the original list
    sorted_references = sorted(references, key=lambda x: x.lower())
    return references == sorted_references

##################################Reference order check#####################################################################################################################################
def order_check(text):
    if check_references_alphabetical_order(text):
        return("References in the PDF are in alphabetical order")
    else:
        return("References in the PDF are not in alphabetical order")

#Output reference order check
ref_order= order_check('text')
##################################Et al Italics Check############################################
def check_italics_in_et_al_citations(pdf_path):
    pdf_document = fitz.open(pdf_path)
    italics_found = False
    output = ""

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        blocks = page.get_text("dict", flags=11)["blocks"]

        for block in blocks:
            if block.get("type") == 0:  # Type 0 represents text
                for line in block["lines"]:
                    for span in line["spans"]:
                        if "et al." in span["text"]:
                            if "italic" in span["font"].lower():
                                output += f"Found italic 'et al.' on Page {page_num + 1}"
                                italics_found = True
    pdf_document.close()
    if not italics_found:
        output += "No occurrences of 'et al.' in italics were found in the PDF."
    return output


###################################################################################################################################################################
############################### Functions to generate Harvard citations

def generate_harvard_citation_1(row):
    authors = row['author']
    year = row['year'][0]

    # Check if 'et al.' is present in the author names
    if any('et al.' in author for author in authors):
        return f"{authors[0]} ({year})"  # Use the first author with 'et al.' and the year
    else:
        total_surnames = count_surnames(authors)
        if total_surnames == 1:
            # Use the first surname and the year
            surname = re.findall(r'[A-Z][a-z]+', authors[0])[0]
            return f"{surname} ({year})"
        elif total_surnames == 2:
            # Use the first and second surnames joined by 'and' and the year
            surnames = re.findall(r'[A-Z][a-z]+', authors[0])
            return f"{surnames[0]} and {surnames[1]} ({year})"
        elif total_surnames == 3:
            # Use the first and second surnames joined by 'and' and the year
            surnames = re.findall(r'[A-Z][a-z]+', authors[0])
            return f"{surnames[0]}, {surnames[1]} and {surnames[2]} ({year})"
        elif total_surnames >= 4:
            # Use the first surname and 'et al.' with the year
            surname = re.findall(r'[A-Z][a-z]+', authors[0])[0]
            return f"{surname} et al. ({year})"
        else:
            return ""

def generate_harvard_citation_2(row):
    authors = row['author']
    year = row['year'][0]

    # Check if 'et al.' is present in the author names
    if any('et al.' in author for author in authors):
        return f"({authors[0]}, {year})"  # Use the first author with 'et al.' in parenthesis and the year
    else:
        total_surnames = count_surnames(authors)
        if total_surnames == 1:
            # Use the first surname and the year in parenthesis
            surname = re.findall(r'[A-Z][a-z]+', authors[0])[0]
            return f"({surname}, {year})"
        elif total_surnames == 2:
            # Use the first and second surnames joined by 'and' with the year in parenthesis
            surnames = re.findall(r'[A-Z][a-z]+', authors[0])
            return f"({surnames[0]} and {surnames[1]}, {year})"
        elif total_surnames == 3:
            # Use the first and second surnames joined by 'and' with the year in parenthesis
            surnames = re.findall(r'[A-Z][a-z]+', authors[0])
            return f"({surnames[0]}, {surnames[1]} and {surnames[2]}, {year})"
        elif total_surnames >= 4:
            # Use the first surname and 'et al.' with the year in parenthesis
            surname = re.findall(r'[A-Z][a-z]+', authors[0])[0]
            return f"({surname} et al., {year})"
        else:
            return ""

def check_citation_presence(row, text):
    harvard_citation_1 = row['Harvard Citation 1']
    harvard_citation_2 = row['Harvard Citation 2']

    count_citation_1 = text.count(harvard_citation_1)
    count_citation_2 = text.count(harvard_citation_2)

    row['Harvard Cite 1'] = '✔' if count_citation_1 > 0 else '❌'
    row['Harvard Cite 2'] = '✔' if count_citation_2 > 0 else '❌'

    if count_citation_1 + count_citation_2 == 0:
        row['Number of times Cited'] = 'Not cited/Havard'
    else:
        row['Number of times Cited'] = count_citation_1 + count_citation_2

    return row

#####

def extract_citations_for_author(author_name, text):
    # Extract the surname as the first word before the comma in the author row
    author = author_name[0]
    # Extract the surname
    author_surname = author.split(',')[0].strip() if author else None
    
    # Define the pattern to find citations for the extracted author surname
    author_citation_pattern = rf'\b({author_surname}\s+\(\d{{4}}\)|{author_surname}\s+\d{{4}}|INFOCOM \d{{4}})'  # Include INFOCOM citation format

    
    # Find all citations matching the author surname pattern in the PDF text
    citations = re.findall(author_citation_pattern, text)
    return citations if citations else '-'

############ Function to count authors############################################
def count_surnames(authors):
    total_surnames = 0
    for entry in authors:
        # Extract surnames using a regex pattern for the last name
        surnames = re.findall(r'[A-Z][a-z]+\s*,', entry)
        total_surnames += len(surnames)
    return total_surnames

###########################Table 1 Function to process REFCHECKS#########################
def process_other_functions(text):
    references = [] 
    # Create a temp file to store the extracted text
    if text:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as text_file:
            text_file.write(text)
            text_filename = text_file.name
        
        references = extract_references_from_file(text_filename)
    else:
        print("Text data is empty or invalid.")

    with open('extracted_text.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        
    #Reference Dataframe
    df = pd.DataFrame(references)
    df = df.reset_index(drop=True)
    auth_years =(df[['author', 'year']])
    auth_year = auth_years.dropna()
    auth_year['Authors'] = auth_year['author'].apply(count_surnames)
    auth_year['Harvard Citation 1'] = auth_year.apply(generate_harvard_citation_1, axis=1)
    # Apply the function to create matching citations
    auth_year['Harvard Citation 2'] = auth_year.apply(generate_harvard_citation_2, axis=1)
    auth_year = auth_year.apply(check_citation_presence, axis=1, args=(text,))
    # New column to store citations for each author
    auth_year['Other citations for Author'] = auth_year['author'].apply(
        lambda author: extract_citations_for_author(author, text)
    )


    auth_count=HTML(auth_year.to_html(classes='table table-stripped'))
    
    # Calculate the percentages
    cited_count = (auth_year['Number of times Cited'] != 'Ref not cited/Havard').sum()
    not_cited_count = (auth_year['Number of times Cited'] == 'Ref not cited/Havard').sum()
    # Calculate total count of references
    total_count = len(auth_year)
    percent_cited = (cited_count / total_count) * 100
    percent_not_cited = (not_cited_count / total_count) * 100

    # Summary with counts and percentages
    summary_df = pd.DataFrame({
        'Total': [total_count],
        'Cited': [cited_count],
        'Not Cited': [not_cited_count],
        '% Cited': [percent_cited],
        '% Not Cited': [percent_not_cited]
    })
    marks_df = HTML(summary_df.to_html(classes='table table-stripped'))
    #combined DataFrame to a CSV file
    combined_df = pd.concat([summary_df, auth_year], ignore_index=True)
    combined_df.to_csv('reference_data.csv', index=False)        
    
    return {
        'Alphabet Check': ref_order,
        'Author Count': auth_count,
        'REFERENCE CITED RESULT': marks_df,
        #'Author Year Data': auth_year
    }

########################Access Ref check results in CSV#########################################################
@app.route('/downloadref_csv_file')
def downloadref_csv_file():
    csv_file_path = 'reference_data.csv'  # Path to your generated CSV file
    return send_file(csv_file_path, as_attachment=True)

@app.route('/downloadcite_csv_file')
def downloadcite_csv_file():
    csv_file_path = 'citation_data.csv'  # Path to your generated CSV file
    return send_file(csv_file_path, as_attachment=True)

import citations

def process_cite_functions(pdf_path):
    italics_check=check_italics_in_et_al_citations(pdf_path)
    citation_text= extract_citations_from_pdf(pdf_path)
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
            author = re.sub(r'\(\)', '', author)  # Remove remaining parentheses
        else:
            year = None
            author = citation.strip()

        return {'Author': author, 'Year': year}

    df[['Author', 'Year']] = df['Citations'].apply(extract_author_and_year).apply(pd.Series)
    dfc = df.reset_index(drop=True)
    cita_year = dfc.dropna()
#############In Sentence POSITION OF CITATION ###############################
    def cite_sentence_position(citation):
        pattern =global_pattern
        citations = re.findall(pattern, citation_text)
        #Creating a list to store positions
        positions = []

        for citation in citations:
            #Checking citation position in sentence
            position = None
            if citation_text.startswith(citation):
                position = "At Start Please check!!"
            elif citation_text.endswith(citation):
                position = "✔"
            else:
                position = "✔"
            positions.append((citation, position))
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
    return { 'Italics check':italics_check, 'Citations in PDF': citedf}
###################################################################################
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and file.filename.endswith('.pdf'):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('process_file', filename=file.filename))
    else:
        return render_template('error.html', error_message='Invalid file format. Please upload a PDF file.')

@app.route('/process/<filename>', methods=['GET', 'POST'])
def process_file(filename):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if request.method == 'POST':
        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(pdf_path)
        citation_text= extract_citations_from_pdf(pdf_path)

        # Process other functions
        results = process_other_functions(text)
        citeresults = process_cite_functions(pdf_path)
        
        italics_result = check_italics_in_et_al_citations(pdf_path)
        if italics_result:
            flash(italics_result)

        return render_template('report.html', results=results, citeresults=citeresults, italics_result=italics_result)

    return render_template('process_file.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
