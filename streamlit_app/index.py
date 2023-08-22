import os, streamlit as st
import logging
from fpdf import FPDF


# Uncomment to specify your OpenAI API key here (local testing only, not in production!), or add corresponding environment variable (recommended)
# os.environ['OPENAI_API_KEY']= ""

from llama_index import StorageContext, load_index_from_storage

logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Define a simple Streamlit app
st.title("Boston.gov RFP generator")
st.markdown(
    "This app generates RFPs using OpenAI's [GPTs](https://beta.openai.com/docs/models/overview) for texts."
)
topic = st.text_input(label="What is the topic of the RFP?", placeholder="Bicycle Repair and Maintenance Employee Benefit")
organization = st.text_input(
    label="What is the organization you are writing the RFP for?",
    placeholder="City of San Francisco",
)

if "statement_of_need" not in st.session_state:
    st.session_state.statement_of_need = ""
if "quick_description" not in st.session_state:
    st.session_state.quick_description = ""
if "expectations" not in st.session_state:
    st.session_state.expectations = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

def generate_text(query):
    # load the index from vector_store.json
    storage_context = StorageContext.from_defaults(persist_dir=".")
    index = load_index_from_storage(storage_context)
    # create a query engine to ask question
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    return response.response


# If the 'Submit' button is clicked
if st.button("Generate Statement of Need"):
    if not topic.strip():
        st.error(f"Please provide the RFP topic.")
    elif not organization.strip():
        st.error(f"Please provide the organization.")
    else:
        try:
            query = f"""
            Write a statement of need for a RFP for {topic} for {organization}
            in 1-3 sentences.
            
            End with the following sentence: We look forward to receiving your proposal.
            """
            response = generate_text(query)
            st.session_state.statement_of_need = response
        except Exception as e:
            st.error(f"An error occurred: {e}")


if st.session_state.statement_of_need:
    st.markdown("""---""")
    statement_of_need = st.text_area(label="Statement of Need", value=st.session_state.statement_of_need, height=100)

    if st.button("Generate Quick Description"):
        if not statement_of_need.strip():
            st.error(f"Please generate Statement of Need first.")
        else:
            try:
                query = f"""
                Write a quick description for the scope of work section for a RFP for {topic} for {organization} in one sentence.

                Previous response: {statement_of_need}
                """
                response = generate_text(query)
                st.session_state.quick_description = response
                logging.info(
                    f"Quick description: {st.session_state.quick_description}"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")


if st.session_state.quick_description:
    st.markdown("""---""")
    quick_description = st.text_area(label="Quick Description", value=st.session_state.quick_description, height=100)

    if st.button("Generate Expectations"):
        if not quick_description.strip():
            st.error(f"Please generate Quick Description first.")
        else:
            try:
                query = f"""
                Write the expectations the scope of work section for a RFP for {topic} for {organization} in multiple paragraphs with titles: Materials/Resources, Services, Labor, Quality criteria for this component

                Response so far:
                {statement_of_need}
                {quick_description}
                """
                response = generate_text(query)
                st.session_state.expectations = response
                logging.info(
                    f"Expectations: {st.session_state.expectations}"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")


if st.session_state.expectations:
    st.markdown("""---""")
    expectations = st.text_area(label="Expectations", value=st.session_state.expectations, height=500)

    if st.button("Generate Summary"):
        if not expectations.strip():
            st.error(f"Please generate Expectations first.")
        else:
            try:
                query = f"""
                Write a project summary for a RFP for {topic} for {organization} in 1-3 sentences.

                Response so far:
                {statement_of_need}
                {quick_description}
                {expectations}
                """
                response = generate_text(query)
                st.session_state.summary = response
                logging.info(
                    f"Summary: {st.session_state.summary}"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state.summary:
    st.markdown("""---""")
    summary = st.text_area(label="Summary", value=st.session_state.summary, height=200)

    if st.button("Put it all together!"):
        if not summary.strip():
            st.error("Please generate Summary first.")
        else:
            st.header(topic)
            st.caption(organization)

            st.subheader("Statement of Need")
            st.markdown(statement_of_need)

            st.subheader("Quick Description")
            st.markdown(quick_description)

            st.subheader("Expectations")
            st.markdown(expectations)

            st.subheader("Summary")
            st.markdown(summary)

            pdf = FPDF('P', 'mm', 'A4')
            pdf.add_page()

            pdf.set_font(family='Arial', style='B', size=18)
            pdf.multi_cell(0, 5, topic, 0, 1)

            pdf.set_font(family='Arial', size=14)
            pdf.multi_cell(0, 5, organization, 0, 1)
            pdf.ln()

            pdf.set_font(family='Arial', style='B', size=16)
            pdf.multi_cell(0, 5, 'Statement of Need', 0, 1)

            pdf.set_font(family='Arial', size=12)
            pdf.multi_cell(0, 5, statement_of_need, 0, 1)
            pdf.ln()

            pdf.set_font(family='Arial', style='B', size=16)
            pdf.multi_cell(0, 5, 'Quick Description', 0, 1)

            pdf.set_font(family='Arial', size=12)
            pdf.multi_cell(0, 5, quick_description, 0, 1)
            pdf.ln()

            pdf.set_font(family='Arial', style='B', size=16)
            pdf.multi_cell(0, 5, 'Expectations', 0, 1)

            pdf.set_font(family='Arial', size=12)
            pdf.multi_cell(0, 5, expectations, 0, 1)
            pdf.ln()

            pdf.set_font(family='Arial', style='B', size=16)
            pdf.multi_cell(0, 5, 'Summary', 0, 1)

            pdf.set_font(family='Arial', size=12)
            pdf.multi_cell(0, 5, summary, 0, 1)
            pdf.ln()

            pdf.output('rfp.pdf', 'F')

            with open("rfp.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()


            st.download_button(
                'Download PDF',
                data=PDFbyte,
                file_name='rfp.pdf',
                mime='application/octet-stream'
            )
