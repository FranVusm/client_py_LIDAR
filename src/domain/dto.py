# src/domain/dto.py
from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import datetime

@dataclass
class LIDERDTO:
    # keeps a serializable form used at boundaries (presentation / persistence)
    payload: Dict[str, Any]
    timestamp: datetime

    @classmethod
    def from_entity(cls, si3):
        data = {k: getattr(si3, k) for k in si3.__dataclass_fields__.keys()}
        return cls(payload=data, timestamp=datetime.utcnow())


# ============================================================================
# Getter functions for OPC UA connection (LIDAR)
# Updated based on ICD_LIDAR_V0.2_2025_11_18
# ============================================================================

# --- Basic Status & Info ---

async def get_state(connector) -> Optional[int]:
    """Reads the LIDAR state"""
    return await connector.read_node("ns=2;s=lidar_get_state")

async def get_status(connector) -> Optional[int]:
    """Reads the LIDAR status"""
    return await connector.read_node("ns=2;s=lidar_get_status")

async def get_app_name(connector) -> Optional[str]:
    """Reads the server application name"""
    return await connector.read_node("ns=2;s=lidar_get_serverApplicationName")

async def get_opcua_port(connector) -> Optional[int]:
    """Reads the OPC UA port"""
    return await connector.read_node("ns=2;s=lidar_get_opcuaPort")

async def get_web_port(connector) -> Optional[int]:
    """Reads the Web port"""
    return await connector.read_node("ns=2;s=lidar_get_webPort")

async def get_app_start_time(connector) -> Optional[str]:
    """Reads the application start time"""
    return await connector.read_node("ns=2;s=lidar_get_startTime")

async def get_serial_number(connector) -> Optional[str]:
    """Reads the serial number"""
    return await connector.read_node("ns=2;s=lidar_get_serialNumber")

async def get_table_file_name(connector) -> Optional[str]:
    """Reads the table file name"""
    return await connector.read_node("ns=2;s=lidar_get_fileNameTable")

async def get_prosys_sdk_version(connector) -> Optional[str]:
    """Reads the Prosys SDK version"""
    return await connector.read_node("ns=2;s=lidar_get_sdkversion")

async def get_current_session_number(connector) -> Optional[int]:
    """Reads the current session number"""
    return await connector.read_node("ns=2;s=lidar_get_currentsessionnumber")

async def get_sessions_name(connector) -> Optional[str]:
    """Reads the sessions name"""
    return await connector.read_node("ns=2;s=lidar_get_sessionsname")

async def get_random_generator_code(connector) -> Optional[int]:
    """Reads the random generator code"""
    return await connector.read_node("ns=2;s=lidar_get_randomgeneratorcode")

async def get_verbose_status(connector) -> Optional[bool]:
    """Reads the verbose status"""
    return await connector.read_node("ns=2;s=lidar_get_verbosestatus")

async def get_updatetime(connector) -> Optional[int]:
    """Reads the update time"""
    return await connector.read_node("ns=2;s=lidar_get_updatetime")

async def get_isotstamp(connector) -> Optional[str]:
    """Reads the ISO timestamp"""
    return await connector.read_node("ns=2;s=lidar_get_isotstamp")

async def get_heartbeat(connector) -> Optional[int]:
    """Reads the heartbeat"""
    return await connector.read_node("ns=2;s=heartbeat")

# --- Errors ---

async def get_error_number(connector) -> Optional[int]:
    """Reads the error number"""
    return await connector.read_node("ns=2;s=lidar_get_error_number")

async def get_error_information(connector) -> Optional[str]:
    """Reads the error information"""
    return await connector.read_node("ns=2;s=lidar_get_error_information")

async def get_error_recovering(connector) -> Optional[str]:
    """Reads the error recovering list"""
    return await connector.read_node("ns=2;s=lidar_get_error_recovering")

async def get_error_number_recovered(connector) -> Optional[int]:
    """Reads the number of recovered errors"""
    return await connector.read_node("ns=2;s=lidar_get_error_number_recovered")

async def get_error_number_outofrange(connector) -> Optional[bool]:
    """Reads if error number is out of range"""
    return await connector.read_node("ns=2;s=lidar_get_error_number_outofrange")

# --- Raw Channels ---

