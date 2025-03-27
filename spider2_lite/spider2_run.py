import json
import logging
import os
import sys

from camel.models import ModelFactory
from camel.types import ModelPlatformType
from colorama import Fore
from dotenv import load_dotenv

from camel_database_agent import DatabaseAgent
from camel_database_agent.database_base import TrainLevel

load_dotenv()

"""设置日志"""
logging.basicConfig(
    level=logging.FATAL,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logging.getLogger("camel_database_agent").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type=os.environ["MODEL_NAME"],
    api_key=os.environ["OPENAI_API_KEY"],
    url=os.environ["OPENAI_API_BASE_URL"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))
spider2_sqlite_database = os.path.join(current_dir, "database", "local_sqlite")
spider2_workspace = os.path.join(current_dir, "workspace", os.environ["MODEL_NAME"])
if not os.path.exists(spider2_workspace):
    os.makedirs(spider2_workspace)
else:
    pass
    # shutil.rmtree(spider2_workspace)
    # os.makedirs(spider2_workspace)

with open(os.path.join(current_dir, "spider2-lite.jsonl"), "r") as f:
    examples = [json.loads(line) for line in f]
    examples = [example for example in examples if example["instance_id"].startswith("local")]
    examples = sorted(examples, key=lambda x: x["db"])

    database_agent_cache = {}
    success = 0
    failed = 0
    total = len(examples)
    for example in examples:
        try:
            instance_id = example["instance_id"]
            db_id = example["db"]
            question = example["question"]
            db_path = os.path.join(spider2_sqlite_database, f"{db_id}.sqlite")
            if not os.path.exists(db_path):
                print(f"{Fore.RED}database {db_id} not found{Fore.RESET}")
                continue
            if db_id not in database_agent_cache:
                database_agent_cache[db_id] = database_agent = DatabaseAgent(
                    db_url=f"sqlite:///{db_path}",
                    model=model,
                    data_path=os.path.join(str(spider2_workspace), db_id),
                )
                database_agent.train_knowledge(
                    level=TrainLevel.LOW,
                    reset_train=False,
                )
            database_agent = database_agent_cache[db_id]
            response = database_agent.ask(
                session_id=instance_id,
                question=question,
            )

            example["sql"] = response.sql
            if response.success:
                example["result"] = True
                success += 1
            else:
                example["result"] = False
                failed += 1
        except Exception as e:
            print(f"{Fore.RED}{e!s}{Fore.RESET}")
        finally:
            print(f"process {success+failed}/{total}")

        with open(os.path.join(spider2_workspace, "spider2-lite-result.jsonl"), "a") as f:
            f.write(json.dumps(example) + "\n")

    print(
        f"success: {success}, failed: {failed}, total: {total}",
    )
