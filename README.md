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

### With Polling Mode

To use polling instead of subscriptions (useful for slower update rates):

```bash
python main.py opc.tcp://localhost:4840 --RATE 1.0
```

The `--RATE` parameter specifies the polling interval in seconds (e.g., 0.5, 1.0, 2.5).

### Interactive Menu

Once running, the client provides an interactive menu:

```
================= SI3 OPC UA =================
1) Show Graph (Bokeh)
2) Call generic method (call: <name>)
3) Test OPC UA getters (usage example)
b) Put in background (recover terminal)
q) Exit
==============================================
Option:
```

**Menu Options:**
- **1** - Opens/refreshes the Bokeh web interface for real-time data visualization
- **2** - Calls a generic OPC UA method by name
- **3** - Demonstrates how to use the getter functions with example calls
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

#### Session & Configuration
- `get_current_session_number(connector)` - Current session number
- `get_sessions_name(connector)` - Sessions name
- `get_random_generator_code(connector)` - Random generator code
- `get_verbose_status(connector)` - Verbose status
- `get_update_time(connector)` - Update time
- `get_isotstamp(connector)` - ISO timestamp

#### Error Information
- `get_error_number(connector)` - Error number
- `get_error_information(connector)` - Error information
- `get_error_recovering(connector)` - Error recovery status
- `get_error_number_recovered(connector)` - Recovered error number
- `get_error_number_outofrange(connector)` - Out of range error flag

#### PR59 Sensor
- `get_pr59_temp1(connector)` - Temperature 1
- `get_pr59_temp2(connector)` - Temperature 2
- `get_pr59_temp3(connector)` - Temperature 3
- `get_pr59_temp4_fet(connector)` - Temperature 4 FET
- `get_pr59_sp1(connector)` - SP1
- `get_pr59_main_voltage(connector)` - Main voltage
- `get_pr59_main_current(connector)` - Main current
- `get_pr59_fan1_state(connector)` - Fan 1 state
- `get_pr59_fan2_state(connector)` - Fan 2 state
- `get_pr59_comm_port(connector)` - Communication port

#### TDC (Time-to-Digital Converter)
- `get_tdc_counter1(connector)` through `get_tdc_counter5(connector)` - Counters 1-5
- `get_tdc_acq_index(connector)` - Acquisition index
- `get_tdc_status(connector)` - TDC status
- `get_tdc_internal_temp(connector)` - Internal temperature
- `get_tdc_fpga_temp(connector)` - FPGA temperature
- `get_tdc_wr_pps(connector)` - WR PPS status
- `get_tdc_wr_10mhz(connector)` - WR 10MHz status
- `get_tdc_data_file_name(connector)` - Data file name

#### Ximea Camera
- `get_ximea_enc64_file(connector)` - Enc64 file
- `get_ximea_delta_x(connector)` - Delta X
- `get_ximea_delta_y(connector)` - Delta Y
- `get_ximea_r80(connector)` - R80 value
- `get_ximea_r80_center_x(connector)` - R80 center X
- `get_ximea_r80_center_y(connector)` - R80 center Y
- `get_ximea_temperature(connector)` - Temperature
- `get_ximea_status(connector)` - Status

#### Other
- `get_heartbeat(connector)` - Heartbeat counter
- `get_fw_position(connector)` - Filter wheel position
- `get_simul_flag(connector)` - Simulation flag
- `get_ntp_sync(connector)` - NTP sync status
- `get_cx7000_port_values(connector)` - CX7000 port values
- `get_cx7000_status(connector)` - CX7000 status
- `get_table_file_name(connector)` - Table file name

## Examples

### Example 1: Using Getter Functions

```python
import asyncio
from infrastructure.opcua_connector import OpcUaConnector
from domain.dto import get_state, get_status, get_heartbeat, get_pr59_temp1

async def main():
    # Connect to OPC UA server
    connector = OpcUaConnector("opc.tcp://localhost:4840")
    await connector.connect()
    
    try:
        # Read values using getters
        state = await get_state(connector)
        status = await get_status(connector)
        heartbeat = await get_heartbeat(connector)
        temp1 = await get_pr59_temp1(connector)
        
        print(f"State: {state}")
        print(f"Status: {status}")
        print(f"Heartbeat: {heartbeat}")
        print(f"PR59 Temp1: {temp1}")
        
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
from domain.entity import SI3

async def main():
    connector = OpcUaConnector("opc.tcp://localhost:4840")
    await connector.connect()
    
    si3 = SI3()
    history = MemoryHistoryRepo(retention_minutes=10)
    
    # Attribute map: domain attribute -> OPC UA node ID
    ATTR_MAP = {
        "heartbeat": "ns=2;s=heartbeat",
        "pr59_temp1": "ns=2;s=si3_get_pr59_temp1",
        "pr59_temp2": "ns=2;s=si3_get_pr59_temp2",
    }
    
    try:
        # Start monitoring with subscription (500ms period)
        await monitor_subscription(connector, ATTR_MAP, si3, history, period_ms=500)
        
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
