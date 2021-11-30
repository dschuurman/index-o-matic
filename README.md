# index-o-matic

This program helps to create an index for a PDF manuscript. It requires a plaintext file of index terms
and a PDF manuscript. It creates a plaintext output file named `index.txt`.

Note that the code is able to perform a case-insesntive search and is able to spot hyphenated occurrences of words.

## Dependencies

This project uses Python version 3 and relies on having the 
[pdfgrep](https://pdfgrep.org) package installed and accessible
from the command-line.

## Configuration

This code includes several constants that need to be adjusted for your manuscript and your environment. These include:
- `INDEX_TERMS_FILENAME`: is the name of a plaintext file with a list of index terms (one per line)
- `OUTPUT_FILENAME`: the output filename that will be created containing the index
- `BOOK_PDF_FILENAME`: the filename of the PDF manuscript
- `PDFGREP`: the full path for `pdfgrep`
- `PAGE_OFFSET`: the offset between PDF page numbers and the actual page numbers used in the manuscript
- `MAX_INDEX_PAGE`: the maximum page number use in the index (this can be used to
prevent endnotes from being indexed)

## Disclaimer

This code still requires human eyes - it is unaware of context, but it can provide a quick initial draft index.

This program arose from the need to create an index for a book project. 
It is provided "as is" without any warranty, expressed or implied, about merchantability or fitness for a particular purpose. Your mileage may vary.
