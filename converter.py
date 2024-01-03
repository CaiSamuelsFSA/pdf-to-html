import pdfplumber

def pdf_to_html(input_pdf_path, output_html_path):
    with pdfplumber.open(input_pdf_path) as pdf:
        html_content = ""
        lastsize = 0
        output = ""
        count = 0
        occurrence = 0
        closeTag = ""
        sizes = []
        isBold = []
        boldText = False

        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]

            for element in pdf.chars:
                sizes.append(element['size'])
                output += element['text']
                if "Bold" in element['fontname']:
                    isBold.append(True)
                else:
                    isBold.append(False)

            sizes = [round(x) for x in sizes]

            uniqueSizes = set(sizes)
            uniqueSizesSort = list(uniqueSizes)
            uniqueSizesSort.sort()

            text = page.extract_text()
            # Iterate through text elements and assign corresponding font sizes
            for i, text_element in enumerate(text):
                font_size = sizes[count]
                if output[count] != " ":
                    occurrence = 0
                if text_element == output[count]:
                    count += 1
                elif output[count] == " ":
                    occurrence += 1
                    count += occurrence
                    font_size = sizes[count]
                if font_size != lastsize:
                    html_content += f'{closeTag}'
                if font_size == lastsize:
                    pass
                elif font_size == uniqueSizesSort[-1]:
                    html_content += '<h1>'
                    closeTag = "</h1>"
                elif font_size == uniqueSizesSort[-2]:
                    html_content += '<h2>'
                    closeTag = "</h2>"
                else:
                    html_content += '<p>'
                    closeTag = "</p>"
                if isBold[count] == True and boldText == False:
                    html_content += '<b>'
                    boldText = True
                elif isBold[count] == False and boldText == True:
                    text_element += '</b>'
                    boldText = False
                html_content += f'{text_element}'
                lastsize = font_size

        # Write HTML content to the output file
        with open(output_html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

pdf_to_html('./files/recall.pdf', './files/output.html')