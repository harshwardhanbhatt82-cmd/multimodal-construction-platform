
import json
from datetime import datetime

import streamlit as st
from PIL import Image

# Optional Gemini integration. The application still works without it.
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Multimodal Construction Intelligence",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Multimodal Construction Intelligence Platform")
st.caption(
    "AI-assisted construction safety, preliminary crack assessment, "
    "project planning, valuation, and site guidance."
)


# ---------------------------------------------------------
# 2. SESSION STATE
# ---------------------------------------------------------

for key in (
    "safety_report",
    "crack_report",
    "planning_report",
    "site_answer",
):
    if key not in st.session_state:
        st.session_state[key] = None


# ---------------------------------------------------------
# 3. SIDEBAR CONFIGURATION
# ---------------------------------------------------------

with st.sidebar:
    st.header("Configuration")

    api_key = st.text_input(
        "Gemini API key (optional)",
        type="password",
        help="Leave empty to use offline demonstration mode.",
    )

    model_name = st.selectbox(
        "Gemini model",
        [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ],
    )

    if api_key:
        if GEMINI_AVAILABLE:
            st.success("Gemini configured for API requests")
        else:
            st.warning("Gemini SDK is not installed")
    else:
        st.info("Offline demonstration mode")

    st.divider()

    st.markdown("### About this project")
    st.caption("College capstone prototype")
    st.caption("Built with Python and Streamlit")
    st.caption("Optional multimodal Gemini integration")

    st.warning(
        "Not a certified safety inspection, structural diagnosis, "
        "or professional property valuation."
    )


# ---------------------------------------------------------
# 4. AI AND OFFLINE RESPONSE ENGINE
# ---------------------------------------------------------

def offline_response(category: str, question: str = "") -> str:
    """Return explicitly labelled demonstration content."""

    if category == "safety":
        return """
## Demonstration Safety Report

**Mode:** Offline demonstration. No AI image analysis was performed.

### PPE observations
- Helmet use: Not assessed.
- High-visibility clothing: Not assessed.
- Safety footwear: Not assessed.
- Eye and hearing protection: Not assessed.

### Potential site hazards
No image-based hazard findings are available in offline mode.

### Recommended inspection checklist
1. Verify required PPE before workers enter the site.
2. Check scaffolding, ladders, and edge protection.
3. Inspect electrical equipment and cable routing.
4. Keep walkways clear of debris and materials.
5. Confirm that emergency access routes are unobstructed.
6. Record findings with the site safety officer.

### Limitations
This sample does not describe the uploaded image. A qualified safety
professional must assess actual site conditions.
"""

    if category == "crack":
        return """
## Demonstration Crack Assessment

**Mode:** Offline demonstration. No AI image analysis was performed.

### Image assessment
- Crack location: Not assessed.
- Pattern and direction: Not assessed.
- Crack width and depth: Not measured.
- Material condition: Not assessed.
- Structural severity: Cannot be determined.

### Recommended next steps
1. Record the location and date of the observation.
2. Photograph the area with a scale for reference.
3. Document any changes over time.
4. Look for associated displacement, water ingress, or other damage.
5. Arrange an in-person assessment by a qualified structural engineer
   when appropriate.

**Important:** An image or this sample report cannot establish whether
a structure is safe to occupy.
"""

    if category == "planning":
        return f"""
## Construction Planning Guidance

**Mode:** Offline rule-based demonstration. No AI API was called.

### Budget categories to consider
- Site preparation and excavation
- Foundation and structural work
- Masonry, roofing, and waterproofing
- Electrical and plumbing installations
- Doors, windows, flooring, and finishes
- Labour, equipment, and transportation
- Professional fees, permits, and applicable taxes
- Contingency for unexpected expenses

### Planning recommendations
1. Break the project into work packages.
2. Estimate quantities and obtain local supplier quotations.
3. Create a milestone-based construction schedule.
4. Track actual spending against the approved budget.
5. Document changes, risks, and approvals.

### Your question
{question if question else "No question supplied."}

Actual costs depend on location, design, specifications, and market
conditions. Verify estimates with local professionals.
"""

    return f"""
## Construction Site Assistant

**Mode:** Offline rule-based demonstration. No AI API was called.

### Your question
{question if question else "No question supplied."}

### General site coordination checklist
1. Review the approved work schedule.
2. Confirm worker assignments and required PPE.
3. Check material availability and equipment condition.
4. Record completed work, delays, and safety observations.
5. Confirm inspection requirements and outstanding tasks.
6. Follow official weather warnings and the site's safety plan.

### Weather limitations
This application has not retrieved live weather information.
Check an official local forecast before making weather-dependent
site decisions.

For engineering, structural, or safety-critical decisions, consult
the appropriately qualified professional.
"""


