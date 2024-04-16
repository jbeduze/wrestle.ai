import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = 'your-openai-api-key'

def extract_fields_from_document(document):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Extract the following fields from the credit application document:\n{document}\n\nFields:\n1. Full name\n2. Social Security Number\n3. Address\n4. Phone number\n5. Email address\n6. Current employer\n7. Position\n8. Monthly income\n9. Purpose of the loan\n10. Loan amount\n",
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def main():
    st.title("Credit Application Analysis")
    uploaded_file = st.file_uploader("Upload a credit application", type=['pdf', 'txt'])

    if uploaded_file is not None:
        # Assuming the file is in plain text format
        document_text = uploaded_file.getvalue().decode("utf-8")

        if st.button("Analyze"):
            with st.spinner('Analyzing...'):
                result = extract_fields_from_document(document_text)
                st.subheader("Extracted Information")
                st.write(result)

if __name__ == "__main__":
    main()