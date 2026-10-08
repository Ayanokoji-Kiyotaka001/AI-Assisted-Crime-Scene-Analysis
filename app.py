
import streamlit as st
import os

from google import genai


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CrimeLens AI",
    page_icon="🔎",
    layout="wide"
)


# =====================================================
# GEMINI
# =====================================================

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:

    st.error(
        "Gemini API key not found."
    )

    st.stop()


client = genai.Client(
    api_key=api_key
)


# =====================================================
# SESSION STORAGE
# =====================================================

if "analysis" not in st.session_state:

    st.session_state.analysis = None


if "report" not in st.session_state:

    st.session_state.report = None


# =====================================================
# WEBSITE HEADER
# =====================================================

st.title("🔎 CrimeLens AI")

st.subheader(
    "AI-Assisted Crime Scene Analysis"
)

st.write(
    "Upload forensic evidence and use AI to "
    "generate structured investigative observations."
)

st.warning(
    "⚠️ AI-generated results are assistance only. "
    "They must be verified by qualified forensic personnel."
)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📁 Case Information")


case_id = st.sidebar.text_input(
    "Case ID",
    placeholder="Example: CASE-001"
)


investigator = st.sidebar.text_input(
    "Investigator Name"
)


location = st.sidebar.text_input(
    "Crime Scene Location"
)


description = st.sidebar.text_area(
    "Case Description"
)


# =====================================================
# MAIN TABS
# =====================================================

upload_tab, analysis_tab, report_tab = st.tabs(
    [
        "📤 Evidence Upload",
        "🔬 Analysis",
        "📄 Crime Report"
    ]
)


# =====================================================
# EVIDENCE UPLOAD
# =====================================================

with upload_tab:

    st.header(
        "📤 Upload Evidence"
    )

    uploaded_file = st.file_uploader(
        "Select an evidence file",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "mp4",
            "mov",
            "avi",
            "pdf",
            "txt"
        ]
    )


    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )


        # IMAGE PREVIEW

        if uploaded_file.type.startswith("image"):

            st.image(
                uploaded_file,
                caption="Uploaded Evidence",
                width=600
            )


        # VIDEO PREVIEW

        elif uploaded_file.type.startswith("video"):

            st.video(
                uploaded_file
            )


        # DOCUMENT

        else:

            st.info(
                "Document uploaded successfully."
            )


# =====================================================
# ANALYZE EVIDENCE
# =====================================================

with analysis_tab:

    st.header(
        "🔬 Evidence Analysis"
    )


    if not uploaded_file:

        st.info(
            "Upload evidence first."
        )


    else:

        if st.button(
            "🚀 ANALYZE EVIDENCE",
            type="primary"
        ):

            with st.spinner(
                "AI is analyzing the evidence..."
            ):

                try:

                    # Upload file to Gemini

                    uploaded = client.files.upload(
                        file=uploaded_file
                    )


                    # Analysis instructions

                    prompt = """

You are an AI assistant supporting
forensic investigators.

Analyze the uploaded evidence carefully.

Provide a structured forensic observation.

Use the following sections:

1. EVIDENCE DESCRIPTION

Describe what is visible or contained
in the uploaded evidence.

2. OBSERVATIONS

List important observable details.

3. POTENTIAL EVIDENCE

Identify objects, patterns,
materials or information that
may have forensic relevance.

4. POSSIBLE FORENSIC SIGNIFICANCE

Explain why the observed material
may be relevant to an investigation.

5. INVESTIGATIVE LEADS

Mention possible areas that an
investigator may examine further.

6. LIMITATIONS

Explain what cannot be determined
from the uploaded evidence.

IMPORTANT:

Do not invent facts.

Do not identify a person with certainty.

Do not determine guilt or innocence.

Clearly distinguish observations
from interpretation.

Use terms such as "possible",
"appears", or "may indicate"
where appropriate.

The result is AI-assisted and must
be verified by qualified forensic
personnel.

"""


                    # Gemini analysis

                    response = client.models.generate_content(

                        model="gemini-2.5-flash",

                        contents=[
                            uploaded,
                            prompt
                        ]

                    )


                    # Store result

                    st.session_state.analysis = response.text


                    st.success(
                        "✅ Evidence analysis completed."
                    )


                except Exception as e:

                    st.error(
                        f"Analysis failed: {e}"
                    )


    # SHOW RESULT

    if st.session_state.analysis:

        st.divider()

        st.subheader(
            "🔬 AI Analysis Result"
        )

        st.markdown(
            st.session_state.analysis
        )


# =====================================================
# CRIME REPORT
# =====================================================

with report_tab:

    st.header(
        "📄 Crime Report Generation"
    )


    if not st.session_state.analysis:

        st.info(
            "Analyze evidence first."
        )


    else:

        st.success(
            "Evidence analysis is ready."
        )


        if st.button(
            "📄 GENERATE CRIME REPORT",
            type="primary"
        ):

            with st.spinner(
                "Generating crime report..."
            ):


                report_prompt = f"""

Create a structured
AI-assisted crime scene analysis report.

CASE INFORMATION

Case ID:
{case_id}

Investigator:
{investigator}

Crime Scene Location:
{location}

Case Description:
{description}


EVIDENCE ANALYSIS

{st.session_state.analysis}


Prepare the report using these sections:

# CRIMELENS AI
## Crime Scene Analysis Report

### 1. Case Information

### 2. Case Description

### 3. Evidence Examined

### 4. Scene Observations

### 5. Potential Evidence

### 6. Forensic Significance

### 7. Investigative Leads

### 8. Limitations

### 9. Verification Requirements

### 10. Conclusion


IMPORTANT:

Do not invent information.

Do not make definitive suspect
identification.

Do not determine guilt or innocence.

Clearly state that the report is
AI-assisted and requires verification
by qualified forensic personnel.

"""


                response = client.models.generate_content(

                    model="gemini-2.5-flash",

                    contents=report_prompt

                )


                st.session_state.report = response.text


        # DISPLAY REPORT

        if st.session_state.report:

            st.divider()

            st.subheader(
                "📄 Generated Crime Report"
            )

            st.markdown(
                st.session_state.report
            )


            # DOWNLOAD

            st.download_button(

                label="⬇️ DOWNLOAD REPORT",

                data=st.session_state.report,

                file_name="CrimeLens_Crime_Report.md",

                mime="text/markdown"

            )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "CrimeLens AI | AI-Assisted Forensic Evidence Processing"
)
