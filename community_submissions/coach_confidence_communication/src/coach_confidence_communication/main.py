import argparse

from coach_confidence_communication.crew import ConfidenceCoachCrew


def run() -> None:
    parser = argparse.ArgumentParser(description="Run the AI Confidence Coach crew.")
    parser.add_argument("--text", required=True, help="Message or transcript to analyze")
    parser.add_argument("--context", default="general", help="Context such as request, feedback, update")
    args = parser.parse_args()

    crew = ConfidenceCoachCrew().crew()
    result = crew.kickoff(inputs={"text": args.text, "context": args.context})
    print(result)


if __name__ == "__main__":
    run()
