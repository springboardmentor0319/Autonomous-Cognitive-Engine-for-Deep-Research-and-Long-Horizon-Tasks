"""
Full Multi-Agent Research System

This module integrates all components of the research system:
- User clarification and scoping
- Research brief generation  
- Multi-agent research coordination
- Final report generation
- Automatic report saving to disk

The system orchestrates the complete research workflow from initial user
input through final report delivery.
"""

from pathlib import Path
from datetime import datetime

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from deep_research_from_scratch.utils import get_today_str
from deep_research_from_scratch.prompts import final_report_generation_prompt
from deep_research_from_scratch.state_scope import AgentState, AgentInputState
from deep_research_from_scratch.research_agent_scope import (
    clarify_with_user,
    write_research_brief,
)
from deep_research_from_scratch.multi_agent_supervisor import supervisor_agent

# ===== Config =====

from langchain.chat_models import init_chat_model

# Primary: Google Gemini | Alternatives: "openai:gpt-4.1", "anthropic:claude-sonnet-4-20250514"
writer_model = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    temperature=0.0,
    max_tokens=32000,
)

# ===== FINAL REPORT GENERATION =====

async def final_report_generation(state: AgentState):
    """
    Final report generation node.

    Synthesizes all research findings into a comprehensive final report
    and saves it as a Markdown file.
    """

    notes = state.get("notes", [])
    findings = "\n".join(notes)

    final_report_prompt = final_report_generation_prompt.format(
        research_brief=state.get("research_brief", ""),
        findings=findings,
        date=get_today_str(),
    )

    # Generate final report
    final_report = await writer_model.ainvoke(
        [HumanMessage(content=final_report_prompt)]
    )

    report_text = final_report.content

    # ===== SAVE REPORT TO FILE =====

    # Create output directory inside project
    output_dir = Path("files")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"research_report_{timestamp}.md"
    file_path = output_dir / file_name

    # Write report to file
    file_path.write_text(report_text, encoding="utf-8")

    print(f"\n✅ Report saved to: {file_path.resolve()}\n")

    return {
        "final_report": report_text,
        "messages": [f"Here is the final report:\n\n{report_text}"],
    }


# ===== GRAPH CONSTRUCTION =====

deep_researcher_builder = StateGraph(
    AgentState,
    input_schema=AgentInputState
)

# Add workflow nodes
deep_researcher_builder.add_node("clarify_with_user", clarify_with_user)
deep_researcher_builder.add_node("write_research_brief", write_research_brief)
deep_researcher_builder.add_node("supervisor_subgraph", supervisor_agent)
deep_researcher_builder.add_node("final_report_generation", final_report_generation)

# Add workflow edges
deep_researcher_builder.add_edge(START, "clarify_with_user")
deep_researcher_builder.add_edge("write_research_brief", "supervisor_subgraph")
deep_researcher_builder.add_edge("supervisor_subgraph", "final_report_generation")
deep_researcher_builder.add_edge("final_report_generation", END)

# Compile workflow
agent = deep_researcher_builder.compile()