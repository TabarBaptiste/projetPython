import PyPDF2

def merge_and_split_pdf(file1, file2, page_order, output):
    pdf_writer = PyPDF2.PdfWriter()

    with open(file1, 'rb') as file1:
        pdf1 = PyPDF2.PdfReader(file1)
        
        pages_file1 = [int(x[1:]) - 1 for x in page_order.replace('p', '').split(';') if x.startswith('1')]
        for page in pages_file1:
            pdf_writer.add_page(pdf1.pages[page])

        if file2:
            with open(file2, 'rb') as file2:
                pdf2 = PyPDF2.PdfReader(file2)

                pages_file2 = [int(x[1:]) - 1 for x in page_order.replace('p', '').split(';') if x.startswith('2')]
                for page in pages_file2:
                    pdf_writer.add_page(pdf2.pages[page])

    with open(output, 'wb') as out_file:
        pdf_writer.write(out_file)

merge_and_split_pdf('lettre.pdf', 'qrCodes.pdf', '1p0;2p0;1p1;2p1', 'output.pdf')
