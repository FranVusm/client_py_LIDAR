# src/application/use_cases/monitor.py
import asyncio
from datetime import datetime
from typing import Dict, Callable, List

class OpcSubscriptionHandler:
    def __init__(self, attr_map: Dict[str, str], si3_entity, history_repo):
        """
        attr_map: domain_attr -> node_id
        """
        self.attr_map = attr_map
        self.rev_map = {v: k for k, v in attr_map.items()}
        self.si3 = si3_entity
        self.history = history_repo

    async def datachange_notification(self, node, val, data):
        # asyncua may call this synchronously; allow both
        nodeid = node.nodeid.to_string()
        attr = self.rev_map.get(nodeid)
        ts = datetime.utcnow()
        if attr:
            # attribute names in entity should match attr_map keys (case-insensitive)
            attr_lower = attr.lower()
            self.si3.set_attr(attr_lower, val)
            self.history.append(attr, val, ts)

    # compatibility if called sync:
    def datachange_notification(self, node, val, data):
        # wrapper to schedule async if needed
        # For simple updates we can just run the logic directly if it doesn't await anything
        # But since set_attr and history.append are sync, we can just duplicate logic or call a common method
        nodeid = node.nodeid.to_string()
        attr = self.rev_map.get(nodeid)
        ts = datetime.utcnow()
        if attr:
            attr_lower = attr.lower()
            self.si3.set_attr(attr_lower, val)
            self.history.append(attr, val, ts)


async def monitor_subscription(opc_connector, attr_map: Dict[str, str], si3, history_repo, period_ms=500):
    handler = OpcSubscriptionHandler(attr_map, si3, history_repo)
    await opc_connector.create_subscription(period_ms, handler)
    await opc_connector.subscribe_to_nodes(list(attr_map.values()))
    # subscription runs until cancelled; keep coroutine alive
    while True:
        await asyncio.sleep(1.0)
        
async def monitor_polling(opc_connector, attr_map: Dict[str, str], si3, history_repo, interval_seconds: float):
    node_ids = list(attr_map.values())
    attrs    = list(attr_map.keys())
    delay    = max(0.001, float(interval_seconds))  # minimum 1ms, in seconds

    while True:
        try:
            values = await opc_connector.read_nodes(node_ids)
            ts = datetime.utcnow()
            # Update entity + history (same observable effect for Bokeh)
            for attr, val in zip(attrs, values):
                attr_lower = attr.lower()
                si3.set_attr(attr_lower, val)
                history_repo.append(attr, val, ts)
        except Exception as e:
            # Don't kill the loop if there's a temporary failure
            print(f"[polling] {type(e).__name__}: {e}")
        await asyncio.sleep(delay)