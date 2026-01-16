# import os
# import streamlit as st
#
# from llm.gemini_client import GeminiLLM
# from agents.question_agent import QuestionGenerationAgent
#
#
# def run_app():
#     st.set_page_config(
#         page_title="Narrative Constraint Question Generator",
#         layout="wide",
#     )
#
#     # ---------------- Sidebar ----------------
#     st.sidebar.title("🔑 Configuration")
#
#     api_key = st.sidebar.text_input(
#         "Google Gemini API Key",
#         type="password",
#         help="Your API key is used only for this session.",
#     )
#
#     temperature = st.sidebar.slider(
#         "Temperature",
#         min_value=0.0,
#         max_value=1.0,
#         value=0.5,
#         step=0.05,
#     )
#
#     st.sidebar.markdown("---")
#     st.sidebar.caption("Track-1 | IIT-KGP Hackathon")
#
#     # ---------------- Main UI ----------------
#     st.title("📚 Narrative Constraint Question Generator")
#
#     st.markdown(
#         """
#         Generate **binary factual questions** that must be true in the novel
#         for a hypothetical character backstory to be globally consistent.
#         """
#     )
#
#     character = st.text_input(
#         "Character Name",
#         placeholder="e.g. Elizabeth Bennet",
#     )
#
#     backstory = st.text_area(
#         "Hypothetical Backstory",
#         height=250,
#         placeholder="Paste the hypothetical backstory here...",
#     )
#
#     generate_btn = st.button("🚀 Generate Questions")
#
#     # ---------------- Logic ----------------
#     if generate_btn:
#         if not api_key:
#             st.error("Please enter your Google API key in the sidebar.")
#             return
#
#         if not character or not backstory:
#             st.error("Please provide both character name and backstory.")
#             return
#
#         # Set env var for this runtime
#         os.environ["GOOGLE_API_KEY"] = api_key
#
#         with st.spinner("Generating constraint questions..."):
#             #-----------------------------Question Generator ----------------
#             gemini = GeminiLLM(
#                 api_key=api_key,
#                 temperature=temperature,
#             )
#
#             question_agent = QuestionGenerationAgent(gemini)
#
#             result = question_agent.run(
#                 character=character,
#                 content=backstory,
#             )
#
#         st.subheader("Generated Questions")
#         #----------------------------------------------------------------------
#         st.code(result, language="json")


import os
import json
import streamlit as st

from llm.gemini_client import GeminiLLM
from agents.question_agent import QuestionGenerationAgent


from rag_pipeline.retrieval.pipeline import NovelQAPipeline


def run_app():
    st.set_page_config(
        page_title="Narrative Constraint Question Generator",
        layout="wide",
    )

    # ---------------- Sidebar ----------------
    st.sidebar.title("🔑 Configuration")

    api_key = st.sidebar.text_input(
        "Google Gemini API Key",
        type="password",
        help="Your API key is used only for this session.",
    )

    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
    )

    novel_id = st.sidebar.text_input(
        "Novel ID",
        value="hp_7",
        help="Used for retrieval filtering",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Track-1 | IIT-KGP Hackathon")

    # ---------------- Main UI ----------------
    st.title("📚 Narrative Constraint Question Generator")

    st.markdown(
        """
        Generate **binary factual questions** that must be true in the novel
        for a hypothetical character backstory to be globally consistent.
        """
    )

    character = st.text_input(
        "Character Name",
        placeholder="e.g. Elizabeth Bennet",
    )

    backstory = st.text_area(
        "Hypothetical Backstory",
        height=250,
        placeholder="Paste the hypothetical backstory here...",
    )

    col1, col2 = st.columns(2)

    generate_btn = col1.button("🚀 Generate Questions")
    retrieve_btn = col2.button("📖 Retrieve & Verify")

    # ---------------- State ----------------
    if "questions" not in st.session_state:
        st.session_state.questions = None

    # ---------------- Generate Questions ----------------
    if generate_btn:
        if not api_key:
            st.error("Please enter your Google API key in the sidebar.")
            return

        if not character or not backstory:
            st.error("Please provide both character name and backstory.")
            return

        os.environ["GOOGLE_API_KEY"] = api_key

        with st.spinner("Generating constraint questions..."):
            gemini = GeminiLLM(
                api_key=api_key,
                temperature=temperature,
            )

            question_agent = QuestionGenerationAgent(gemini)

            result = question_agent.run(
                character=character,
                content=backstory,
            )

            st.session_state.questions = json.loads(result)

        st.subheader("Generated Questions")
        st.code(result, language="json")

    # ---------------- Retrieve & Verify ----------------
    if retrieve_btn:
        if not st.session_state.questions:
            st.error("Generate questions first.")
            return

        with (st.spinner("Retrieving evidence from novel...")):
            # pipeline = NovelQAPipeline(
            #     chunks_path="chunks/novels.chunks.json"
            # )

            results = []
            for q in st.session_state.questions:
                qa_result =""
                # pipeline.run(
                #     novel_id=novel_id,
                #     character_id=character,
                #     question=q,
                # )
                results.append(qa_result)

        st.subheader("Retrieval Results")
        for r in results:
            with st.expander(r["question"]):
                st.json(r)


