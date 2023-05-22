import os
import PyPDF2
from user_data import Sent_applications
def rename_pdf_file(file_path, title_olympiad, name,surname,patronymic):

    new_file_name = f"{title_olympiad} {name} {surname} {patronymic}.pdf"

    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        with open(new_file_path, 'wb') as new_file:
            pdf_writer = PyPDF2.PdfWriter()


            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            pdf_writer.write(new_file)


    return new_file_path

