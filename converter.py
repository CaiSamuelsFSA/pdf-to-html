import pdfplumber

font_sizes = []

def pdf_to_html(input_pdf_path, output_html_path):
    with pdfplumber.open(input_pdf_path) as pdf:
        html_content = ""
        lastsize = 0
        output = ""
        count = 0
        occurrence = 0

        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]

            for element in pdf.chars:
                font_sizes.append(element['size'])
                output += element['text']

            text = page.extract_text()
            # Iterate through text elements and assign corresponding font sizes
            for i, text_element in enumerate(text):
                font_size = font_sizes[count]
                if output[count] != " ":
                    occurrence = 0
                if text_element == output[count]:
                    count += 1
                elif output[count] == " ":
                    occurrence += 1
                    count += occurrence
                    font_size = font_sizes[count]
                if font_size == lastsize:
                    html_content += f'{text_element}'
                else:
                    html_content += f'</span><span style="font-size: {font_size}pt;"><br>{text_element}'
                lastsize = font_size

        # Write HTML content to the output file
        with open(output_html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

pdf_to_html('./files/recall.pdf', './files/output.html')