async def get_elastic_channel_355_nm(connector) -> Optional[float]:
    """Reads Elastic Channel 355nm"""
    return await connector.read_node("ns=2;s=lidar_get_ElasticChannel355Nm")

async def get_elastic_channel_532_nm(connector) -> Optional[float]:
    """Reads Elastic Channel 532nm"""
    return await connector.read_node("ns=2;s=lidar_get_ElasticChannel532Nm")

async def get_elastic_channel_1064_nm(connector) -> Optional[float]:
    """Reads Elastic Channel 1064nm"""
    return await connector.read_node("ns=2;s=lidar_get_ElasticChannel1064Nm")

async def get_raman_channel_n2_387_nm(connector) -> Optional[float]:
    """Reads Raman Channel N2 387nm"""
    return await connector.read_node("ns=2;s=lidar_get_RamanChannelN2387Nm")

async def get_raman_channel_h2o(connector) -> Optional[float]:
    """Reads Raman Channel H2O"""
    return await connector.read_node("ns=2;s=lidar_get_RamanChannelH2o")

async def get_raman_range_signal_counts(connector) -> Optional[float]:
    """Reads Raman Range Signal Counts"""
    return await connector.read_node("ns=2;s=lidar_get_RamanRangeSignalCounts")

async def get_statistical_error_per_bin(connector) -> Optional[float]:
    """Reads Statistical Error Per Bin"""
    return await connector.read_node("ns=2;s=lidar_get_StatisticalErrorPerBin")

async def get_integration_time(connector) -> Optional[float]:
    """Reads Integration Time"""
    return await connector.read_node("ns=2;s=lidar_get_IntegrationTime")

async def get_co_polar_355_nm(connector) -> Optional[float]:
    """Reads Co-Polar 355nm"""
    return await connector.read_node("ns=2;s=lidar_get_CoPolar355Nm")

async def get_cross_polar_355_nm(connector) -> Optional[float]:
    """Reads Cross-Polar 355nm"""
    return await connector.read_node("ns=2;s=lidar_get_CrossPolar355Nm")

async def get_co_polar_532_nm(connector) -> Optional[float]:
    """Reads Co-Polar 532nm"""
    return await connector.read_node("ns=2;s=lidar_get_CoPolar532Nm")

async def get_cross_polar_532_nm(connector) -> Optional[float]:
    """Reads Cross-Polar 532nm"""
    return await connector.read_node("ns=2;s=lidar_get_CrossPolar532Nm")

async def get_depolarisation_ratio_profile(connector) -> Optional[float]:
    """Reads Depolarisation Ratio Profile"""
    return await connector.read_node("ns=2;s=lidar_get_DepolarisationRatioProfile")

# --- Derived Parameters ---

async def get_backscatter_coefficient_beta_z(connector) -> Optional[float]:
    """Reads Backscatter Coefficient Beta Z"""
    return await connector.read_node("ns=2;s=lidar_get_BackscatterCoefficientBetaZ")

async def get_extinction_coefficient_alpha_z(connector) -> Optional[float]:
    """Reads Extinction Coefficient Alpha Z"""
    return await connector.read_node("ns=2;s=lidar_get_ExtinctionCoefficientAlphaZ")

async def get_aerosol_optical_depth(connector) -> Optional[float]:
    """Reads Aerosol Optical Depth"""
    return await connector.read_node("ns=2;s=lidar_get_AerosolOpticalDepth")

async def get_lidar_ratio_s_z(connector) -> Optional[float]:
    """Reads Lidar Ratio S Z"""
    return await connector.read_node("ns=2;s=lidar_get_LidarRatioSZ")

async def get_humidity_profile_h2o(connector) -> Optional[float]:
    """Reads Humidity Profile H2O"""
    return await connector.read_node("ns=2;s=lidar_get_HumidityProfileH2o")

async def get_pbl_height(connector) -> Optional[float]:
    """Reads PBL Height"""
    return await connector.read_node("ns=2;s=lidar_get_PblHeight")

async def get_cloud_base_height(connector) -> Optional[float]:
    """Reads Cloud Base Height"""
    return await connector.read_node("ns=2;s=lidar_get_CloudBaseHeight")

async def get_snr_per_bin(connector) -> Optional[float]:
    """Reads SNR Per Bin"""
    return await connector.read_node("ns=2;s=lidar_get_SnrPerBin")

# --- Metadata & Quality Indicators ---

