def has_odd(L):
   v=len(L)
   if v % 2 == 1:
      return True
   else:
      return False

from pyparsing import OneOrMore, Word, alphas, Suppress

# Define the parser to extract authors from the Harvard reference string 
comma = Suppress(",")
and_ = Suppress("and")
initial = ""

# Define a pattern for author names (assuming they're composed of alphabetic characters)
author_name = Word(alphas + "-.")

# Define the pattern for multiple authors separated by commas and 'and'
authors = OneOrMore(author_name + (comma | and_ | initial))

# Example Harvard reference string
harvard_reference = "Smith, J. , Johnson, A. B., and Williams,C. D.W."
#harvard_reference = "J. Smith, A. Johnson, and C. D.W. Williams"

harvard_reference = harvard_reference.replace(", ", ",")
print (harvard_reference )
harvard_reference = harvard_reference.replace(". ", ".")
print (harvard_reference)
harvard_reference = harvard_reference.replace(",and", " and")
harvard_reference = harvard_reference.replace(".and", "and")
print (harvard_reference)
# Parse the authors from the reference string

parsed_authors = authors.parseString(harvard_reference)
print (parsed_authors)
# Output the extracted authors
if has_odd(parsed_authors):
    print("error!")
else:
    parsed_authors = parsed_authors[::2]
print (parsed_authors)