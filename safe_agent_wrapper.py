# safe_agent_wrapper.py

# safe_agent_wrapper.py
from runtime_monitor import RuntimeMonitor

class SafeAgentWrapper:
    def __init__(self, agent, monitor: RuntimeMonitor):
        self.agent = agent
        self.monitor = monitor

        self._orig_get_next_action = agent._get_next_action
        agent._get_next_action = self._wrapped_get_next_action

    async def run(self, *args, **kwargs):
        return await self.agent.run(*args, **kwargs)

    def stop(self):
        return self.agent.stop()

    async def _wrapped_get_next_action(self, browser_state_summary):
        # Let the agent plan as usual
        await self._orig_get_next_action(browser_state_summary)

        actions = getattr(self.agent.state.last_model_output, "action", None)

        print("\n==== ACTIONS DETECTED ====")
        print(actions)

        if not actions:
            return

        for act in actions:
            act_dict = act.model_dump()
            print("RAW ACTION DICT:", act_dict)

            # e.g. {'access_downloads': {...}} → act_name = 'access_downloads'
            act_name = next(iter(act_dict))
            print("ACTION TYPE:", act_name)

            # 1) Existing repeat detector
            flagged_repeat = self.monitor.record_action(act_name)
            if flagged_repeat:
                print("🚨 SUSPICIOUS BEHAVIOR: too many repeated actions")
                self.agent.stop()
                return

            # 2) FILE ACCESS / EXFILTRATION GUARD

            # Case 1: direct file access tool
            if act_name == "access_downloads":
                details = act_dict.get("access_downloads", {})
                flagged_file = self.monitor.record_file_access(
                    tool_name="access_downloads",
                    details=details,
                )
                if flagged_file:
                    print("🚨 FILE ACCESS BLOCKED by SafeAgentWrapper")
                    self.agent.stop()
                    return

            # Case 2: exfiltration via send_email
            if act_name == "send_email":
                details = act_dict.get("send_email", {})
                flagged_email = self.monitor.record_file_access(
                    tool_name="send_email",
                    details=details,
                )
                if flagged_email:
                    print("🚨 EMAIL EXFILTRATION BLOCKED by SafeAgentWrapper")
                    self.agent.stop()
                    return
        return




# safe_agent_wrapper.py
# //////
# from datetime import datetime
# from runtime_monitor import RuntimeMonitor, AgentEvent
# import functools
# import inspect

# class SafeAgentWrapper:
#     def __init__(self, agent, monitor):
#         self.agent = agent
#         self.monitor = monitor

#         # Save original
#         self._orig_get_next_action = agent._get_next_action

#         # Patch
#         agent._get_next_action = self._wrapped_get_next_action

#     # NEW — forward run() to underlying agent
#     async def run(self, *args, **kwargs):
#         return await self.agent.run(*args, **kwargs)

#     # NEW — let wrapper still stop the real agent
#     def stop(self):
#         return self.agent.stop()

#     async def _wrapped_get_next_action(self, browser_state_summary):
#         # Call original first
#         await self._orig_get_next_action(browser_state_summary)

#         # NOW the actions exist
#         actions = getattr(self.agent.state.last_model_output, "action", None)

#         print("\n==== ACTIONS DETECTED ====")
#         print(actions)

#         if actions:
#             for act in actions:
#                 # Name of the action (navigate, click, scroll, extract)
#                 act_dict = act.model_dump()
#                 act_name = next(iter(act_dict))

#                 print("ACTION:", act_name)

#                 flagged = self.monitor.record_action(act_name)
#                 if flagged:
#                     print("🚨 SUSPICIOUS BEHAVIOR")
#                     self.agent.stop()
#         return


# ////////////////////////
# class SafeAgentWrapper:
#     def __init__(self, agent, monitor):
#         self.agent = agent
#         self.monitor = monitor
#         self._orig_execute_step = agent._execute_step
#         agent._execute_step = self._wrapped_execute_step

#     # NEW — forward run() to underlying agent
#     async def run(self, *args, **kwargs):
#         return await self.agent.run(*args, **kwargs)

#     # NEW — let wrapper still stop the real agent
#     def stop(self):
#         return self.agent.stop()

