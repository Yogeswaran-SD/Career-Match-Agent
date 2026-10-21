import os
from dotenv import load_dotenv
from langchain.agents import create_agent
import gradio as gr


from shared_tools import web_search_tool, get_job_recommendation, get_resume_data
from llm import create_llm
from system_prompt import SYSTEM_PROMPT_LOCAL_TOOLS

load_dotenv()

llm = create_llm()
tools = [web_search_tool, get_job_recommendation, get_resume_data]
SYSTEM_PROMPT = SYSTEM_PROMPT_LOCAL_TOOLS

job_search_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def run_agent(job_title: str, salary: int):
    user_prompt = (
        f"I'm looking for {job_title} roles with a minimum annual salary "
        f"of ₹{salary}. Find matching live job openings, check my resume "
        f"against the skills these jobs require, and give me a prep plan "
        f"for any skills I'm missing."
    )

    response = job_search_agent.invoke({
        "messages": [{"role": "user", "content": user_prompt}]
    })

    print("\n\n\nACTUAL RESPONSE WITH TOOLS\n\n\n", response)

    return response["messages"][-1].content

def deploy_agent():
    with gr.Blocks(title="Career Match Agent") as iface:
        gr.Markdown("## Career Match Agent")
        gr.Markdown("Finds job openings matched to your resume, using live listings and your indexed resume data.")
        job_title = gr.Textbox(label="Job Title / Keywords", placeholder="python")
        salary = gr.Textbox(label="Minimum Annual Salary (INR)", placeholder="400000")
        find_jobs_btn = gr.Button("Find Jobs", variant="primary")
        output = gr.Textbox(label="Recommended Jobs", lines=20)
        find_jobs_btn.click(fn=run_agent, inputs=[job_title, salary], outputs=output)
    iface.launch()

if __name__ == "__main__":
    # response = run_agent("react", "40000")
    # print("\nCLEAN RESPONSE\n")
    # print(response)
    deploy_agent()