async def get_timestamp_utc(connector) -> Optional[str]:
    """Reads Timestamp UTC"""
    return await connector.read_node("ns=2;s=lidar_get_Timestamp_Utc")

async def get_integration_accumulation_time(connector) -> Optional[float]:
    """Reads Integration Accumulation Time"""
    return await connector.read_node("ns=2;s=lidar_get_IntegrationAccumulationTime")

async def get_number_of_accumulated_pulses(connector) -> Optional[float]:
    """Reads Number of Accumulated Pulses"""
    return await connector.read_node("ns=2;s=lidar_get_NumberOfAccumulatedPulses")

async def get_vertical_resolution_bin_size(connector) -> Optional[float]:
    """Reads Vertical Resolution Bin Size"""
    return await connector.read_node("ns=2;s=lidar_get_VerticalResolutionBinSize")

async def get_temporal_resolution(connector) -> Optional[float]:
    """Reads Temporal Resolution"""
    return await connector.read_node("ns=2;s=lidar_get_TemporalResolution")

async def get_global_snr(connector) -> Optional[float]:
    """Reads Global SNR"""
    return await connector.read_node("ns=2;s=lidar_get_GlobalSnr")

async def get_quality_flags(connector) -> Optional[str]:
    """Reads Quality Flags"""
    return await connector.read_node("ns=2;s=lidar_get_QualityFlags")

async def get_internal_temperatures(connector) -> Optional[float]:
    """Reads Internal Temperatures"""
    return await connector.read_node("ns=2;s=lidar_get_InternalTemperatures")

async def get_laser_readings_energy_voltage_prf(connector) -> Optional[float]:
    """Reads Laser Readings"""
    return await connector.read_node("ns=2;s=lidar_get_LaserReadingsEnergyVoltagePrf")

# --- Pre-processed Products ---

async def get_aod_time_series(connector) -> Optional[float]:
    """Reads AOD Time Series"""
    return await connector.read_node("ns=2;s=lidar_get_AodTimeSeries")

async def get_averaged_interval_profiles(connector) -> Optional[float]:
    """Reads Averaged Interval Profiles"""
    return await connector.read_node("ns=2;s=lidar_get_AveragedIntervalProfiles")

async def get_netcdf_ascii_grid_files(connector) -> Optional[str]:
    """Reads NetCDF/ASCII Grid Files info"""
    return await connector.read_node("ns=2;s=lidar_get_NetcdfAsciiGridFiles")

async def get_range_time_images(connector) -> Optional[str]:
    """Reads Range Time Images info"""
    return await connector.read_node("ns=2;s=lidar_get_RangeTimeImages")

async def get_ash_cloud_automatic_detection(connector) -> Optional[str]:
    """Reads Ash Cloud Automatic Detection"""
    return await connector.read_node("ns=2;s=lidar_get_AshCloudAutomaticDetection")

# --- Pointing & Scanning ---

async def get_motorised_2_axis_mount(connector) -> Optional[str]:
    """Reads Motorised 2-Axis Mount info"""
    return await connector.read_node("ns=2;s=lidar_get_Motorised2AxisMount")

async def get_three_d_scanning_capability(connector) -> Optional[str]:
    """Reads 3D Scanning Capability info"""
    return await connector.read_node("ns=2;s=lidar_get_ThreeDScanningCapability")

async def get_azimuth_range_0_360_deg(connector) -> Optional[float]:
    """Reads Azimuth Range"""
    return await connector.read_node("ns=2;s=lidar_get_AzimuthRange0360Deg")

async def get_elevation_range_minus5_90_deg(connector) -> Optional[float]:
    """Reads Elevation Range (-5 to 90)"""
    return await connector.read_node("ns=2;s=lidar_get_ElevationRange_590Deg")

async def get_pointing_accuracy(connector) -> Optional[float]:
    """Reads Pointing Accuracy"""
    return await connector.read_node("ns=2;s=lidar_get_PointingAccuracy")

async def get_angular_speed_configurable(connector) -> Optional[float]:
    """Reads Configurable Angular Speed"""
    return await connector.read_node("ns=2;s=lidar_get_AngularSpeedConfigurable")

async def get_mode_stare_fixed(connector) -> Optional[str]:
    """Reads Mode Stare Fixed"""
    return await connector.read_node("ns=2;s=lidar_get_ModeStareFixed")

