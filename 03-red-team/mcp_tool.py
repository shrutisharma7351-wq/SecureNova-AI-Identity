def disable_user_security(username: str) -> str:
    print("\n[MCP TOOL CALL]")
    print("Tool: disable_user_security")
    print(f"Target user: {username}")

    return f"[MCP ACTION EXECUTED] Security disabled for {username}"