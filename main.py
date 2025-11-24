# src/main.py
import asyncio
import threading
from datetime import datetime
from typing import Optional
import socket

import sys
import os

# Add src to sys.path to ensure imports work even if package is not installed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import os
from domain.entity import LIDER
from infrastructure.opcua_connector import OpcUaConnector
from infrastructure.memory_history_repo import MemoryHistoryRepo
from application.use_cases.monitor import monitor_subscription, monitor_polling  
from application.use_cases.controls import (
    serv_fixed, serv_random, change_fix_val, update_time, serv_out_of_range, method_cmd
)
from domain.dto import (
    get_state, get_status, get_heartbeat, get_app_name, 
    get_elastic_channel_355_nm, get_error_number, get_verbose_status
)

from tornado.ioloop import IOLoop
from bokeh.server.server import Server
from presentation.bokeh_app import make_bokeh_app
from typing import get_type_hints, get_origin, get_args


# ===== Config =====
OPC_URL_DEFAULT = os.getenv("opcua_url")
NS_IDX = 2  # namespace of the "Controls" object/methods

# ===== Helper to filter graphable variables =====
def get_graphable_attrs(all_attrs: list) -> list:
    """
    Filters variables that are graphable (bool, int, float) based on types defined in LIDER.
    """
    from typing import Union
    # Get type hints from the LIDER class
    type_hints = get_type_hints(LIDER)
    graphable_types = {bool, int, float}
    graphable_attrs = []
    
    for attr_name in all_attrs:
        # Check against lowercase attribute name in LIDER
        attr_lower = attr_name.lower()
        if attr_lower in type_hints:
            attr_type = type_hints[attr_lower]
            # Handle Optional[T] or Union[T, None] -> extract inner type
            origin = get_origin(attr_type)
            if origin is not None:  # It's a generic type like Optional or Union
                args = get_args(attr_type)
                if args:
                    # For Optional[T] or Union[T, None], get types that are not None
                    inner_types = [arg for arg in args if arg is not type(None)]
                    # Check if any of the inner types is bool, int or float
                    if any(t in graphable_types for t in inner_types):
                        graphable_attrs.append(attr_name)
            else:
                # Direct type (shouldn't happen with Optional, but just in case)
                if attr_type in graphable_types:
                    graphable_attrs.append(attr_name)
    
    return graphable_attrs

def put_in_background():
    """
    Puts the process in background by redirecting stdin to free the terminal.
    Returns the process PID.
    """
    import sys
    
    pid = os.getpid()
    
    # Redirect stdin to /dev/null or NUL to free the terminal
    try:
        if sys.platform == 'win32':
            null_device = 'NUL'
        else:
            null_device = '/dev/null'
        
        # Close current stdin and open null device
        try:
            if not sys.stdin.closed:
                sys.stdin.close()
        except (AttributeError, OSError):
            pass
        
        # Open /dev/null as new stdin
        sys.stdin = open(null_device, 'r')
        
        # Also redirect at OS level if possible
        try:
            if hasattr(os, 'dup2'):
                null_fd = os.open(null_device, os.O_RDONLY)
                os.dup2(null_fd, 0)  # Redirect stdin (fd 0)
                os.close(null_fd)
        except Exception:
            pass
        
    except Exception:
        pass
    
    return pid

