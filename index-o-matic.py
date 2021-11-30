# index-o-matic.py
# (C) 2020 Derek Schuurman
# License: GNU General Public License (GPL) v3
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Creates a file of index terms from a PDF manuscript.
# Input: file listing index terms (plain text) and a manuscript (PDF)
# Output: a index file (plain text)
# Requires: pdfgrep command-line tool to be installed.

from subprocess import Popen, PIPE

INDEX_TERMS_FILENAME = 'index-terms.txt'
OUTPUT_FILENAME = 'index.txt'
BOOK_PDF_FILENAME = 'book.pdf'
PDFGREP = '/opt/homebrew/bin/pdfgrep'
ENCODING = 'utf-8'

# Set the page offset to make the PDF page numbers
# correspond the the actual book page numbers
PAGE_OFFSET = 12

# Limit the search up to MAX_INDEX_PAGE
MAX_INDEX_PAGE = 208

index_file = open(OUTPUT_FILENAME,'w')
terms_file = open(INDEX_TERMS_FILENAME, 'r')

print('Beginning search for the following index words...')

# Read each index term and search for it in the book
for word in terms_file:
    word = word.strip()
    if word == 'end':
        break

    # If line is empty or commented out, continue at top of loop
    if word == '' or word[0] == '#':
        continue
    print(word, end=': ', flush=True)
    index_file.write(word + ': ')

    # Search for word (without hyphens) by starting pdfgrep process
    p = Popen([PDFGREP, '-in', '-C 1', word, BOOK_PDF_FILENAME], stdout=PIPE)
    output, errors = p.communicate()
    results = str(output, ENCODING)

    # Look for all possible hyphenated versions of the word using regex
    for i in range(1,len(word)-1):
        hyphenated_word = word[0:i] + '-[^a-zA-Z0-9]*' + word[i:]
        p = Popen([PDFGREP, '-in', '-C 1', hyphenated_word, BOOK_PDF_FILENAME], stdout=PIPE)
        output, errors = p.communicate()
        output = str(output, ENCODING)
        if output != '':
            results += output
            
    # If nothing found, continue to next index term
    if results == '':
        continue
    
     # Collect all the page numbers found in a list
    results = results.split('\n')
    page_nums = []
    for line in results:
        if line == '':
            break
        if not ':' in line[0:4]:
            continue
        page = int(line.split(':')[0])
        page -= PAGE_OFFSET
        if page < 0 or page > MAX_INDEX_PAGE:
            continue
        page_nums.append(page)

    # Sort and remove duplicate page numbers in list
    page_nums = list(set(page_nums))
    page_nums.sort()

    # If no results found, write newline to output file and continue to next term
    if (len(page_nums)==0):
        index_file.write('\n')
        continue

    # If pages found, write comma-separated list of pages to output file
    for i in range(len(page_nums)):
        if i < len(page_nums)-1:
            page = '{}, '.format(page_nums[i])
        else:
            page = '{}\n'.format(page_nums[i])
        index_file.write(page)
        print(page, end='')

 # Close input and output files
terms_file.close()
index_file.close()