#     async def _wrapped_execute_step(self, step_index, step_info, *args, **kwargs):

#         print("\n========== STEP DEBUG ==========")
#         print("STEP INDEX =", step_index)
#         print("TYPE(step_info) =", type(step_info))
#         print("DIR(step_info) =", dir(step_info))
#         print("RAW step_info =", step_info)

#         # extract the REAL action name
#         action_name = getattr(step_info, "action", None)
#         print("ACTION NAME:", action_name)

#         # detector
#         if action_name:
#             flagged = self.monitor.record_action(action_name)
#             if flagged:
#                 print("🚨 SECURITY LOOP DETECTED:", action_name)
#                 self.agent.stop()
#                 return

#         # run original browser-use behavior
#         return await self._orig_execute_step(step_index, step_info, *args, **kwargs)



#belows works



# class SafeAgentWrapper:
#     """Wraps Browser-Use Agent by intercepting Playwright page inside _execute_step()."""

#     def __init__(self, agent, monitor: RuntimeMonitor):
#         self.agent = agent
#         self.monitor = monitor

#         # Patch the agent's _execute_step method
#         original_execute_step = agent._execute_step

#         async def wrapped_execute_step(*args, **kwargs):
#             # Run the original _execute_step first
#             result = await original_execute_step(*args, **kwargs)

#             # After the first step, browser session should exist
#             session = getattr(self.agent, "browser_session", None)
#             if not session:
#                 return result

#             page = getattr(session, "page", None)
#             if not page:
#                 return result

#             # Patch only once
#             if not hasattr(page, "_wrapped_by_detector"):

#                 original_goto = page.goto
#                 original_reload = page.reload

#                 async def safe_goto(url, *a, **k):
#                     print(f"[Wrapper] Intercepted GOTO → {url}")
#                     self.monitor.observe(
#                         AgentEvent(
#                             action_type="goto",
#                             url=url,
#                             timestamp=datetime.utcnow()
#                         )
#                     )
#                     return await original_goto(url, *a, **k)

#                 async def safe_reload(*a, **k):
#                     current_url = page.url
#                     print(f"[Wrapper] Intercepted RELOAD → {current_url}")
#                     self.monitor.observe(
#                         AgentEvent(
#                             action_type="reload",
#                             url=current_url,
#                             timestamp=datetime.utcnow()
#                         )
#                     )
#                     return await original_reload(*a, **k)

#                 page.goto = safe_goto
#                 page.reload = safe_reload
#                 page._wrapped_by_detector = True

#                 print("🔒 Wrapper successfully attached to Playwright page")

#             return result

#         # Patch the method
#         agent._execute_step = wrapped_execute_step

#     async def run(self):
#         try:
#             return await self.agent.run()
#         except Exception as e:
#             print("\n🚨 SECURITY VIOLATION — AGENT STOPPED 🚨")
#             print("Reason:", e)
#             print("--------------------------------------------------\n")
#             raise


# from datetime import datetime
# from runtime_monitor import RuntimeMonitor, AgentEvent


# class SafeAgentWrapper:
#     """Wraps browser-use's Agent and intercepts its browser actions."""

#     def __init__(self, agent, monitor: RuntimeMonitor):
#         self.agent = agent
#         self.monitor = monitor

#         # intercept playwright page once browser is launched
#         agent.on_browser_launch = self._patch_playwright_page

#     async def run(self):
#         return await self.agent.run()

#     def _patch_playwright_page(self, page):
#         """Hook into Playwright API the agent uses."""
        
#         original_goto = page.goto
#         original_reload = page.reload

#         async def safe_goto(url, *args, **kwargs):
#             self.monitor.observe(
#                 AgentEvent(
#                     action_type="goto",
#                     url=url,
#                     timestamp=datetime.utcnow()
#                 )
#             )
#             return await original_goto(url, *args, **kwargs)

#         async def safe_reload(*args, **kwargs):
#             current_url = page.url
#             self.monitor.observe(
#                 AgentEvent(
#                     action_type="reload",
#                     url=current_url,
#                     timestamp=datetime.utcnow()
#                 )
#             )
#             return await original_reload(*args, **kwargs)

#         # Monkey patch
#         page.goto = safe_goto
#         page.reload = safe_reload
