import json
import logging
import os
import shutil
import sys

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from colorama import Fore
from dotenv import load_dotenv

from camel_database_agent import DatabaseAgent
from camel_database_agent.database_base import TrainLevel

load_dotenv()

"""设置日志"""
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logging.getLogger("camel_database_agent").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

model = ModelFactory.create(
    model_platform=ModelPlatformType.DEFAULT,
    model_type=ModelType.GPT_4O_MINI,
)

# model = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
#     model_type=os.environ["API_MODEL_TYPE"],
#     api_key=os.environ["API_KEY"],
#     url=os.environ["API_URL"],
# )

current_dir = os.path.dirname(os.path.abspath(__file__))
spider2_sqlite_database = os.path.join(current_dir, "database", "local_sqlite")
spider2_workspace = os.path.join(current_dir, "workspace", os.environ["API_MODEL_TYPE"])
if not os.path.exists(spider2_workspace):
    os.makedirs(spider2_workspace)
else:
    shutil.rmtree(spider2_workspace)
    os.makedirs(spider2_workspace)

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
                print(f"{Fore.GREEN}{instance_id} success, count {success}{Fore.RESET}")
            else:
                example["result"] = False
                failed += 1
                print(f"{Fore.RED}{instance_id} failed, count {failed}{Fore.RESET}")
        except Exception as e:
            print(str(e))
        finally:
            print(
                f"{Fore.GREEN}success: {success}, "
                f"failed: {Fore.RED}{failed}{Fore.RESET}, "
                f"total: {total}"
            )

        with open(os.path.join(spider2_workspace, "spider2-lite-result.jsonl"), "a") as f:
            f.write(json.dumps(example) + "\n")
