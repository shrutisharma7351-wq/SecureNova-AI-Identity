from llm import ask_llm


class SimulatedAgent:
    def __init__(
        self,
        name="Agent",
        role="user",
        system_prompt="",
        tools=None
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.tools = tools or {}

    def respond(self, user_prompt: str) -> str:
        prompt = f"""
{self.system_prompt}

Your agent identity:
Name: {self.name}
Role: {self.role}

USER INPUT:
{user_prompt}
"""

        return ask_llm(prompt)

    def execute_privileged_action(self, action: str) -> str:
        allowed_actions = ["DELETE_TEST_USER"]

        if action not in allowed_actions:
            return f"[DENIED] Unknown privileged action: {action}"

        return f"[PRIVILEGED ACTION EXECUTED] {action}"

    def retrieve_knowledge(self, query: str, retriever) -> str:
        """
        Agent requests information from the simulated RAG retriever.
        """
        return retriever(query)

    def act_on_decision(
        self,
        response: str,
        target: str = "test-user"
    ):
        """
        The agent inspects the LLM's natural-language response.
        If the response indicates that an available tool should be
        used, the agent invokes that registered simulated tool.
        """

        response_lower = response.lower()

        for tool_name, tool_fn in self.tools.items():

            tool_name_lower = tool_name.lower()

            if (
                tool_name_lower in response_lower
                and (
                    "call" in response_lower
                    or "use" in response_lower
                    or "execute" in response_lower
                    or "action" in response_lower
                    or "should" in response_lower
                    or "recommend" in response_lower
                )
            ):
                return tool_fn(target)

        return None