def ask_ai(
    prompt: str,
    category: str,
    image: Image.Image | None = None,
) -> tuple[str, str]:
    """
    Return a response and its source label.

    If no API key is supplied, use offline demo content.
    API errors are reported rather than silently presented as AI results.
    """

    if not api_key:
        return offline_response(category, prompt), "Offline demo"

    if not GEMINI_AVAILABLE:
        return (
            "The Gemini SDK is unavailable. Install the requirements "
            "and restart the application, or clear the API key to use "
            "offline demonstration mode."
        ), "Configuration error"

    try:
        client = genai.Client(api_key=api_key)

        contents = [prompt]

        if image is not None:
            contents.append(image)

        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.2,
            ),
        )

        result = response.text

        if not result:
            return "The API returned no text. Please try again.", "API response"

        return result, "Gemini API"

    except Exception as exc:
        return (
            f"Gemini request failed ({type(exc).__name__}). "
            "Check your API access, model availability, and configuration. "
            "Clear the API key to return to offline demo mode."
        ), "API error"


# ---------------------------------------------------------
# 5. SHARED REPORT DISPLAY AND DOWNLOAD
# ---------------------------------------------------------

def show_report(
    report: str,
    filename: str,
    source: str,
) -> None:
    """Display and provide a downloadable report."""

    if source == "Gemini API":
        st.success("Response generated using the Gemini API.")
    elif source == "Offline demo":
        st.info(
            "Offline demonstration report. It does not represent "
            "actual AI analysis of the uploaded image."
        )
    else:
        st.warning(f"Response status: {source}")

    st.markdown(report)

    st.download_button(
        "Download report",
        data=report,
        file_name=filename,
        mime="text/markdown",
        key=f"download_{filename}",
    )


def load_image(uploaded_file) -> Image.Image | None:
    """Safely load a supported image."""

    if uploaded_file is None:
        return None

    try:
        image = Image.open(uploaded_file)
        image.verify()

        uploaded_file.seek(0)

        return Image.open(uploaded_file).convert("RGB")

    except Exception:
        st.error("Unable to read this image. Please upload a valid JPG or PNG.")
        return None


# ---------------------------------------------------------
# 6. APPLICATION TABS
# ---------------------------------------------------------

safety_tab, crack_tab, planning_tab, assistant_tab = st.tabs(
    [
        "🦺 Site Safety & PPE",
        "🧱 Crack Assessment",
        "📊 Planning & Valuation",
        "💬 Site Assistant",
    ]
)


# ---------------------------------------------------------
# 7. SITE SAFETY AND PPE
# ---------------------------------------------------------