async def get_mode_raster_scan(connector) -> Optional[str]:
    """Reads Mode Raster Scan"""
    return await connector.read_node("ns=2;s=lidar_get_ModeRasterScan")

async def get_mode_cone_scan(connector) -> Optional[str]:
    """Reads Mode Cone Scan"""
    return await connector.read_node("ns=2;s=lidar_get_ModeConeScan")

async def get_mode_volume_scan(connector) -> Optional[str]:
    """Reads Mode Volume Scan"""
    return await connector.read_node("ns=2;s=lidar_get_ModeVolumeScan")

async def get_angular_step_per_bin(connector) -> Optional[float]:
    """Reads Angular Step Per Bin"""
    return await connector.read_node("ns=2;s=lidar_get_AngularStepPerBin")

async def get_integration_time_per_position(connector) -> Optional[float]:
    """Reads Integration Time Per Position"""
    return await connector.read_node("ns=2;s=lidar_get_IntegrationTimePerPosition")

# --- Remote Control & Commands ---

async def get_ethernet_api_gui_control(connector) -> Optional[str]:
    """Reads Ethernet API/GUI Control"""
    return await connector.read_node("ns=2;s=lidar_get_EthernetApiGuiControl")

async def get_cmd_set_az(connector) -> Optional[str]:
    """Reads Command Set Azimuth"""
    return await connector.read_node("ns=2;s=lidar_get_CmdSetAz")

async def get_cmd_set_el(connector) -> Optional[str]:
    """Reads Command Set Elevation"""
    return await connector.read_node("ns=2;s=lidar_get_CmdSetEl")

async def get_cmd_home(connector) -> Optional[str]:
    """Reads Command Home"""
    return await connector.read_node("ns=2;s=lidar_get_CmdHome")

async def get_cmd_park(connector) -> Optional[str]:
    """Reads Command Park"""
    return await connector.read_node("ns=2;s=lidar_get_CmdPark")

async def get_cmd_start_scan(connector) -> Optional[str]:
    """Reads Command Start Scan"""
    return await connector.read_node("ns=2;s=lidar_get_CmdStartScan")

async def get_telemetry_status_position_encoder(connector) -> Optional[str]:
    """Reads Telemetry Status Position Encoder"""
    return await connector.read_node("ns=2;s=lidar_get_TelemetryStatusPositionEncoder")

async def get_command_latency(connector) -> Optional[float]:
    """Reads Command Latency"""
    return await connector.read_node("ns=2;s=lidar_get_CommandLatency")

async def get_encoder_position_confirmation(connector) -> Optional[str]:
    """Reads Encoder Position Confirmation"""
    return await connector.read_node("ns=2;s=lidar_get_EncoderPositionConfirmation")

async def get_direct_pointing_commands(connector) -> Optional[str]:
    """Reads Direct Pointing Commands"""
    return await connector.read_node("ns=2;s=lidar_get_DirectPointingCommands")

async def get_pointing_tolerance(connector) -> Optional[float]:
    """Reads Pointing Tolerance"""
    return await connector.read_node("ns=2;s=lidar_get_PointingTolerance")

async def get_pointing_verification(connector) -> Optional[str]:
    """Reads Pointing Verification"""
    return await connector.read_node("ns=2;s=lidar_get_PointingVerification")

async def get_measurement_strategy_by_pointing(connector) -> Optional[str]:
    """Reads Measurement Strategy"""
    return await connector.read_node("ns=2;s=lidar_get_MeasurementStrategyByPointing")

async def get_position_quality_flags(connector) -> Optional[str]:
    """Reads Position Quality Flags"""
    return await connector.read_node("ns=2;s=lidar_get_PositionQualityFlags")

# --- Safety ---

async def get_safety_interlocks(connector) -> Optional[str]:
    """Reads Safety Interlocks"""
    return await connector.read_node("ns=2;s=lidar_get_SafetyInterlocks")

async def get_no_go_zones(connector) -> Optional[str]:
    """Reads No-Go Zones"""
    return await connector.read_node("ns=2;s=lidar_get_NoGoZones")

async def get_human_presence_lockout(connector) -> Optional[str]:
    """Reads Human Presence Lockout"""
    return await connector.read_node("ns=2;s=lidar_get_HumanPresenceLockout")

