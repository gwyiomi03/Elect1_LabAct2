import subprocess
import sys

import streamlit as st
import streamlit.components.v1 as components


# PAGE SETUP
st.set_page_config(
    page_title="Adaptive Coding Environment",
    layout="wide"
)

st.title("Adaptive Python Coding Environment")

st.write(
    "Simple IDE prototype "
    "according to a user model."
)


# USER INFORMATION / ONBOARDING
st.sidebar.header("User Information")


years = st.sidebar.number_input(
    "Years of programming experience",
    min_value=0,
    max_value=60,
    value=2
)


ai_select = st.sidebar.selectbox(
    "Do you currently use AI tools for programming?",
    [
        "Yes",
        "No, but I plan to soon",
        "No, and I don't plan to"
    ]
)


ai_sentiment = st.sidebar.selectbox(
    "How do you feel about using AI tools?",
    [
        "Very favorable",
        "Favorable",
        "Indifferent",
        "Unsure",
        "Unfavorable",
        "Very unfavorable"
    ]
)


available_tasks = [
    "Debugging and getting help",
    "Writing code",
    "Testing code",
    "Learning about a codebase",
    "Documenting code"
]


if ai_select == "Yes":

    ai_tasks = st.sidebar.multiselect(
        "What do you use AI for?",
        available_tasks
    )

else:

    ai_tasks = []


# CREATE USER MODEL
def get_experience_group(years):

    if years <= 2:
        return "Early Experience"

    if years <= 5:
        return "Mid Experience"

    return "Long Experience"


def get_ai_preference(sentiment):

    if sentiment in [
        "Very favorable",
        "Favorable"
    ]:
        return "High"

    if sentiment in [
        "Indifferent",
        "Unsure"
    ]:
        return "Moderate"

    return "Low"


user_model = {

    "experience":
        get_experience_group(years),

    "ai_usage":
        ai_select,

    "ai_preference":
        get_ai_preference(ai_sentiment),

    "ai_debugging":
        "Debugging and getting help"
        in ai_tasks,

    "ai_writing":
        "Writing code"
        in ai_tasks,

    "ai_testing":
        "Testing code"
        in ai_tasks,

    "ai_learning":
        "Learning about a codebase"
        in ai_tasks,

    "ai_documentation":
        "Documenting code"
        in ai_tasks
}


# SHOW USER MODEL
with st.sidebar.expander(
    "Current User Model",
    expanded=True
):

    st.json(user_model)


# CODE EDITOR
st.subheader("Python Code")

default_code = """x = 10

if x > 5:
    print("Pasar Cutie")
"""

code = st.text_area(
    "Enter Python code",
    value=default_code,
    height=300,
    key="python_code_editor"
)

components.html(
    """
    <script>
    const doc = window.parent.document;

    function addGutter() {
        const textareas = doc.querySelectorAll('textarea[aria-label="Enter Python code"]');
        textareas.forEach(function (ta) {
            if (ta.dataset.gutterAdded) return;
            ta.dataset.gutterAdded = "true";

            const style = getComputedStyle(ta);

            const wrapper = doc.createElement('div');
            wrapper.style.position = 'relative';
            ta.parentNode.insertBefore(wrapper, ta);
            wrapper.appendChild(ta);

            const gutter = doc.createElement('div');
            gutter.style.position = 'absolute';
            gutter.style.left = '0';
            gutter.style.top = '0';
            gutter.style.bottom = '0';
            gutter.style.width = '38px';
            gutter.style.overflow = 'hidden';
            gutter.style.textAlign = 'right';
            gutter.style.paddingRight = '6px';
            gutter.style.paddingTop = style.paddingTop;
            gutter.style.fontFamily = style.fontFamily;
            gutter.style.fontSize = style.fontSize;
            gutter.style.lineHeight = style.lineHeight;
            gutter.style.color = '#8a8a8a';
            gutter.style.background = 'rgba(120,120,120,0.08)';
            gutter.style.borderRight = '1px solid rgba(120,120,120,0.25)';
            gutter.style.userSelect = 'none';
            gutter.style.pointerEvents = 'none';
            wrapper.insertBefore(gutter, ta);

            ta.style.paddingLeft = '46px';
            ta.style.boxSizing = 'border-box';

            function updateNumbers() {
                const lineCount = ta.value.split('\\n').length;
                let html = '';
                for (let i = 1; i <= lineCount; i++) {
                    html += i + '<br>';
                }
                gutter.innerHTML = html;
                gutter.scrollTop = ta.scrollTop;
            }

            ta.addEventListener('input', updateNumbers);
            ta.addEventListener('scroll', function () {
                gutter.scrollTop = ta.scrollTop;
            });

            updateNumbers();
        });
    }

    setInterval(addGutter, 300);
    </script>
    """,
    height=0,
)


