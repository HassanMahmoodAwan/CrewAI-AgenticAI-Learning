from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Crew
from crewai.tools import BaseTool
import os

load_dotenv(".env")


orginal_fuzzy_email = """
hi sir,yesterday i send email, you can PFA but no one reply and still work not done and i dont understand why this happening. i already explain before but again same issue coming. ABL team is not serious and delay is too much. i am waiting long time and now very frustrate. please see this and do something fast because client also asking again and again and i dont have answer. POC is overdue now.
also meeting was plan but no update and nobody inform me anything. this is not good way working. kindly check and revert me asap.
regards, hassan
"""  

class ReplaceJargonTool(BaseTool):
    name:str = "Replace Jargon Tool"
    description:str = "A tool to replace jargon's in emails with simpler language."
    
    def _run(self, email: str) -> str:
        jargon_dict = {
            "ABL" : "Allied Bank Limited",
            "KPI" : "Key Performance Indicator",
            "ROI" : "Return on Investment",
            "ASAP" : "As Soon As Possible",
            "FYI" : "For Your Information",
            "POC" : "Proof of Concept",
            "PFA": "Please Find Attachment",
        }
        email = email.lower()
        suggestions = []
        for jargon, simple in jargon_dict.items():
            if jargon.lower() in email:
                suggestions.append(f"Replace Jargon '{jargon}' with '{simple}'.")
                
        return "\n".join(suggestions) if suggestions else "No jargon exists with in email."


try:
    
    jt = ReplaceJargonTool()
    print(jt.run(orginal_fuzzy_email))  


    llm = LLM(
        model="gpt-4.1-mini",
        temperature=0.1,
    )

    email_assistant = Agent(
        role = "Allied Bank Email Assistant",
        goal = "You are an expert email assistant for Allied Bank, helping employees to make there email communication more     professional and effective.",
        backstory = "You have high skills in communication, expert in writing professional.",
        tools = [ReplaceJargonTool()],
        llm = llm,
        # verbose = True
    )


    task = Task(
        description = f"Improve Email professionally as I provided you the rough email: ''''{orginal_fuzzy_email}''' ",
        agent = email_assistant,
        expected_output = "A professional and well-structured email that conveys the same message in a polite and effective manner."
    )

    crew = Crew(
        agents = [email_assistant],
        tasks = [task],
        llm = llm,
        verbose = True
    )

    result = crew.kickoff()

    print(result)
    
except Exception as e:
    print(f"An error occurred: {e}")