from dotenv import load_dotenv
from langsmith import Client

from ls_evalvators import field_accuracy, escalation_correct,trajectory_match
from ls_target import run_agent

load_dotenv()

client = Client()

client.evaluate(
    run_agent,
    data="invoice-extraction-v1",
    evaluators=[field_accuracy, escalation_correct, trajectory_match],
    experiment_prefix="sonnet-escalation",
    max_concurrency=1,
)