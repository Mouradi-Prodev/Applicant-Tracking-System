from io import BytesIO
import streamlit as st
import docx2txt as doc
import PyPDF2
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def draw_percentage_circle(percentage):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie([percentage, 100 - percentage], labels=[f'{percentage}%', ''], colors=['#1f78b4', '#d9d9d9'], startangle=90, counterclock=False)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig

def Validate(Resume,job_description):
    if Resume is not None and len(job_description)>=2:
        return True
    return False
def validate_upload(Resume):
    if Resume is not None:
        # Use the content of the uploaded file
        content = Resume
        st.write(content)  # Display the content for validation
    else:
        st.write("No file uploaded.")

def CheckFileType(Resume):
    
    file_type = Resume.type
    if "pdf" in file_type.lower():
        return "pdf"
    elif "docx" in file_type.lower() or "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in file_type.lower():
        return "docx"
    return file_type

def Process(res,job_description):
    text = [res , job_description]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    match = cosine_similarity(count_matrix)[0][1]
    match = match*100
    match = round(match,2)
    st.divider()
    st.markdown('**Matching Percentage : **'+str(match)+'%')
    
    col1, col2 = st.columns([2, 2])
    with col1:
        st.pyplot(draw_percentage_circle(match))
    with col2:
        st.text(res)

def extract_text_from_pdf(resume):
    text = ""
    pdf_reader = PyPDF2.PdfReader(resume)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text
def CheckMatch(Resume,job_description):
    
    with st.spinner('Wait for it...'):
        file_type = CheckFileType(Resume)
        if(file_type == "pdf"):
            res = extract_text_from_pdf(Resume)
            Process(res,job_description)
        elif(file_type == "docx"):
            
            res = doc.process(Resume)
            Process(res,job_description)
        else:    
            st.write("Unsupported file type.")
        
        


def main(): 
    st.set_page_config(
        page_title="Applicant Tracking System",
        
        layout="wide",
        
    )

    container = st.container()
    with container:
        st.title("Applicant tracking system")
       

    col1, col2 = st.columns([2,3])

    with col1:
        Resume = st.file_uploader("Upload your Resume: ",type=["pdf","docx"],key="Resume",accept_multiple_files=False)
        
       


    with col2:
        job_description = st.text_area("Job description",key="job_description",height=10,placeholder="Write or Paste your Job description")
    
    with st.container():
        validate_button = st.button("Validate")

        if validate_button:
            if Validate(Resume,job_description):
                st.toast(':green[Successfully validated]',icon="✅")
                CheckMatch(Resume,job_description)
            else:
                st.toast(":red[Error, fill job description and resume]")
               
        
       
    # UploadedFile(file_id='c29962b9-322d-46ee-ba7e-3b6dc906bca1',
    #               name='Mouradi_CV Pro.pdf', 
    #               type='application/pdf', 
    #               size=173373, 
    #               _file_urls=file_id: "c29962b9-322d-46ee-ba7e-3b6dc906bca1" 
    #               upload_url: "/_stcore/upload_file/7ff36606-a314-4995-885c-3b20c374f549/c29962b9-322d-46ee-ba7e-3b6dc906bca1" 
    #               delete_url: "/_stcore/upload_file/7ff36606-a314-4995-885c-3b20c374f549/c29962b9-322d-46ee-ba7e-3b6dc906bca1" )
   

if __name__ == "__main__":
    main()