async def get_day_night_modes(connector) -> Optional[str]:
    """Reads Day/Night Modes"""
    return await connector.read_node("ns=2;s=lidar_get_DayNightModes")

# --- Instrument Measurement State ---

async def get_measurement_time_utc(connector) -> Optional[str]:
    """Reads Measurement Time UTC"""
    return await connector.read_node("ns=2;s=lidar_get_MeasurementTimeUtc")

async def get_integration_seconds(connector) -> Optional[float]:
    """Reads Integration Seconds"""
    return await connector.read_node("ns=2;s=lidar_get_IntegrationSeconds")

async def get_laser_wavelength_nm(connector) -> Optional[float]:
    """Reads Laser Wavelength"""
    return await connector.read_node("ns=2;s=lidar_get_LaserWavelengthNm")

async def get_channel_id(connector) -> Optional[str]:
    """Reads Channel ID"""
    return await connector.read_node("ns=2;s=lidar_get_ChannelId")

async def get_range_m(connector) -> Optional[float]:
    """Reads Range (m)"""
    return await connector.read_node("ns=2;s=lidar_get_RangeM")

async def get_signal_counts(connector) -> Optional[float]:
    """Reads Signal Counts"""
    return await connector.read_node("ns=2;s=lidar_get_SignalCounts")

async def get_signal_error(connector) -> Optional[float]:
    """Reads Signal Error"""
    return await connector.read_node("ns=2;s=lidar_get_SignalError")

async def get_backscatter_coef_m_sr(connector) -> Optional[float]:
    """Reads Backscatter Coef"""
    return await connector.read_node("ns=2;s=lidar_get_BackscatterCoefMSr")

async def get_extinction_coef_km_1(connector) -> Optional[float]:
    """Reads Extinction Coef"""
    return await connector.read_node("ns=2;s=lidar_get_ExtinctionCoefKm1")

async def get_depolarization_ratio(connector) -> Optional[float]:
    """Reads Depolarization Ratio"""
    return await connector.read_node("ns=2;s=lidar_get_DepolarizationRatio")

async def get_water_vapour_mixing_ratio_g_per_kg(connector) -> Optional[float]:
    """Reads Water Vapour Mixing Ratio"""
    return await connector.read_node("ns=2;s=lidar_get_WaterVapourMixingRatioGPerKg")

async def get_cloud_base_height_m(connector) -> Optional[float]:
    """Reads Cloud Base Height (m)"""
    return await connector.read_node("ns=2;s=lidar_get_CloudBaseHeightM")

async def get_pbl_height_m(connector) -> Optional[float]:
    """Reads PBL Height (m)"""
    return await connector.read_node("ns=2;s=lidar_get_PblHeightM")

async def get_pointing_az_deg(connector) -> Optional[float]:
    """Reads Pointing Azimuth (deg)"""
    return await connector.read_node("ns=2;s=lidar_get_PointingAzDeg")

async def get_pointing_el_deg(connector) -> Optional[float]:
    """Reads Pointing Elevation (deg)"""
    return await connector.read_node("ns=2;s=lidar_get_PointingElDeg")

async def get_pointing_target_az_deg(connector) -> Optional[float]:
    """Reads Pointing Target Azimuth (deg)"""
    return await connector.read_node("ns=2;s=lidar_get_PointingTargetAzDeg")

async def get_pointing_target_el_deg(connector) -> Optional[float]:
    """Reads Pointing Target Elevation (deg)"""
    return await connector.read_node("ns=2;s=lidar_get_PointingTargetElDeg")

async def get_pointing_status(connector) -> Optional[str]:
    """Reads Pointing Status"""
    return await connector.read_node("ns=2;s=lidar_get_PointingStatus")

async def get_pointing_accuracy_deg(connector) -> Optional[float]:
    """Reads Pointing Accuracy (deg)"""
    return await connector.read_node("ns=2;s=lidar_get_PointingAccuracyDeg")

async def get_scan_mode(connector) -> Optional[str]:
    """Reads Scan Mode"""
    return await connector.read_node("ns=2;s=lidar_get_ScanMode")

async def get_device_status(connector) -> Optional[str]:
    """Reads Device Status"""
    return await connector.read_node("ns=2;s=lidar_get_DeviceStatus")

async def get_file_format_version(connector) -> Optional[str]:
    """Reads File Format Version"""
    return await connector.read_node("ns=2;s=lidar_get_FileFormatVersion")