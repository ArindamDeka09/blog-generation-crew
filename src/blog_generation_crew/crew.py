from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
import os
from crewai import LLM

# Base LLM configuration with an extended timeout buffer for stable connections
# Fully configured open-proxy wrapper with a 10-minute timeout buffer
# and custom client argument maps to prevent 504 gateway disconnects
NIM_LLM = LLM(
    model="openai/meta/llama-3.1-70b-instruct",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY"),
    timeout=600.0,      # Informs the internal wrapper to maintain the connection for 10 minutes
    max_tokens=4000,    # Preserves your long-form token generation runway
    config=dict(
        connect_timeout=600.0, # Forces the underlying HTTP client transport layer to hold the link open
        read_timeout=600.0
    )
)

# Optimized Search Tool: Chunks and compresses data so the manager isn't overwhelmed
web_search_tool = SerperDevTool(
    config=dict(
        llm=dict(
            provider="nvidia",
            config=dict(
                model="meta/llama-3.1-70b-instruct",
                api_key=os.environ.get("NVIDIA_API_KEY"),
                base_url="https://integrate.api.nvidia.com/v1"
            ),
        ),
        embedder=dict(
            provider="nvidia",
            config=dict(
                model="nvidia/nv-embed-qa-4",
                api_key=os.environ.get("NVIDIA_API_KEY"),
                base_url="https://integrate.api.nvidia.com/v1"
            ),
        ),
    )
)

@CrewBase
class BlogGenerationCrew():
    """BlogGenerationCrew crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # 1. Define your Team Leader / Project Manager Agent
    @agent
    def team_leader(self) -> Agent:
        return Agent(
            config=self.agents_config["team_leader"],
            llm=NIM_LLM,
            verbose=True,
            allow_delegation=True  # Crucial for hierarchical workflows
        )

    # 2. Define your Team Members
    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            llm=NIM_LLM,
            verbose=True,
            allow_delegation=False,
            tools=[web_search_tool]
        )

    @agent
    def blog_writing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["blog_writing_agent"],
            llm=NIM_LLM,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def blog_review_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["blog_review_agent"],
            llm=NIM_LLM,
            verbose=True,
            allow_delegation=False
        )

    # Define the task for the crew
    @task
    def blog_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["blog_writing_task"],
            output_file="blog.md"
        )

    # 3. Complete Hierarchical Setup
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,  # Keeps your tutor's assignment completely intact
            verbose=True,
            manager_llm=NIM_LLM  # The leader coordinates all agent interactions
        )