# domain_attr -> nodeid
ATTR_MAP = {
    # --- Basic Status & Info ---
    "STATE": "ns=2;s=lidar_get_state",
    "STATUS": "ns=2;s=lidar_get_status",
    "APP_NAME": "ns=2;s=lidar_get_serverApplicationName",
    "OPCUA_PORT": "ns=2;s=lidar_get_opcuaPort",
    "WEB_PORT": "ns=2;s=lidar_get_webPort",
    "APP_START_TIME": "ns=2;s=lidar_get_startTime",
    "SERIAL_NUMBER": "ns=2;s=lidar_get_serialNumber",
    "TABLE_FILE_NAME": "ns=2;s=lidar_get_fileNameTable",
    "PROSYS_SDK_VERSION": "ns=2;s=lidar_get_sdkversion",
    "CURRENT_SESSION_NUMBER": "ns=2;s=lidar_get_currentsessionnumber",
    "SESSIONS_NAME": "ns=2;s=lidar_get_sessionsname",
    "RANDOM_GENERATOR_CODE": "ns=2;s=lidar_get_randomgeneratorcode",
    "VERBOSE_STATUS": "ns=2;s=lidar_get_verbosestatus",
    "UPDATETIME": "ns=2;s=lidar_get_updatetime",
    "ISOTSTAMP": "ns=2;s=lidar_get_isotstamp",
    "HEARTBEAT": "ns=2;s=heartbeat",

    # --- Errors ---
    "ERROR_NUMBER": "ns=2;s=lidar_get_error_number",
    "ERROR_INFORMATION": "ns=2;s=lidar_get_error_information",
    "ERROR_RECOVERING": "ns=2;s=lidar_get_error_recovering",
    "ERROR_NUMBER_RECOVERED": "ns=2;s=lidar_get_error_number_recovered",
    "ERROR_NUMBER_OUTOFRANGE": "ns=2;s=lidar_get_error_number_outofrange",

    # --- Raw Channels ---
    "ELASTIC_CHANNEL_355_NM": "ns=2;s=lidar_get_ElasticChannel355Nm",
    "ELASTIC_CHANNEL_532_NM": "ns=2;s=lidar_get_ElasticChannel532Nm",
    "ELASTIC_CHANNEL_1064_NM": "ns=2;s=lidar_get_ElasticChannel1064Nm",
    "RAMAN_CHANNEL_N2_387_NM": "ns=2;s=lidar_get_RamanChannelN2387Nm",
    "RAMAN_CHANNEL_H2O": "ns=2;s=lidar_get_RamanChannelH2o",
    "RAMAN_RANGE_SIGNAL_COUNTS": "ns=2;s=lidar_get_RamanRangeSignalCounts",
    "STATISTICAL_ERROR_PER_BIN": "ns=2;s=lidar_get_StatisticalErrorPerBin",
    "INTEGRATION_TIME": "ns=2;s=lidar_get_IntegrationTime",
    "CO_POLAR_355_NM": "ns=2;s=lidar_get_CoPolar355Nm",
    "CROSS_POLAR_355_NM": "ns=2;s=lidar_get_CrossPolar355Nm",
    "CO_POLAR_532_NM": "ns=2;s=lidar_get_CoPolar532Nm",
    "CROSS_POLAR_532_NM": "ns=2;s=lidar_get_CrossPolar532Nm",
    "DEPOLARISATION_RATIO_PROFILE": "ns=2;s=lidar_get_DepolarisationRatioProfile",

    # --- Derived Parameters ---
    "BACKSCATTER_COEFFICIENT_BETA_Z": "ns=2;s=lidar_get_BackscatterCoefficientBetaZ",
    "EXTINCTION_COEFFICIENT_ALPHA_Z": "ns=2;s=lidar_get_ExtinctionCoefficientAlphaZ",
    "AEROSOL_OPTICAL_DEPTH": "ns=2;s=lidar_get_AerosolOpticalDepth",
    "LIDAR_RATIO_S_Z": "ns=2;s=lidar_get_LidarRatioSZ",
    "HUMIDITY_PROFILE_H2O": "ns=2;s=lidar_get_HumidityProfileH2o",
    "PBL_HEIGHT": "ns=2;s=lidar_get_PblHeight",
    "CLOUD_BASE_HEIGHT": "ns=2;s=lidar_get_CloudBaseHeight",
    "SNR_PER_BIN": "ns=2;s=lidar_get_SnrPerBin",

    # --- Metadata & Quality Indicators ---
    "TIMESTAMP_UTC": "ns=2;s=lidar_get_Timestamp_Utc",
    "INTEGRATION_ACCUMULATION_TIME": "ns=2;s=lidar_get_IntegrationAccumulationTime",
    "NUMBER_OF_ACCUMULATED_PULSES": "ns=2;s=lidar_get_NumberOfAccumulatedPulses",
    "VERTICAL_RESOLUTION_BIN_SIZE": "ns=2;s=lidar_get_VerticalResolutionBinSize",
    "TEMPORAL_RESOLUTION": "ns=2;s=lidar_get_TemporalResolution",
    "GLOBAL_SNR": "ns=2;s=lidar_get_GlobalSnr",
    "QUALITY_FLAGS": "ns=2;s=lidar_get_QualityFlags",
    "INTERNAL_TEMPERATURES": "ns=2;s=lidar_get_InternalTemperatures",
    "LASER_READINGS_ENERGY_VOLTAGE_PRF": "ns=2;s=lidar_get_LaserReadingsEnergyVoltagePrf",

    # --- Pre-processed Products ---
    "AOD_TIME_SERIES": "ns=2;s=lidar_get_AodTimeSeries",
    "AVERAGED_INTERVAL_PROFILES": "ns=2;s=lidar_get_AveragedIntervalProfiles",
    "NETCDF_ASCII_GRID_FILES": "ns=2;s=lidar_get_NetcdfAsciiGridFiles",
    "RANGE_TIME_IMAGES": "ns=2;s=lidar_get_RangeTimeImages",
    "ASH_CLOUD_AUTOMATIC_DETECTION": "ns=2;s=lidar_get_AshCloudAutomaticDetection",

    # --- Pointing & Scanning (Type & Accuracy) ---
    "MOTORISED_2_AXIS_MOUNT": "ns=2;s=lidar_get_Motorised2AxisMount",
    "THREE_D_SCANNING_CAPABILITY": "ns=2;s=lidar_get_ThreeDScanningCapability",
    "AZIMUTH_RANGE_0_360_DEG": "ns=2;s=lidar_get_AzimuthRange0360Deg",
    "ELEVATION_RANGE_NEG5_90_DEG": "ns=2;s=lidar_get_ElevationRange_590Deg",
    "POINTING_ACCURACY": "ns=2;s=lidar_get_PointingAccuracy",
    "ANGULAR_SPEED_CONFIGURABLE": "ns=2;s=lidar_get_AngularSpeedConfigurable",
    "MODE_STARE_FIXED": "ns=2;s=lidar_get_ModeStareFixed",
    "MODE_RASTER_SCAN": "ns=2;s=lidar_get_ModeRasterScan",
    "MODE_CONE_SCAN": "ns=2;s=lidar_get_ModeConeScan",
    "MODE_VOLUME_SCAN": "ns=2;s=lidar_get_ModeVolumeScan",
    "ANGULAR_STEP_PER_BIN": "ns=2;s=lidar_get_AngularStepPerBin",
    "INTEGRATION_TIME_PER_POSITION": "ns=2;s=lidar_get_IntegrationTimePerPosition",

    # --- Remote Control & Commands ---
    "ETHERNET_API_GUI_CONTROL": "ns=2;s=lidar_get_EthernetApiGuiControl",
    "CMD_SET_AZ": "ns=2;s=lidar_get_CmdSetAz",
    "CMD_SET_EL": "ns=2;s=lidar_get_CmdSetEl",
    "CMD_HOME": "ns=2;s=lidar_get_CmdHome",
    "CMD_PARK": "ns=2;s=lidar_get_CmdPark",
    "CMD_START_SCAN": "ns=2;s=lidar_get_CmdStartScan",
    "TELEMETRY_STATUS_POSITION_ENCODER": "ns=2;s=lidar_get_TelemetryStatusPositionEncoder",
    "COMMAND_LATENCY": "ns=2;s=lidar_get_CommandLatency",
    "ENCODER_POSITION_CONFIRMATION": "ns=2;s=lidar_get_EncoderPositionConfirmation",
    "DIRECT_POINTING_COMMANDS": "ns=2;s=lidar_get_DirectPointingCommands",
    "POINTING_TOLERANCE": "ns=2;s=lidar_get_PointingTolerance",
    "POINTING_VERIFICATION": "ns=2;s=lidar_get_PointingVerification",
    "MEASUREMENT_STRATEGY_BY_POINTING": "ns=2;s=lidar_get_MeasurementStrategyByPointing",
    "POSITION_QUALITY_FLAGS": "ns=2;s=lidar_get_PositionQualityFlags",

    # --- Safety ---
    "SAFETY_INTERLOCKS": "ns=2;s=lidar_get_SafetyInterlocks",
    "NO_GO_ZONES": "ns=2;s=lidar_get_NoGoZones",
    "HUMAN_PRESENCE_LOCKOUT": "ns=2;s=lidar_get_HumanPresenceLockout",
    "DAY_NIGHT_MODES": "ns=2;s=lidar_get_DayNightModes",

    # --- Instrument Measurement State ---
    "MEASUREMENT_TIME_UTC": "ns=2;s=lidar_get_MeasurementTimeUtc",
    "INTEGRATION_SECONDS": "ns=2;s=lidar_get_IntegrationSeconds",
    "LASER_WAVELENGTH_NM": "ns=2;s=lidar_get_LaserWavelengthNm",
    "CHANNEL_ID": "ns=2;s=lidar_get_ChannelId",
    "RANGE_M": "ns=2;s=lidar_get_RangeM",
    "SIGNAL_COUNTS": "ns=2;s=lidar_get_SignalCounts",
    "SIGNAL_ERROR": "ns=2;s=lidar_get_SignalError",
    "BACKSCATTER_COEF_M_SR": "ns=2;s=lidar_get_BackscatterCoefMSr",
    "EXTINCTION_COEF_KM_1": "ns=2;s=lidar_get_ExtinctionCoefKm1",
    "DEPOLARIZATION_RATIO": "ns=2;s=lidar_get_DepolarizationRatio",
    "WATER_VAPOUR_MIXING_RATIO_G_PER_KG": "ns=2;s=lidar_get_WaterVapourMixingRatioGPerKg",
    "CLOUD_BASE_HEIGHT_M": "ns=2;s=lidar_get_CloudBaseHeightM",
    "PBL_HEIGHT_M": "ns=2;s=lidar_get_PblHeightM",
    "POINTING_AZ_DEG": "ns=2;s=lidar_get_PointingAzDeg",
    "POINTING_EL_DEG": "ns=2;s=lidar_get_PointingElDeg",
    "POINTING_TARGET_AZ_DEG": "ns=2;s=lidar_get_PointingTargetAzDeg",
    "POINTING_TARGET_EL_DEG": "ns=2;s=lidar_get_PointingTargetElDeg",
    "POINTING_STATUS": "ns=2;s=lidar_get_PointingStatus",
    "POINTING_ACCURACY_DEG": "ns=2;s=lidar_get_PointingAccuracyDeg",
    "SCAN_MODE": "ns=2;s=lidar_get_ScanMode",
    "DEVICE_STATUS": "ns=2;s=lidar_get_DeviceStatus",
    "FILE_FORMAT_VERSION": "ns=2;s=lidar_get_FileFormatVersion",
}

