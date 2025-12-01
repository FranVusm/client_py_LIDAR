# src/infrastructure/opcua_connector.py
import asyncio
from asyncua import Client, ua, Node
from typing import List, Any

class OpcUaConnector:
    def __init__(self, opc_url: str, timeout: int = 5_000, security_string: str = None):
        self.url = opc_url
        self._client = Client(self.url, timeout=timeout/1000.0)
        self.security_string = security_string
        self._subscription = None
        self._sub_handler = None
        self._lock = asyncio.Lock()  # necessary for disconnect and to avoid race conditions

    @property
    def client(self) -> Client:
        return self._client

    async def connect(self):
        if self.security_string:
            await self._client.set_security_string(self.security_string)
        await self._client.connect()

    async def disconnect(self):
        async with self._lock:
            if self._subscription is not None:
                try:
                    await self._subscription.delete()
                except Exception:
                    pass
                finally:
                    self._subscription = None
                    self._sub_handler = None
            if self._client is not None:
                try:
                    await self._client.disconnect()
                finally:
                    pass  # don't set to None to avoid breaking flows that reuse _client

    def _ensure_connected(self):
        # Defensive version: don't depend on .session (doesn't exist in some versions)
        if self._client is None:
            raise RuntimeError("OPC UA not connected (client=None)")
        # If you want to be stricter, you could try a light ping here.

    async def read_node(self, node_id: str):
        self._ensure_connected()
        node = self._client.get_node(node_id)
        return await node.read_value()

    async def read_nodes(self, node_ids: List[str]):
        self._ensure_connected()
        nodes = [self._client.get_node(nid) for nid in node_ids]
        return await asyncio.gather(*(n.read_value() for n in nodes))

    async def write_node(self, node_id: str, value: Any, variant_type=None):
        self._ensure_connected()
        node = self._client.get_node(node_id)
        if variant_type is not None:
            val = ua.Variant(value, variant_type)
            return await node.write_value(val)
        else:
            return await node.write_value(value)

    # --------- SUBSCRIPTION (no behavior changes) ----------
    async def create_subscription(self, period_ms: int, handler):
        if self._subscription:
            await self._subscription.delete()
        self._sub_handler = handler
        self._subscription = await self._client.create_subscription(period_ms, handler)
        return self._subscription

    async def subscribe_to_nodes(self, node_ids: List[str]):
        if not self._subscription:
            raise RuntimeError("subscription not created; call create_subscription first")
        nodes = [self._client.get_node(nid) for nid in node_ids]
        handles = []
        for n in nodes:
            h = await self._subscription.subscribe_data_change(n)
            handles.append(h)
        return handles
    # ----------------------------------------------------------------

   
    # src/infrastructure/opcua_connector.py

    # src/infrastructure/opcua_connector.py

    # src/infrastructure/opcua_connector.py

    async def call_controls_method(self, ns_idx: int, method_name: str, *args):
        """
        Calls a method under 'Controls' by resolving the real NodeId:
        1. Gets 'Controls' by its BrowseName (e.g.: "2:Controls").
        2. Enumerates its children (HasComponent) and filters those that are Methods.
        3. Compares the BrowseName.Name of each method (case-insensitive).
        4. Calls the method using the specific NodeId found.
        """
        self._ensure_connected()
        controls_node = None
        try:
            # 1) Get the Controls object by its BrowseName
            controls_node = await self.client.nodes.objects.get_child([f"{ns_idx}:Controls"])

            # 2) Enumerate components and filter methods (Your original logic)
            refs = await controls_node.get_references(ua.ObjectIds.HasComponent, direction=ua.BrowseDirection.Forward)
            target_method_node = None
            names_seen = []

            for r in refs:
                node = self.client.get_node(r.NodeId)
                
                if await node.read_node_class() != ua.NodeClass.Method:
                    continue
                
                # ===== THE CORRECTED LINE IS HERE! =====
                bn = await node.read_browse_name()
                # ======================================

                names_seen.append(bn.to_string())
                
                # Compare only .Name (ignore ns) and case-insensitive
                if (bn.Name or "").strip().lower() == method_name.strip().lower():
                    target_method_node = node
                    break # Found the method

            if target_method_node is None:
                lista = ", ".join(sorted(names_seen)) if names_seen else "(no published methods)"
                raise RuntimeError(
                    f"Method '{method_name}' not found under {controls_node.nodeid}. "
                    f"Available: {lista}"
                )

            # 3) Call using the real NodeId of the method (e.g.: ns=2;i=115)
            #    (This was the key part of your original logic)
            return await controls_node.call_method(target_method_node.nodeid, *args)

        except Exception as e:
            # Corrected debug block
            node_id_str = str(controls_node.nodeid) if controls_node else "Controls(not found)"
            print(f"[Debug] call_controls_method logic failed at {node_id_str} for {method_name}: {type(e).__name__}: {e}")
            raise e

