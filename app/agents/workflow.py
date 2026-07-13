from typing import TypedDict
from app.agents.skill_gap_agent import analyze_skill_gap
from langgraph.graph import StateGraph, END
from app.agents.resume_agent import analyze_resume
from app.agents.resume_tailor_agent import tailor_resume
from app.agents.interview_agent import generate_interview_prep
class AgentState(TypedDict):
    resume_text: str
    summary: str
    job_description: str
    skill_gap: dict
    tailored_resume: dict
    interview_prep: dict


def resume_node(state: AgentState):
    summary = analyze_resume(state["resume_text"])
    return {"summary": summary}
def skill_gap_node(state: AgentState):
    print("STATE RECEIVED:", state)

    result = analyze_skill_gap(
        state["summary"],
        state["job_description"]
    )

    return {
        "skill_gap": result
    }
def resume_tailor_node(state: AgentState):
    skill_gap = state["skill_gap"]

    result = tailor_resume(
        state["summary"],
        skill_gap.missing_skills,
        skill_gap.recommended_skills
    )

    return {
        "tailored_resume": result.model_dump()
    }
    

def interview_prep_node(state: AgentState):
    skill_gap = state["skill_gap"]

    result = generate_interview_prep(
        state["summary"],
        state["job_description"],
        skill_gap.missing_skills
    )

    return {
        "interview_prep": result.model_dump()
    } 
    
graph = StateGraph(AgentState)

graph.add_node("resume_analyzer", resume_node)
graph.add_node("skill_gap_analyzer", skill_gap_node)
graph.add_node("resume_tailor", resume_tailor_node)
graph.add_node("interview_prep", interview_prep_node)

graph.set_entry_point("resume_analyzer")

graph.add_edge("resume_analyzer", "skill_gap_analyzer")
graph.add_edge("skill_gap_analyzer", "resume_tailor")
graph.add_edge("resume_tailor", "interview_prep")
graph.add_edge("interview_prep", END)
workflow = graph.compile()