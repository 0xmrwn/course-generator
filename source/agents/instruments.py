import os

from modules import file

BASE_DIR = os.environ.get("BASE_DIR", "./agent_results")


class AgentInstruments:
    """
    Base class for multli-agent instruments that are tools, state, and functions that an agent can use across the lifecycle of conversations
    """

    def __init__(self) -> None:
        self.session_id = None
        self.messages = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def sync_messages(self, messages: list):
        """
        Syncs messages with the orchestrator
        """
        raise NotImplementedError

    def make_agent_chat_file(self, team_name: str):
        return os.path.join(self.root_dir, f"agent_chats_{team_name}.json")

    def make_agent_cost_file(self, team_name: str):
        return os.path.join(self.root_dir, f"agent_cost_{team_name}.json")

    @property
    def root_dir(self):
        return os.path.join(BASE_DIR, self.session_id)


class FileAgentInstruments(AgentInstruments):
    """
    Unified Toolset for the Postgres Data Analytics Multi-Agent System

    Advantages:
        - All agents have access to the same state and functions
        - Gives agent functions awareness of changing context
        - Clear and concise capabilities for agents
        - Clean database connection management

    Guidelines:
        - Agent Functions should not call other agent functions directly
            - Instead Agent Functions should call external lower level modules
        - Prefer 1 to 1 mapping of agents and their functions
        - The state lifecycle lives between all agent orchestrations
    """

    def __init__(self, session_id: str) -> None:
        super().__init__()

        self.session_id = session_id
        self.messages = []
        self.reset_files()

    def sync_messages(self, messages: list):
        """
        Syncs messages with the orchestrator
        """
        self.messages = messages

    def reset_files(self):
        """
        Clear everything in the root_dir
        """

        # if it does not exist create it
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        for fname in os.listdir(self.root_dir):
            os.remove(os.path.join(self.root_dir, fname))

    def get_file_path(self, fname: str):
        """
        Get the full path to a file in the root_dir
        """
        return os.path.join(self.root_dir, fname)

    # -------------------------- Agent Properties -------------------------- #

    # -------------------------- Agent Functions -------------------------- #

    def write_file(self, content: str):
        fname = self.get_file_path("write_file.txt")
        return file.write_file(fname, content)

    def write_json_file(self, json_str: str):
        fname = self.get_file_path("write_json_file.json")
        return file.write_json_file(fname, json_str)
