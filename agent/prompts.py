def planner_prompt(user_prompt: str) -> str:
    planner_prompt = f"""
                        You are the planner agent. Convert the user prompt into a complete engineering project plan.
                        User request: {user_prompt}
                    """
    return planner_prompt

def architect_prompt(plan: str) -> str:
    architect_prompt = f"""
                        You are the architect agent. Based on the following project plan, break it down into explicit engineering tasks.    

                        Rules:
                        - For each file in the plan, create one or implementation tasks.
                        - in each task description, specify:
                            * The task to implement.
                            * The name of the variables, functions, classes, annd componets to be defined.
                            * Mention how the task depends on or will be used by the previous and next tasks.
                            * Include integration details: imports, expected functions signatures, data flow.
                        - Order tasks so that dependnencies are implemented first.
                        - Each step must be self -contained but also carry forward the context from previous steps.

                        Project Plan: {plan}
                    """
    return architect_prompt

def coder_sys_prompt() -> str:
    coder_prompt = f"""
                        You are the coder agent. Based on the following project plan and task, generate the complete code implementation for the task.

                        Rules:
                        - Write clean, well-structured, and commented code.
                        - Follow best practices for the specified technologies.
                        - Ensure the code integrates seamlessly with previous tasks.
                        - Adhere to the function signatures and data flow specified in the task description.
                        - If the task depends on previous tasks, ensure those dependencies are correctly referenced.
                    """
    return coder_prompt