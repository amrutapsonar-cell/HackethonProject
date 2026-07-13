!pip install -q nest_asyncio
# ==============================================================================
# STEP 1: SYSTEM DEPENDENCY INSTALLATION
# ==============================================================================
import sys
import os

# Install mandatory frameworks quietly
print("[INFO] Installing CrewAI, LangChain Gemini, and dependencies...")
!pip install -q crewai langchain-google-genai duckduckgo-search

# ==============================================================================
# STEP 2: SYSTEM CONFIGURATION & INITIALIZATION
# ==============================================================================
import os
import sys
from google.colab import userdata
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool  
from crewai import Agent, Task, Crew, Process, LLM # <--- Added LLM import

# Validate and ingest secret API token
try:
    gemini_key = userdata.get('GEMINI_API_KEY')
    os.environ["GEMINI_API_KEY"] = gemini_key
    print("[SUCCESS] Gemini API Key successfully loaded from Colab Secrets.")
except Exception as e:
    print("[ERROR] Failed to fetch GEMINI_API_KEY from Colab Secrets. Ensure it is added to the left-hand key menu.")
    sys.exit(1)

# Initialize Gemini using CrewAI's native LLM wrapper
gemini_llm = LLM(
    model="gemini/gemini-1.5-pro", # <--- Prefix with 'gemini/'
    temperature=0.15
)

# ==============================================================================
# WRAP DUCKDUCKGO IN CREWAI'S NATIVE @TOOL DECORATOR
# ==============================================================================
@tool("DuckDuckGo Web Search")
def search_tool(query: str) -> str:
    """Use this tool to search the web for current events, corporate news, and market information."""
    return DuckDuckGoSearchRun().run(query)

# ==============================================================================
# STEP 3: CREWAI AGENT DEFINITIONS 
# ==============================================================================
market_researcher = Agent(
    role='Automotive Market Intelligence Lead',
    goal='Thoroughly research Indian automotive companies (OEMs and Tier-1 suppliers) to uncover concrete operational, logistical, and quality control bottlenecks.',
    backstory="""You are a veteran equity research analyst and industrial engineer specializing in the Indian automotive sector. 
    You have a deep understanding of corporate ecosystems, from tier-2 component manufacturing up to major passenger and commercial vehicle OEMs. 
    Your analytical style is completely objective, data-driven, and focused on identifying hidden friction points in corporate operations—such as 
    climbing warranty overheads, multi-tier supply chain bottlenecks, inflationary logistics pressures, and underperforming dealer networks.""",
    verbose=False,
    allow_delegation=False,
    tools=[search_tool], 
    llm=gemini_llm
)

solutions_architect = Agent(
    role='B2B Automotive Consulting Solutions Architect',
    goal='Precisely map discovered corporate challenges to the exact core services offered in the XYZ Analytics Consulting Product Handbook.',
    backstory="""You are the principal solutions architect at XYZ Analytics Consulting. You are an expert at transforming raw corporate vulnerabilities 
    into structured, data-driven analytics engineering projects. You know the XYZ Analytics Product & Solutions Handbook inside and out. 
    You translate operational pain points into quantifiable business cases, defining exact KPIs to track and mapping out clear, multi-phase 
    implementation roadmaps that justify enterprise expenditure.""",
    verbose=False,
    allow_delegation=False,
    llm=gemini_llm
)

# Initialize Gemini using CrewAI's native LLM wrapper
gemini_llm = LLM(
    model="gemini/gemini-1.5-pro-latest", # <--- Added the -latest suffix
    temperature=0.15
)

# ==============================================================================
# STEP 4: DEFINITION OF CORE ANALYSIS RUNNER
# ==============================================================================
import nest_asyncio
import time

# Apply nest_asyncio to prevent Colab event loop conflicts
nest_asyncio.apply()

def execute_sales_intelligence_pipeline(company_name, segment, primary_focus):
    print(f"\n[EXECUTION] Initiating Intelligence Synthesis for: {company_name} ({segment})...")
    
    research_task = Task(
        description=f"""Conduct targeted market research on {company_name}, operating within the Indian automotive {segment} domain.
        Identify current systemic operational challenges they face. Focus specifically on areas relating to {primary_focus}.
        Provide clear, structural notes detailing where their operational vulnerabilities lie.""",
        expected_output="A bulleted list highlighting concrete operational or logistical bottlenecks.",
        agent=market_researcher
    )

    mapping_task = Task(
        description=f"""Review the operational vulnerabilities found for {company_name}. 
        Map these findings directly to exactly ONE solution from the XYZ Product Handbook:
        - Warranty Analytics
        - Supply-Chain Risk Prediction
        - Dealer & Field Service Intelligence
        
        Draft a high-impact executive recommendation. Do NOT use introductory statements like 'Based on...' or 'According to...'. 
        Incorporate the exact KPI metrics and matching ROI percentage improvements defined in the XYZ Product Handbook context.""",
        expected_output="""A professional corporate dossier structured EXACTLY as follows:
        ### [COMPANY NAME] — TARGET DOSSIER
        * **Recommended Consulting Solution:** [Exact match from the 3 handbook options]
        * **Identified Core Business Challenges:** [Brief synthesis of operational pain points]
        * **Expected Business Value & Target KPIs:** [Explicitly quote relevant metrics and ROI gains from the handbook]
        * **Projected Deployment Roadmap:** [Outline Phase 1, Phase 2, and Phase 3 timeline over a 9-12 month horizon]""",
        agent=solutions_architect
    )

    pipeline_crew = Crew(
        agents=[market_researcher, solutions_architect],
        tasks=[research_task, mapping_task],
        process=Process.sequential
    )

    # Revert to standard kickoff() now that nest_asyncio is handling the environment
    return pipeline_crew.kickoff()

# ==============================================================================
# STEP 5: PIPELINE EXECUTION LOOP
# ==============================================================================
# TIP: For testing, let's just run 2 companies to ensure it works before running all 12
target_companies = [
    {"name": "Maruti Suzuki India Ltd.", "segment": "Passenger Vehicle OEM", "focus": "Dealership Networks & Aftermarket Data Fragmentation"},
    {"name": "Tata Motors Ltd.", "segment": "Passenger, Commercial & EV OEM", "focus": "EV Battery Sourcing & Multi-Tier Supplier Delays"},
    # Uncomment the rest once you confirm the first two work perfectly!
    # {"name": "Mahindra & Mahindra Ltd.", "segment": "SUV & Agricultural Tractor OEM", "focus": "Heavy-Duty Component Failure Rates & Supplier Defects"},
    # {"name": "Bosch Limited India", "segment": "Tier-1 Component Supplier", "focus": "Global Electronic Import Bottlenecks & Inbound Logistics Lead Times"},
]

final_compiled_report = ""

for target in target_companies:
    try:
        dossier_output = execute_sales_intelligence_pipeline(target["name"], target["segment"], target["focus"])
        final_compiled_report += str(dossier_output) + "\n\n---\n\n"
        
        # Add a 10-second delay between companies to prevent API Rate Limiting
        print("[INFO] Pausing for 10 seconds to respect API rate limits...")
        time.sleep(10) 
        
    except Exception as e:
        print(f"[ERROR] Failed to process {target['name']}. Error: {e}")

print("\n" + "="*80)
print("FINAL COMPILED SALES INTELLIGENCE TARGET DOSSIER MATRIX")
print("="*80 + "\n")
print(final_compiled_report)
