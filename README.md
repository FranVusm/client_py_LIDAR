# SI3 OPC UA Python Client

A clean architecture OPC UA client for SI3 monitoring and history with Bokeh visualization.

## Table of Contents

- [Installation](#installation)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Usage](#usage)
- [Client Features](#client-features)
- [Getter Functions](#getter-functions)
- [Examples](#examples)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/FranVusm/client_py_LIDER.git
cd client_py_LIDER
```

## Virtual Environment Setup

It's recommended to use a virtual environment to isolate dependencies.

### Linux/Mac

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### Windows

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

### Step 2: Install Dependencies

Once the virtual environment is activated, install the package and its dependencies:

```bash
pip install -e .
```

This will install:
- `asyncua` - OPC UA client library
- `bokeh` - Interactive visualization library
- `tornado` - Web server for Bokeh
- `python-dotenv` - Environment variable management

## Usage

### Basic Usage

Run the client with the OPC UA server URL:

```bash
python main.py opc.tcp://localhost:4840
```

#### Secure mode

To use secure mode, add the following parameters:

```bash
python main.py opc.tcp://localhost:4840 --secure
```

### With Polling Mode

To use polling instead of subscriptions (useful for slower update rates):

```bash
python main.py opc.tcp://localhost:4840 --RATE 1.0
```

The `--RATE` parameter specifies the polling interval in seconds (e.g., 0.5, 1.0, 2.5).

#### Secure mode

To use secure mode, add the following parameters:

```bash
python main.py opc.tcp://localhost:4840 --RATE 1.0 --secure
```

### Interactive Menu

Once running, the client provides an interactive menu:

```
================= SI3 OPC UA =================
1) Show Graph (Bokeh)
2) Call generic method (call: <name>)
3) Test OPC UA getters (usage example)
4) Test OPC UA setters (usage example)
b) Put in background (recover terminal)
q) Exit
==============================================
Option:
```

**Menu Options:**
- **1** - Opens/refreshes the Bokeh web interface for real-time data visualization
- **2** - Calls a generic OPC UA method by name
- **3** - Demonstrates how to use the getter functions with example calls
- **4** - Demonstrates how to use the setter functions with example calls
- **b/bg/background** - Puts the process in background mode (frees the terminal)
- **q/quit/exit** - Exits the client

### Bokeh Visualization

The client automatically starts a Bokeh server when launched. Access the visualization at:
- `http://<your-ip>:5010/bokeh_app` (or the port shown in the console)

The Bokeh interface allows you to:
- Select multiple variables to graph
- Adjust the time window (1-60 minutes)
- View real-time sensor data
- Hide/show individual variables via legend clicks

## Client Features

### 1. OPC UA Connection Management
- Automatic connection and reconnection
- Connection health monitoring
- Support for subscriptions and polling modes

### 2. Real-time Monitoring
- **Subscription Mode** (default): Uses OPC UA subscriptions for efficient real-time updates (500ms period)
- **Polling Mode**: Periodic reads at specified intervals (useful for slower networks)

### 3. Data History
- In-memory history repository
- Configurable retention period (default: 10 minutes)
- Automatic data pruning

### 4. Interactive Visualization
- Bokeh-based web interface
- Multi-variable plotting
- Real-time updates
- Interactive controls (zoom, pan, reset)

### 5. Method Calling
- Generic method invocation
- Support for all methods under the "Controls" object
- Examples: `ServFixed`, `ServRandom`, `change_fix_val`, `update_time`, `ServOutOfRange`

## Getter Functions

### Location

All getter functions are located in:
```
src/domain/dto.py
```

### Available Getters

The client provides async getter functions for reading OPC UA node values. All getters follow the pattern:

```python
async def get_<attribute_name>(connector) -> Optional[<type>]:
    """Description"""
    return await connector.read_node("ns=2;s=si3_get_<attribute_name>")
```

### Available Getter Functions

