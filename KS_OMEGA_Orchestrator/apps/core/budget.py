from apps.core.utils import env, logger

def check_budget_cap(task):
    cap = float(env("KSOMEGA_MAX_BUDGET_USD", "25") or 25)
    declared = float(task.get("constraints", {}).get("budget_usd", cap))
    if declared > cap:
        logger("budget.cap.hit", {"cap": cap, "declared": declared, "action": "clamped"})
        task["constraints"]["budget_usd"] = cap
    return task