with safety_tab:
    st.header("Construction Site Safety")

    st.write(
        "Upload a construction-site photograph for a safety report. "
        "Without an API key, the application displays a sample report "
        "rather than analyzing the image."
    )

    safety_file = st.file_uploader(
        "Upload a construction-site image",
        type=["jpg", "jpeg", "png"],
        key="safety_upload",
    )

    safety_image = load_image(safety_file)

    if safety_image is not None:
        st.image(
            safety_image,
            caption="Uploaded construction-site image",
            use_container_width=True,
        )

        if st.button("Analyze site safety", key="run_safety"):
            prompt = """
Review this construction-site image for visible safety concerns.

Structure the response under:
1. Visible observations
2. PPE observations, only where assessable
3. Potential visible hazards
4. Recommended checks and corrective actions
5. Limitations and matters requiring professional inspection

Distinguish observations from assumptions. Do not claim that hidden
hazards are absent. State when something cannot be seen clearly.
This is preliminary AI assistance, not a formal safety inspection.
"""

            with st.spinner("Preparing safety report..."):
                report, source = ask_ai(
                    prompt=prompt,
                    category="safety",
                    image=safety_image,
                )

            st.session_state["safety_report"] = {
                "report": report,
                "source": source,
            }

    saved = st.session_state["safety_report"]

    if saved:
        show_report(
            saved["report"],
            "site_safety_report.md",
            saved["source"],
        )


# ---------------------------------------------------------
# 8. PRELIMINARY CRACK ASSESSMENT
# ---------------------------------------------------------

with crack_tab:
    st.header("Preliminary Crack Assessment")

    st.warning(
        "This tool cannot determine structural safety or replace "
        "an in-person assessment by a qualified structural engineer."
    )

    crack_file = st.file_uploader(
        "Upload a wall or crack image",
        type=["jpg", "jpeg", "png"],
        key="crack_upload",
    )

    crack_image = load_image(crack_file)

    if crack_image is not None:
        st.image(
            crack_image,
            caption="Uploaded image",
            use_container_width=True,
        )

        if st.button("Assess visible crack", key="run_crack"):
            prompt = """
Describe only features visible in this image of a possible crack.

Include:
1. Visible location and pattern
2. Direction and apparent shape
3. Image limitations, including lack of scale or depth information
4. Information a structural engineer would need
5. Appropriate documentation and professional follow-up

Do not infer exact crack width without a scale. Do not assign a
definitive structural severity grade or declare a structure safe
or unsafe based only on this image.
"""

            with st.spinner("Preparing preliminary assessment..."):
                report, source = ask_ai(
                    prompt=prompt,
                    category="crack",
                    image=crack_image,
                )

            st.session_state["crack_report"] = {
                "report": report,
                "source": source,
            }

    saved = st.session_state["crack_report"]

    if saved:
        show_report(
            saved["report"],
            "crack_assessment.md",
            saved["source"],
        )


# ---------------------------------------------------------
# 9. CONSTRUCTION PLANNING AND VALUATION
# ---------------------------------------------------------