# SESSION STATE
if "stdout" not in st.session_state:
    st.session_state.stdout = ""

if "stderr" not in st.session_state:
    st.session_state.stderr = ""


# RUN CODE
def run_python_code(source):

    try:

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                source
            ],
            capture_output=True,
            text=True,
            timeout=3
        )

        return (
            result.stdout,
            result.stderr
        )

    except subprocess.TimeoutExpired:

        return (
            "",
            "Execution stopped: "
            "program took too long."
        )


if st.button(
    "Run Code",
    type="primary"
):

    stdout, stderr = run_python_code(code)

    st.session_state.stdout = stdout
    st.session_state.stderr = stderr


# OUTPUT
st.subheader("Output / Terminal")


if st.session_state.stderr:

    st.error("The program contains an error.")

    st.code(
        st.session_state.stderr,
        language="text"
    )


elif st.session_state.stdout:

    st.code(
        st.session_state.stdout,
        language="text"
    )


else:

    st.write(
        "Run the code to see its output."
    )


# SIMULATED AI DEBUGGING
def explain_error(error):

    if "expected ':'" in error:

        return (
            "The statement is missing a colon (:). "
            "Python requires a colon after statements "
            "such as if, for, while, def, and class."
        )

    if "NameError" in error:

        return (
            "Python cannot find the variable or function "
            "name being used. Check whether it was "
            "defined earlier and whether the spelling "
            "is correct."
        )

    if "IndentationError" in error:

        return (
            "Python detected incorrect indentation. "
            "Check that the statements inside the block "
            "have consistent indentation."
        )

    if "TypeError" in error:

        return (
            "The operation was applied to incompatible "
            "types. Check the types of the values used "
            "in the reported line."
        )

    return (
        "Review the final lines of the error message. "
        "They normally identify the error type and "
        "the line where Python encountered the problem."
    )


# ADAPTIVE AI PANEL
show_ai_panel = (
    ai_select == "Yes"
    and
    user_model["ai_preference"] != "Low"
)


if show_ai_panel:

    st.divider()

    st.subheader("AI Assistance")

    if user_model["ai_debugging"]:

        if st.session_state.stderr:

            if st.button(
                "AI: Explain Error"
            ):

                st.info(
                    explain_error(
                        st.session_state.stderr
                    )
                )


    if user_model["ai_writing"]:

        if st.button(
            "AI: Suggest Code"
        ):

            st.info(
                "Simulated AI feature: "
                "code-generation assistance "
                "would appear here."
            )


    if user_model["ai_testing"]:

        if st.button(
            "AI: Suggest Tests"
        ):

            st.info(
                "Simulated AI feature: "
                "test suggestions would appear here."
            )


    if user_model["ai_learning"]:

        if st.button(
            "AI: Explain Code"
        ):

            st.info(
                "Simulated AI feature: "
                "a natural-language explanation "
                "of the code would appear here."
            )


    if user_model["ai_documentation"]:

        if st.button(
            "AI: Generate Documentation"
        ):

            st.info(
                "Simulated AI feature: "
                "documentation assistance "
                "would appear here."
            )


elif ai_select == "Yes":

    st.info(
        "AI assistance is available but minimized "
        "because this user model has a low "
        "AI preference."
    )