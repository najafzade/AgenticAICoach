from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from coach_confidence_communication.tools.confidence_tools import (
    confidence_marker_detector,
    confidence_rewrite_guidance,
)


@CrewBase
class ConfidenceCoachCrew:
    """Crew for analyzing and strengthening communication confidence."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["analyzer"],
            tools=[confidence_marker_detector],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def coach(self) -> Agent:
        return Agent(
            config=self.agents_config["coach"],
            tools=[confidence_rewrite_guidance],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def analyze_communication(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_communication"],
            agent=self.analyzer(),
        )

    @task
    def craft_feedback(self) -> Task:
        return Task(
            config=self.tasks_config["craft_feedback"],
            agent=self.coach(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
