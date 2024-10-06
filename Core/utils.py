from docxtpl import DocxTemplate
import os
from .models import *
import subprocess  # For opening the document after generating

def generate_doc(student_id):
    student = Student.objects.get(id=student_id)
    
    # Define paths for the template and output
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, 'template.docx')
    output_path = os.path.join(current_directory, 'media', f'{student}.docx')
    
    # Prepare the replacements dictionary (placeholders and their values)
    replacement = {
        'student_id': student.num,
        'teacher': student.teacher.name,
        'level': student.level.name,
        'situ': student.situation,
        'StudentName': f'{student.first_name} {student.last_name}',
        'BirthDate': student.date_birth.strftime('%Y-%m-%d'),  # Format the date
        'Address': student.adress,
        'Class': f'{student.level.name} {student.level_year}',
        'ParentName': student.parent.name,
        'ParentPhone': student.parent.phone
    }

    # Load the Word document template
    doc = DocxTemplate(file_path)
    
    # Render the template with the replacement context
    doc.render(replacement)

    # Save the filled document
    doc.save(output_path)

    # Open the generated document (works on Windows)
    if os.name == 'nt':
        os.startfile(output_path)  # For Windows
