def planner_prompt(user_prompt: str) -> str:
    planner_prompt = f"""
                        You are the planner agent. Convert the user prompt into a complete engineering project plan.
                        User request: {user_prompt}
                    """
    return planner_prompt