#### Server Information
- `get_state(connector)` - Server state
- `get_status(connector)` - Server status
- `get_app_name(connector)` - Application name
- `get_opcua_port(connector)` - OPC UA port
- `get_web_port(connector)` - Web port
- `get_app_start_time(connector)` - Application start time
- `get_serial_number(connector)` - Serial number
- `get_prosys_sdk_version(connector)` - Prosys SDK version
- `get_current_session_number(connector)` - Current session number
- `get_sessions_name(connector)` - Sessions name
- `get_random_generator_code(connector)` - Random generator code
- `get_verbose_status(connector)` - Verbose status
- `get_updatetime(connector)` - Update time
- `get_isotstamp(connector)` - ISO timestamp
- `get_heartbeat(connector)` - Heartbeat counter
- `get_table_file_name(connector)` - Table file name

#### Error Information
- `get_error_number(connector)` - Error number
- `get_error_information(connector)` - Error information
- `get_error_recovering(connector)` - Error recovery status
- `get_error_number_recovered(connector)` - Recovered error number
- `get_error_number_outofrange(connector)` - Out of range error flag

#### Raw Channels
- `get_elastic_channel_355_nm(connector)` - Elastic Channel 355nm
- `get_elastic_channel_532_nm(connector)` - Elastic Channel 532nm
- `get_elastic_channel_1064_nm(connector)` - Elastic Channel 1064nm
- `get_raman_channel_n2_387_nm(connector)` - Raman Channel N2 387nm
- `get_raman_channel_h2o(connector)` - Raman Channel H2O
- `get_raman_range_signal_counts(connector)` - Raman Range Signal Counts
- `get_statistical_error_per_bin(connector)` - Statistical Error Per Bin
- `get_integration_time(connector)` - Integration Time
- `get_co_polar_355_nm(connector)` - Co-Polar 355nm
- `get_cross_polar_355_nm(connector)` - Cross-Polar 355nm
- `get_co_polar_532_nm(connector)` - Co-Polar 532nm
- `get_cross_polar_532_nm(connector)` - Cross-Polar 532nm
- `get_depolarisation_ratio_profile(connector)` - Depolarisation Ratio Profile

#### Derived Parameters
- `get_backscatter_coefficient_beta_z(connector)` - Backscatter Coefficient Beta Z
- `get_extinction_coefficient_alpha_z(connector)` - Extinction Coefficient Alpha Z
- `get_aerosol_optical_depth(connector)` - Aerosol Optical Depth
- `get_lidar_ratio_s_z(connector)` - Lidar Ratio S Z
- `get_humidity_profile_h2o(connector)` - Humidity Profile H2O
- `get_pbl_height(connector)` - PBL Height
- `get_cloud_base_height(connector)` - Cloud Base Height
- `get_snr_per_bin(connector)` - SNR Per Bin

#### Metadata & Quality Indicators
- `get_timestamp_utc(connector)` - Timestamp UTC
- `get_integration_accumulation_time(connector)` - Integration Accumulation Time
- `get_number_of_accumulated_pulses(connector)` - Number of Accumulated Pulses
- `get_vertical_resolution_bin_size(connector)` - Vertical Resolution Bin Size
- `get_temporal_resolution(connector)` - Temporal Resolution
- `get_global_snr(connector)` - Global SNR
- `get_quality_flags(connector)` - Quality Flags
- `get_internal_temperatures(connector)` - Internal Temperatures
- `get_laser_readings_energy_voltage_prf(connector)` - Laser Readings

#### Pointing & Scanning
- `get_motorised_2_axis_mount(connector)` - Motorised 2-Axis Mount
- `get_three_d_scanning_capability(connector)` - 3D Scanning Capability
- `get_azimuth_range_0_360_deg(connector)` - Azimuth Range
- `get_elevation_range_neg5_90_deg(connector)` - Elevation Range
- `get_pointing_accuracy(connector)` - Pointing Accuracy
- `get_angular_speed_configurable(connector)` - Configurable Angular Speed
- `get_mode_stare_fixed(connector)` - Mode Stare Fixed
- `get_mode_raster_scan(connector)` - Mode Raster Scan
- `get_mode_cone_scan(connector)` - Mode Cone Scan
- `get_mode_volume_scan(connector)` - Mode Volume Scan

#### Remote Control & Commands
- `get_ethernet_api_gui_control(connector)` - Ethernet API/GUI Control
- `get_cmd_set_az(connector)` - Command Set Azimuth
- `get_cmd_set_el(connector)` - Command Set Elevation
- `get_cmd_home(connector)` - Command Home
- `get_cmd_park(connector)` - Command Park
- `get_cmd_start_scan(connector)` - Command Start Scan

