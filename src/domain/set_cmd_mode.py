# src/domain/set_cmd_mode.py
from typing import Any
from asyncua import ua

# ============================================================================
# Setter functions for OPC UA connection (LIDAR)
# ============================================================================

# --- Setters ---

async def set_laser_enable(connector, value: Any):
    """Sets lidar_set_laser_enable (Boolean)"""
    await connector.write_node("ns=2;s=lidar_set_laser_enable", value, ua.VariantType.Boolean)

async def set_hv_enable(connector, value: Any):
    """Sets lidar_set_hv_enable (Boolean)"""
    await connector.write_node("ns=2;s=lidar_set_hv_enable", value, ua.VariantType.Boolean)

async def set_laser_prf(connector, value: Any):
    """Sets lidar_set_laser_prf (Int32)"""
    await connector.write_node("ns=2;s=lidar_set_laser_prf", value, ua.VariantType.Int32)

async def set_target_az(connector, value: Any):
    """Sets lidar_set_target_az"""
    await connector.write_node("ns=2;s=lidar_set_target_az", value, ua.VariantType.Double)

async def set_target_el(connector, value: Any):
    """Sets lidar_set_target_el"""
    await connector.write_node("ns=2;s=lidar_set_target_el", value, ua.VariantType.Double)

async def set_scan_speed_az(connector, value: Any):
    """Sets lidar_set_scan_speed_az"""
    await connector.write_node("ns=2;s=lidar_set_scan_speed_az", value, ua.VariantType.Double)

async def set_scan_speed_el(connector, value: Any):
    """Sets lidar_set_scan_speed_el"""
    await connector.write_node("ns=2;s=lidar_set_scan_speed_el", value, ua.VariantType.Double)

async def set_scan_mode_select(connector, value: Any):
    """Sets lidar_set_scan_mode_select (Int32)"""
    await connector.write_node("ns=2;s=lidar_set_scan_mode_select", value, ua.VariantType.Int32)

async def set_bin_width(connector, value: Any):
    """Sets lidar_set_bin_width"""
    await connector.write_node("ns=2;s=lidar_set_bin_width", value, ua.VariantType.Double)

async def set_accumulation_pulses(connector, value: Any):
    """Sets lidar_set_accumulation_pulses (Int32)"""
    await connector.write_node("ns=2;s=lidar_set_accumulation_pulses", value, ua.VariantType.Int32)

async def set_raster_width(connector, value: Any):
    """Sets lidar_set_raster_width"""
    await connector.write_node("ns=2;s=lidar_set_raster_width", value, ua.VariantType.Double)

async def set_raster_height(connector, value: Any):
    """Sets lidar_set_raster_height"""
    await connector.write_node("ns=2;s=lidar_set_raster_height", value, ua.VariantType.Double)

async def set_cone_angle(connector, value: Any):
    """Sets lidar_set_cone_angle"""
    await connector.write_node("ns=2;s=lidar_set_cone_angle", value, ua.VariantType.Double)

async def set_cmd_home(connector, value: Any):
    """Sets lidar_set_cmd_home (Boolean)"""
    await connector.write_node("ns=2;s=lidar_set_cmd_home", value, ua.VariantType.Boolean)

async def set_cmd_park(connector, value: Any):
    """Sets lidar_set_cmd_park (Boolean)"""
    await connector.write_node("ns=2;s=lidar_set_cmd_park", value, ua.VariantType.Boolean)

async def set_start_acquisition(connector, value: Any):
    """Sets lidar_set_start_acquisition (Boolean)"""
    await connector.write_node("ns=2;s=lidar_set_start_acquisition", value, ua.VariantType.Boolean)


# --- Cmd ---

async def cmd_updatestop(connector, value: Any):
    """Sets lidar_updatestop (Boolean)"""
    await connector.write_node("ns=2;s=lidar_updatestop", value, ua.VariantType.Boolean)

async def cmd_updateresume(connector, value: Any):
    """Sets lidar_updateresume (Boolean)"""
    await connector.write_node("ns=2;s=lidar_updateresume", value, ua.VariantType.Boolean)

async def cmd_simul_on(connector, value: Any):
    """Sets lidar_simul_on (Boolean)"""
    await connector.write_node("ns=2;s=lidar_simul_on", value, ua.VariantType.Boolean)

async def cmd_simul_off(connector, value: Any):
    """Sets lidar_simul_off (Boolean)"""
    await connector.write_node("ns=2;s=lidar_simul_off", value, ua.VariantType.Boolean)

async def cmd_servershutdown(connector, value: Any):
    """Sets lidar_servershutdown (Boolean)"""
    await connector.write_node("ns=2;s=lidar_servershutdown", value, ua.VariantType.Boolean)

async def cmd_error_info(connector, value: Any):
    """Sets lidar_error_info (Boolean)"""
    await connector.write_node("ns=2;s=lidar_error_info", value, ua.VariantType.Boolean)

async def cmd_error_reset(connector, value: Any):
    """Sets lidar_error_reset (Boolean)"""
    await connector.write_node("ns=2;s=lidar_error_reset", value, ua.VariantType.Boolean)


# --- Mode ---

async def mode_go_loaded(connector, value: Any):
    """Sets lidar_go_loaded (Boolean)"""
    await connector.write_node("ns=2;s=lidar_go_loaded", value, ua.VariantType.Boolean)

async def mode_go_standby(connector, value: Any):
    """Sets lidar_go_standby (Boolean)"""
    await connector.write_node("ns=2;s=lidar_go_standby", value, ua.VariantType.Boolean)

async def mode_go_online(connector, value: Any):
    """Sets lidar_go_online (Boolean)"""
    await connector.write_node("ns=2;s=lidar_go_online", value, ua.VariantType.Boolean)

async def mode_go_maintenace(connector, value: Any):
    """Sets lidar_go_maintenace (Boolean)"""
    await connector.write_node("ns=2;s=lidar_go_maintenace", value, ua.VariantType.Boolean)
