from langchain_core.messages import SystemMessage, HumanMessage

with open("static/prompts/base_llm.txt") as f:
    base_llm_prompt = f.read()

with open("static/prompts/output_llm.txt") as f:
    output_llm_prompt = f.read()

system_prompt = SystemMessage(
        content=base_llm_prompt
    )

output_prompt = HumanMessage(
    content=output_llm_prompt
)