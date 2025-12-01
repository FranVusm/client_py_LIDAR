import asyncio
from asyncua import ua

async def _get_lider_node(connector, ns_idx):
    """
    Helper to get the LIDER object node.
    Tries 'LIDER' first (as per server_minimal.py), then 'Controls' as fallback.
    """
    try:
        # Try finding by BrowseName "SI3" in namespace ns_idx
        # Note: get_child expects BrowseNames. 
        # If the server created it with add_object(idx, "SI3"), the BrowseName is 2:SI3
        return await connector.client.nodes.objects.get_child([f"{ns_idx}:LIDER"])
    except Exception:
        try:
            return await connector.client.nodes.objects.get_child([f"{ns_idx}:Controls"])
        except Exception as e:
            raise RuntimeError(f"Could not find LIDER or Controls object in namespace {ns_idx}: {e}")

async def serv_fixed(connector, ns_idx):
    """Switch server to FIXED mode."""
    node = await _get_lider_node(connector, ns_idx)
    # Method NodeId defined in server: ns=idx;s=ServFixed
    return await node.call_method(f"ns={ns_idx};s=ServFixed")

async def serv_random(connector, ns_idx):
    """Switch server to RANDOM mode."""
    node = await _get_lider_node(connector, ns_idx)
    return await node.call_method(f"ns={ns_idx};s=ServRandom")

async def serv_out_of_range(connector, ns_idx):
    """Switch server to OUT_OF_RANGE mode."""
    node = await _get_lider_node(connector, ns_idx)
    return await node.call_method(f"ns={ns_idx};s=ServOutOfRange")

async def update_time(connector, ns_idx, heartbeat):
    """Update heartbeat/rate."""
    node = await _get_lider_node(connector, ns_idx)
    return await node.call_method(f"ns={ns_idx};s=update_time", int(heartbeat))

async def change_fix_val(connector, ns_idx, node_name, value):
    """Change a fixed value for a specific node."""
    node = await _get_lider_node(connector, ns_idx)
    return await node.call_method(f"ns={ns_idx};s=change_fix_val", node_name, value)

async def method_cmd(connector, ns_idx, node_name):
    """
    Read a node value by name.
    Assumes the NodeId is ns=idx;s=node_name
    """
    # node = await _get_lider_node(connector, ns_idx)
    # return await node.call_method(f"ns={ns_idx};s={ NodeID}")
    node_id = f"ns={ns_idx};s={node_name}"
    node = connector.client.get_node(node_id)
    return await node.read_value()
