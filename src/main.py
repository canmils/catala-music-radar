from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

researcher = Agent(
    role="Catalan Music Researcher",
    goal="Find possible new Catalan-language music releases from a provided list of artists.",
    backstory="You are careful, skeptical, and you never invent releases.",
    verbose=True
)

classifier = Agent(
    role="Catalan Language Classifier",
    goal="Classify whether music is likely in Catalan, mixed language, or not Catalan.",
    backstory="You are strict and avoid false positives.",
    verbose=True
)

reporter = Agent(
    role="Music Radar Reporter",
    goal="Create a short weekly music radar report.",
    backstory="You write clear, simple, useful summaries.",
    verbose=True
)

task = Task(
    description="""
    Create a sample Catalan music radar report using these artists:
    The Tyets, Figa Flawas, Mushkaa, Oques Grasses, Julieta.

    Do not invent exact release dates.
    Mark uncertain items clearly.
    Output:
    - Artist
    - Possible relevance
    - Confidence: High / Medium / Low
    - Why included
    """,
    expected_output="A short markdown report with clear confidence levels.",
    agent=reporter
)

crew = Crew(
    agents=[researcher, classifier, reporter],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)