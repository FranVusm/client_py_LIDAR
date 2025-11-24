# src/domain/entity.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class LIDER:
    # --- Basic Status & Info ---
    state: Optional[int] = None                  # int32
    status: Optional[int] = None                 # int32
    app_name: Optional[str] = None               # string
    opcua_port: Optional[int] = None             # int32
    web_port: Optional[int] = None               # int32
    app_start_time: Optional[str] = None         # string
    serial_number: Optional[str] = None          # string
    table_file_name: Optional[str] = None        # string
    prosys_sdk_version: Optional[str] = None     # string
    current_session_number: Optional[int] = None # int32
    sessions_name: Optional[str] = None          # String[100]
    random_generator_code: Optional[int] = None  # int32
    verbose_status: Optional[bool] = None        # boolean
    updatetime: Optional[int] = None             # int32
    isotstamp: Optional[str] = None              # string
    heartbeat: Optional[int] = None              # int32

    # --- Errors ---
    error_number: Optional[int] = None               # int32
    error_information: Optional[str] = None          # string
    error_recovering: Optional[str] = None           # string
    error_number_recovered: Optional[int] = None     # int32
    error_number_outofrange: Optional[bool] = None   # boolean

    # --- Raw Channels (Floats) ---
    elastic_channel_355_nm: Optional[float] = None
    elastic_channel_532_nm: Optional[float] = None
    elastic_channel_1064_nm: Optional[float] = None
    raman_channel_n2_387_nm: Optional[float] = None
    raman_channel_h2o: Optional[float] = None
    raman_range_signal_counts: Optional[float] = None
    statistical_error_per_bin: Optional[float] = None
    integration_time: Optional[float] = None
    co_polar_355_nm: Optional[float] = None
    cross_polar_355_nm: Optional[float] = None
    co_polar_532_nm: Optional[float] = None
    cross_polar_532_nm: Optional[float] = None
    depolarisation_ratio_profile: Optional[float] = None

    # --- Derived Parameters (Floats) ---
    backscatter_coefficient_beta_z: Optional[float] = None
    extinction_coefficient_alpha_z: Optional[float] = None
    aerosol_optical_depth: Optional[float] = None
    lidar_ratio_s_z: Optional[float] = None
    humidity_profile_h2o: Optional[float] = None
    pbl_height: Optional[float] = None
    cloud_base_height: Optional[float] = None
    snr_per_bin: Optional[float] = None

    # --- Metadata & Quality Indicators ---
    timestamp_utc: Optional[str] = None                     # string
    integration_accumulation_time: Optional[float] = None   # float
    number_of_accumulated_pulses: Optional[float] = None    # float
    vertical_resolution_bin_size: Optional[float] = None    # float
    temporal_resolution: Optional[float] = None             # float
    global_snr: Optional[float] = None                      # float
    quality_flags: Optional[str] = None                     # string
    internal_temperatures: Optional[float] = None           # float
    laser_readings_energy_voltage_prf: Optional[float] = None # float

    # --- Pre-processed Products ---
    aod_time_series: Optional[float] = None                 # float
    averaged_interval_profiles: Optional[float] = None      # float
    netcdf_ascii_grid_files: Optional[str] = None           # string
    range_time_images: Optional[str] = None                 # string
    ash_cloud_automatic_detection: Optional[str] = None     # string

    # --- Pointing & Scanning (Type & Accuracy) ---
    motorised_2_axis_mount: Optional[str] = None            # string
    three_d_scanning_capability: Optional[str] = None       # string
    azimuth_range_0_360_deg: Optional[float] = None         # float
    elevation_range_neg5_90_deg: Optional[float] = None     # float
    pointing_accuracy: Optional[float] = None               # float
    angular_speed_configurable: Optional[float] = None      # float
    mode_stare_fixed: Optional[str] = None                  # string
    mode_raster_scan: Optional[str] = None                  # string
    mode_cone_scan: Optional[str] = None                    # string
    mode_volume_scan: Optional[str] = None                  # string
    angular_step_per_bin: Optional[float] = None            # float
    integration_time_per_position: Optional[float] = None   # float

    # --- Remote Control & Commands ---
    ethernet_api_gui_control: Optional[str] = None          # string
    cmd_set_az: Optional[str] = None                        # string
    cmd_set_el: Optional[str] = None                        # string
    cmd_home: Optional[str] = None                          # string
    cmd_park: Optional[str] = None                          # string
    cmd_start_scan: Optional[str] = None                    # string
    telemetry_status_position_encoder: Optional[str] = None # string
    command_latency: Optional[float] = None                 # float
    encoder_position_confirmation: Optional[str] = None     # string
    direct_pointing_commands: Optional[str] = None          # string
    pointing_tolerance: Optional[float] = None              # float
    pointing_verification: Optional[str] = None             # string
    measurement_strategy_by_pointing: Optional[str] = None  # string
    position_quality_flags: Optional[str] = None            # string

    # --- Safety ---
    safety_interlocks: Optional[str] = None        # string
    no_go_zones: Optional[str] = None              # string
    human_presence_lockout: Optional[str] = None   # string
    day_night_modes: Optional[str] = None          # string

    # --- Instrument Measurement State ---
    measurement_time_utc: Optional[str] = None                  # string
    integration_seconds: Optional[float] = None                 # float
    laser_wavelength_nm: Optional[float] = None                 # float
    channel_id: Optional[str] = None                            # string
    range_m: Optional[float] = None                             # float
    signal_counts: Optional[float] = None                       # float
    signal_error: Optional[float] = None                        # float
    backscatter_coef_m_sr: Optional[float] = None               # float
    extinction_coef_km_1: Optional[float] = None                # float
    depolarization_ratio: Optional[float] = None                # float
    water_vapour_mixing_ratio_g_per_kg: Optional[float] = None  # float
    cloud_base_height_m: Optional[float] = None                 # float
    pbl_height_m: Optional[float] = None                        # float
    pointing_az_deg: Optional[float] = None                     # float
    pointing_el_deg: Optional[float] = None                     # float
    pointing_target_az_deg: Optional[float] = None              # float
    pointing_target_el_deg: Optional[float] = None              # float
    pointing_status: Optional[str] = None                       # string
    pointing_accuracy_deg: Optional[float] = None               # float
    scan_mode: Optional[str] = None                             # string
    device_status: Optional[str] = None                         # string
    file_format_version: Optional[str] = None                   # string

    # generic setter (keeps single responsibility)
    def set_attr(self, name: str, value):
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            raise AttributeError(f"SI3 has no attribute {name}")

    def update_from_mapping(self, mapping: Dict[str, Any]):
        for k, v in mapping.items():
            if v is None:
                continue
            try:
                self.set_attr(k, v)
            except AttributeError:
                # ignore unknowns or log
                pass
