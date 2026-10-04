from langgraph.checkpoint.postgres import PostgresSaver

from app.core.config import settings


class CheckpointerManager:

    def __init__(self):
        self.checkpointer = None
        self.connection_context = None

    def startup(self):
        self.connection_context = (
            PostgresSaver.from_conn_string(
                settings.checkpoint_database_url
            )
        )

        self.checkpointer = (
            self.connection_context.__enter__()
        )

        # Creates LangGraph checkpoint tables
        # the first time.
        self.checkpointer.setup()

        return self.checkpointer

    def shutdown(self):
        if self.connection_context:
            self.connection_context.__exit__(
                None,
                None,
                None,
            )

            self.connection_context = None
            self.checkpointer = None


checkpointer_manager = CheckpointerManager()