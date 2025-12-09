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
        
        await self._orig_get_next_action(browser_state_summary)
        memory_text = None
        state = getattr(self.agent, "state", None)
        if state is not None:
            current_state = getattr(state, "current_state", None)
            if current_state is not None:
                memory_text = getattr(current_state, "memory", None)
            if memory_text is None:
                memory_text = getattr(state, "memory", None)
        if memory_text:
            print("[SafeWrapper] Scanning agent memory for reload intent and task abort intent...")
            self.monitor.scan_text_for_reload_intent(memory_text)
            self.monitor.scan_text_for_task_abort(memory_text)

        actions = getattr(self.agent.state.last_model_output, "action", None)

        
        if not actions:
            return
        #wait - usually for trying to reload page
        for act in actions:
            act_dict = act.model_dump()
            
            act_name = next(iter(act_dict))
            print("ACTION TYPE:", act_name)
            flagged_repeat = self.monitor.record_action(act_name)
            if flagged_repeat:
                print("🚨 SUSPICIOUS BEHAVIOR: too many repeated actions")
                self.agent.stop()
                return

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