with planning_tab:
    st.header("Construction Planning & Valuation")

    st.write(
        "Calculate an illustrative construction budget from your inputs. "
        "All monetary values are in Indian rupees (INR)."
    )

    col1, col2 = st.columns(2)

    with col1:
        area = st.number_input(
            "Built-up area (sq. ft.)",
            min_value=0.0,
            value=1000.0,
            step=100.0,
        )

        rate = st.number_input(
            "Construction rate (₹ per sq. ft.)",
            min_value=0.0,
            value=1800.0,
            step=100.0,
        )

        contingency_percent = st.number_input(
            "Contingency (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=1.0,
        )

    with col2:
        land_value = st.number_input(
            "Estimated land value (₹)",
            min_value=0.0,
            value=1500000.0,
            step=100000.0,
        )

        other_costs = st.number_input(
            "Other estimated costs (₹)",
            min_value=0.0,
            value=100000.0,
            step=10000.0,
        )

    base_cost = area * rate
    contingency = base_cost * contingency_percent / 100
    total_construction = base_cost + contingency + other_costs
    total_property_value = land_value + total_construction

    st.subheader("Estimated project summary")

    c1, c2 = st.columns(2)
    c1.metric("Base construction cost", f"₹{base_cost:,.0f}")
    c2.metric("Contingency", f"₹{contingency:,.0f}")

    c3, c4 = st.columns(2)
    c3.metric(
        "Total estimated construction",
        f"₹{total_construction:,.0f}",
    )
    c4.metric(
        "Illustrative total property value",
        f"₹{total_property_value:,.0f}",
    )

    st.caption(
        "Illustrative calculation only. These figures are based on "
        "user-provided inputs, not live market data, contractor quotations, "
        "or a certified property valuation."
    )

    budget = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "currency": "INR",
        "area_sq_ft": area,
        "construction_rate_inr_per_sq_ft": rate,
        "base_construction_cost_inr": base_cost,
        "contingency_percent": contingency_percent,
        "contingency_inr": contingency,
        "other_costs_inr": other_costs,
        "total_estimated_construction_inr": total_construction,
        "estimated_land_value_inr": land_value,
        "illustrative_total_property_value_inr": total_property_value,
    }

    st.download_button(
        "Download budget as JSON",
        data=json.dumps(budget, indent=2),
        file_name="construction_budget.json",
        mime="application/json",
    )

    st.divider()

    st.subheader("AI planning assistant")

    planning_question = st.text_area(
        "Ask about budgeting, construction sequencing, or project planning",
        placeholder=(
            "Example: What cost categories should I include "
            "in a house construction budget?"
        ),
        key="planning_question",
    )

    if st.button("Ask about planning", key="run_planning"):
        if not planning_question.strip():
            st.warning("Please enter a question.")
        else:
            prompt = f"""
You are a construction planning assistant for a college capstone.

Give practical, qualified guidance. Do not invent supplier quotations,
local market rates, permits, or engineering approvals. Explain when
local professional verification is required.

User question:
{planning_question}

Current illustrative budget:
{json.dumps(budget, indent=2)}
"""

            with st.spinner("Preparing planning guidance..."):
                report, source = ask_ai(
                    prompt=prompt,
                    category="planning",
                )

            st.session_state["planning_report"] = {
                "report": report,
                "source": source,
            }

    saved = st.session_state["planning_report"]

    if saved:
        show_report(
            saved["report"],
            "planning_guidance.md",
            saved["source"],
        )


# ---------------------------------------------------------
# 10. SITE ASSISTANT
# ---------------------------------------------------------

with assistant_tab:
    st.header("AI Site Assistant")

    st.write(
        "Ask questions about construction workflows, site documentation, "
        "materials, planning, and coordination."
    )

    site_question = st.text_area(
        "Your question",
        placeholder=(
            "Example: What should a daily construction "
            "progress report include?"
        ),
        key="site_question",
    )

    weather_context = st.selectbox(
        "Weather context (optional)",
        [
            "Not provided",
            "Hot and sunny",
            "Rain expected",
            "Heavy rain",
            "Strong winds",
            "Cold conditions",
        ],
    )

    if st.button("Get site guidance", key="run_assistant"):
        if not site_question.strip():
            st.warning("Please enter a question.")
        else:
            prompt = f"""
You are a construction site information assistant.

Answer clearly and practically. Do not replace advice from a qualified
engineer, safety officer, or local authority.

If weather could affect work, explain what should be checked locally.
Do not claim to have retrieved live weather data.

User-provided weather context: {weather_context}

User question:
{site_question}
"""

            with st.spinner("Preparing site guidance..."):
                report, source = ask_ai(
                    prompt=prompt,
                    category="assistant",
                )

            st.session_state["site_answer"] = {
                "report": report,
                "source": source,
            }

    saved = st.session_state["site_answer"]

    if saved:
        show_report(
            saved["report"],
            "site_guidance.md",
            saved["source"],
        )


# ---------------------------------------------------------
# 11. FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Multimodal Construction Intelligence Platform · College capstone "
    "prototype · Offline demonstration and optional Gemini integration"
)