## Examples

### Example 1: Using Getter Functions

```python
import asyncio
from infrastructure.opcua_connector import OpcUaConnector
from domain.dto import get_state, get_status, get_heartbeat, get_elastic_channel_355_nm

async def main():
    # Connect to OPC UA server
    connector = OpcUaConnector("opc.tcp://localhost:4840")
    await connector.connect()
    
    try:
        # Read values using getters
        state = await get_state(connector)
        status = await get_status(connector)
        heartbeat = await get_heartbeat(connector)
        elastic_355 = await get_elastic_channel_355_nm(connector)
        
        print(f"State: {state}")
        print(f"Status: {status}")
        print(f"Heartbeat: {heartbeat}")
        print(f"Elastic Channel 355nm: {elastic_355}")
        
    finally:
        await connector.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: Calling OPC UA Methods

```python
import asyncio
from infrastructure.opcua_connector import OpcUaConnector
from application.use_cases.controls import serv_fixed, serv_random, method_cmd

async def main():
    connector = OpcUaConnector("opc.tcp://localhost:4840")
    await connector.connect()
    
    try:
        NS_IDX = 2  # Namespace index for Controls object
        
        # Call specific methods
        result1 = await serv_fixed(connector, NS_IDX)
        result2 = await serv_random(connector, NS_IDX)
        
        # Call generic method by name
        result3 = await method_cmd(connector, NS_IDX, "update_time", 12345)
        
        print(f"ServFixed result: {result1}")
        print(f"ServRandom result: {result2}")
        print(f"update_time result: {result3}")
        
    finally:
        await connector.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 3: Monitoring with History

```python
import asyncio
from infrastructure.opcua_connector import OpcUaConnector
from infrastructure.memory_history_repo import MemoryHistoryRepo
from application.use_cases.monitor import monitor_subscription
from domain.entity import LIDER

async def main():
    connector = OpcUaConnector("opc.tcp://localhost:4840")
    await connector.connect()
    
    lider = LIDER()
    history = MemoryHistoryRepo(retention_minutes=10)
    
    # Attribute map: domain attribute -> OPC UA node ID
    ATTR_MAP = {
        "HEARTBEAT": "ns=2;s=heartbeat",
        "ELASTIC_CHANNEL_355_NM": "ns=2;s=lidar_get_ElasticChannel355Nm",
    }
    
    try:
        # Start monitoring with subscription (500ms period)
        await monitor_subscription(connector, ATTR_MAP, lider, history, period_ms=500)
        
        # Access history
        heartbeat_history = history.get_history("heartbeat")
        for timestamp, value in heartbeat_history:
            print(f"{timestamp}: {value}")
            
    finally:
        await connector.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Structure

```
si3-python-client-sub/
├── main.py                          # Main entry point
├── setup.py                         # Package setup
├── pyproject.toml                   # Project configuration
├── src/
│   ├── domain/
│   │   ├── entity.py               # SI3 entity (data model)
│   │   └── dto.py                  # Data Transfer Objects + Getter functions
│   ├── infrastructure/
│   │   ├── opcua_connector.py      # OPC UA connection handler
│   │   └── memory_history_repo.py  # In-memory history storage
│   ├── application/
│   │   └── use_cases/
│   │       ├── controls.py         # Control method calls
│   │       ├── history.py          # History queries
│   │       └── monitor.py           # Monitoring logic
│   └── presentation/
│       └── bokeh_app.py            # Bokeh visualization
```

## Environment Variables

You can optionally create a `.env` file in the project root:

```env
opcua_url=opc.tcp://localhost:4840
```

The client will automatically load this if present.

## Troubleshooting

### Connection Issues
- Verify the OPC UA server is running and accessible
- Check the URL format: `opc.tcp://hostname:port`
- Ensure firewall allows the connection

### Bokeh Not Starting
- Check if port 5010 (or the shown port) is available
- Verify all dependencies are installed: `pip list`

### Import Errors
- Ensure the package is installed: `pip install -e .`
- Activate the virtual environment before running

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