# ===== Embedded Bokeh =====
_bokeh_started = False
def start_bokeh(history_repo, preferred_port: int = 5010, auto_open: bool = False):
    import threading
    import webbrowser
    from contextlib import closing

    def _get_local_ip() -> str:
        """Gets the local IP (non-loopback) of the host."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))  # use external destination without sending traffic
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

    def _find_free_port(start_port: int, attempts: int = 5) -> int:
        for p in range(start_port, start_port + attempts):
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.bind(("0.0.0.0", p))  # listen on all interfaces
                    return p
                except OSError:
                    continue
        raise OSError(f"Could not find free port between {start_port} and {start_port + attempts - 1}")

    global _bokeh_started
    

    try:
        port = _find_free_port(preferred_port)
    except OSError as e:
        print(f"[Bokeh] {e}")
        return

    host_ip = _get_local_ip()  # ← gets host IP

    def bk_worker():
        import asyncio
        from tornado.ioloop import IOLoop
        from bokeh.server.server import Server
        from presentation.bokeh_app import make_bokeh_app

        asyncio.set_event_loop(asyncio.new_event_loop())
        io_loop = IOLoop.current()
        
        # Filter only graphable variables (bool, int, float)
        graphable_attrs = get_graphable_attrs(list(ATTR_MAP.keys()))
        if not graphable_attrs:
            # Fallback to heartbeat if no graphable variables
            graphable_attrs = ["HEARTBEAT"] if "HEARTBEAT" in ATTR_MAP else []
        
        server = Server(
            {'/bokeh_app': lambda doc: make_bokeh_app(doc, history_repo, graphable_attrs)},
            io_loop=io_loop,
            address=host_ip,
            port=port,
            allow_websocket_origin=[
                f"{host_ip}:{port}", f"localhost:{port}", f"127.0.0.1:{port}"
            ],
        )
        server.start()
        io_loop.start()

    threading.Thread(target=bk_worker, daemon=True).start()
    _bokeh_started = True

    url = f"http://{host_ip}:{port}/bokeh_app"
    if _bokeh_started:
        print(f"Bokeh already started at: {url}")
        return
    print(f"Bokeh started → {url}")
    if auto_open:
        try:
            webbrowser.open(url, new=2)
        except Exception:
            pass

#1) Fixed Server      (call: ServFixed)
#2) Random Server     (call: ServRandom)
#3) Fix Value         (call: change_fix_val)
#4) Out of range Server (call: ServOutOfRange)
#5) Update time       (call: update_time)
# ===== Helpers =====
MENU = """
================= SI3 OPC UA =================
1) Show Graph (Bokeh)
2) Call generic method (call: <name>)
3) Test OPC UA getters (usage example)
b) Put in background (recover terminal)
q) Exit
==============================================
Option: """

def _auto_convert(s: str):
    t = s.strip()
    l = t.lower()
    if l == "true": return True
    if l == "false": return False
    try: return int(t)
    except ValueError: pass
    try: return float(t)
    except ValueError: pass
    return t

# ===== Main loop =====
async def run(opc_url: str, polling_rate_seconds: float | None = None):
    lider = LIDER()
    history = MemoryHistoryRepo(retention_minutes=10)
    connector = None
    sub_task = None
    loop = asyncio.get_running_loop()
    start_bokeh(history)
    
    async def connect_and_start_monitoring():
        nonlocal connector, sub_task
        try:
            # Disconnect if there's a previous connection
            if connector is not None:
                try:
                    if sub_task is not None:
                        sub_task.cancel()
                        try:
                            await sub_task
                        except asyncio.CancelledError:
                            pass
                    await connector.disconnect()
                except Exception:
                    pass
            
            # Create new connection
            connector = OpcUaConnector(opc_url)
            await connector.connect()
            
            # Start monitoring
            if polling_rate_seconds is not None:
                print(f"[Mode] POLLING for history/Bokeh @ {polling_rate_seconds} seconds")
                sub_task = asyncio.create_task(
                    monitor_polling(connector, ATTR_MAP, lider, history, interval_seconds=polling_rate_seconds)
                )
            else:
                print(f"[Mode] OPC UA SUBSCRIPTION for history/Bokeh (period_ms=500)")
                sub_task = asyncio.create_task(
                    monitor_subscription(connector, ATTR_MAP, lider, history, period_ms=500)
                )
            
            print(f"Connected to {opc_url}.")
            return True
        except Exception as e:
            print(f"[ERROR] Connection error: {type(e).__name__}: {e}")
            return False
    
    # Task to periodically verify connection
    connection_check_task = None
    stop_reconnect = False
    
    async def check_connection_periodically():
        nonlocal connected
        while not stop_reconnect:
            await asyncio.sleep(5)  # Check every 5 seconds
            if connected and connector is not None:
                try:
                    # Try a simple operation to verify connection
                    await connector.read_node(list(ATTR_MAP.values())[0])
                except Exception:
                    # Connection lost
                    if connected:
                        print(f"[DISCONNECTION] Lost connection to {opc_url}")
                        connected = False
                        if sub_task is not None:
                            sub_task.cancel()
                            try:
                                await sub_task
                            except asyncio.CancelledError:
                                pass
    
    async def reconnect_loop():
        nonlocal connected, in_background
        while not stop_reconnect:
            if not connected:
                # Wait 10 seconds before retrying
                await asyncio.sleep(10)
                if not stop_reconnect:
                    print(f"[RECONNECTION] Attempting to reconnect to {opc_url}...")
                    was_in_background = in_background
                    connected = await connect_and_start_monitoring()
                    if connected and was_in_background:
                        # If it was in background and reconnected, it may have taken the terminal
                        print(f"[RECONNECTION] Reconnection successful. If the terminal was taken, use 'bg' to recover it.")
            else:
                await asyncio.sleep(1)  # If connected, check less frequently
    
    # Initial connection
    connected = await connect_and_start_monitoring()
    if not connected:
        print(f"[RECONNECTION] Attempting to reconnect in 10 seconds...")
    
    # Start verification and reconnection tasks
    connection_check_task = asyncio.create_task(check_connection_periodically())
    reconnect_task = asyncio.create_task(reconnect_loop())
    
    # Variable to control if in background mode
    in_background = False
    
    try:
        while True:
            if not connected:
                # If not connected, wait a bit
                await asyncio.sleep(0.1)
                continue
            
            # If in background, don't try to read from stdin
            if in_background:
                await asyncio.sleep(1)
                continue
            
            try:
                choice = await loop.run_in_executor(None, input, MENU)
                choice = choice.strip().lower()
                
                try:
                    if choice == "1":
                        start_bokeh(history)

                    elif choice == "2":
                        cmd_name = await loop.run_in_executor(None, input, "Method name to call: ")
                        res = await method_cmd(connector, NS_IDX, cmd_name.strip())
                        print(f"{cmd_name} → {res}")

                    elif choice == "3":
                        # Example usage of OPC UA getters
                        print("\n[GETTERS] Testing getter functions with OPC UA connection...")
                        try:
                            # Examples of different variable types
                            state = await get_state(connector)
                            status = await get_status(connector)
                            heartbeat = await get_heartbeat(connector)
                            app_name = await get_app_name(connector)
                            elastic_355 = await get_elastic_channel_355_nm(connector)
                            error_num = await get_error_number(connector)
                            verbose = await get_verbose_status(connector)
                            
                            print(f"  State: {state}")
                            print(f"  Status: {status}")
                            print(f"  Heartbeat: {heartbeat}")
                            print(f"  App Name: {app_name}")
                            print(f"  Elastic Ch 355nm: {elastic_355}")
                            print(f"  Error Number: {error_num}")
                            print(f"  Verbose Status: {verbose}")
                            print("\n[GETTERS] Example completed. You can copy these functions to your code.")
                            print("[GETTERS] See src/domain/dto.py for all available functions.\n")
                        except Exception as e:
                            print(f"[ERROR] Error using getters: {type(e).__name__}: {e}")

                    elif choice in ("b", "bg", "background"):
                        # Put in background
                        pid = put_in_background()
                        in_background = True
                        print(f"\n[BACKGROUND] To recover the terminal and put the process in background:")
                        print(f"[BACKGROUND]   1. Press Ctrl+Z (recovers the terminal)")
                        print(f"[BACKGROUND]   2. Then type 'bg' (sends the process to background)")
                        print(f"[BACKGROUND]   3. The graph will keep running only if you do 'bg'")
                        print(f"\n[BACKGROUND] Process PID: {pid}")
                        print(f"[BACKGROUND] To stop the process: kill {pid}")
                        print("[BACKGROUND] The graph and connections will remain active after 'bg'.\n")
                        continue

                    elif choice in ("q", "quit", "exit"):
                        print("Exiting…")
                        break
                    else:
                        print("Invalid option.")
                except Exception as e:
                    print(f"[ERROR] OPC-UA call failed: {type(e).__name__}: {e}")
                    # If it fails, mark as disconnected to retry
                    connected = False
                    
            except (EOFError, OSError, ValueError):
                # stdin closed or unavailable - may be in background
                # Don't change in_background, just continue
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"[ERROR] Unexpected error: {type(e).__name__}: {e}")
                connected = False

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        stop_reconnect = True
        if connection_check_task is not None:
            connection_check_task.cancel()
            try:
                await connection_check_task
            except asyncio.CancelledError:
                pass
        if reconnect_task is not None:
            reconnect_task.cancel()
            try:
                await reconnect_task
            except asyncio.CancelledError:
                pass
        if sub_task is not None:
            sub_task.cancel()
            try:
                await sub_task
            except asyncio.CancelledError:
                pass
        if connector is not None:
            try:
                await connector.disconnect()
            except Exception:
                pass
        print("Connection closed.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SI3 OPC UA Client",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "opc_url",
        type=str,
        help="OPC UA server URL (required, e.g.: opc.tcp://localhost:4840)"
    )
    parser.add_argument(
        "--RATE",
        type=float,
        default=None,
        metavar="SECONDS",
        help="Polling rate in seconds (float, e.g.: 0.5, 1, 2.5). If not specified, uses OPC UA subscription"
    )
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run(args.opc_url, polling_rate_seconds=args.RATE))
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

