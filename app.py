
import streamlit as st

from src.dictionary import search_word


st.set_page_config(
    page_title="Japanese Word Choice Lab",
    page_icon="📚",
    layout="wide"
)


st.title("ことばの使い分けラボ")
st.subheader("Japanese Word Choice Lab")

st.write("Search for a Japanese word to explore its meaning and usage.")


# Search input
search_input = st.text_input("Japanese Word")


# Search button
if st.button("Search"):

    if search_input.strip() == "":
        st.warning("Please enter a word.")

    else:
        results = search_word(search_input.strip())

        if len(results) > 0:

            for result in results:

                st.divider()

                st.header(result["word"])
                st.write("Reading:", result["reading"])

                st.write("Part of Speech:")
                st.write(", ".join(result["part_of_speech"]))

                st.write("Definitions:")
                for definition in result["definitions"]:
                    st.write("- ", definition)

        else:
            st.error("Word not found.")

