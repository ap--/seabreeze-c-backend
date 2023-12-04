"""Wrapper for the C-implementation of the seabreeze-library"""
from seabreeze_c_backend._libseabreeze_wrapper import (
    SeaBreezeAcquisitionDelayFeature,
    SeaBreezeAPI,
    SeaBreezeContinuousStrobeFeature,
    SeaBreezeDataBufferFeature,
    SeaBreezeDevice,
    SeaBreezeDHCPServerFeature,
    SeaBreezeEEPROMFeature,
    SeaBreezeError,
    SeaBreezeEthernetConfigurationFeature,
    SeaBreezeFastBufferFeature,
    SeaBreezeFeature,
    SeaBreezeGPIOFeature,
    SeaBreezeI2CMasterFeature,
    SeaBreezeIntrospectionFeature,
    SeaBreezeIPv4Feature,
    SeaBreezeIrradCalFeature,
    SeaBreezeLightSourceFeature,
    SeaBreezeMulticastFeature,
    SeaBreezeNetworkConfigurationFeature,
    SeaBreezeNonlinearityCoefficientsFeature,
    SeaBreezeNumFeaturesError,
    SeaBreezeOpticalBenchFeature,
    SeaBreezePixelBinningFeature,
    SeaBreezeRawUSBBusAccessFeature,
    SeaBreezeRevisionFeature,
    SeaBreezeShutterFeature,
    SeaBreezeSpectrometerFeature,
    SeaBreezeSpectrumProcessingFeature,
    SeaBreezeStrayLightCoefficientsFeature,
    SeaBreezeStrobeLampFeature,
    SeaBreezeTemperatureFeature,
    SeaBreezeThermoElectricFeature,
    SeaBreezeWifiConfigurationFeature,
)

try:
    from seabreeze_c_backend._version import __version__ as __version__
except ImportError:
    __version__ = "not-installed"


__all__ = [
    # --- backend ---
    "__seabreeze_backend__",
    "SeaBreezeAPI",
    "SeaBreezeDevice",
    "SeaBreezeError",
    "SeaBreezeFeature",
    # --- features ---
    "SeaBreezeAcquisitionDelayFeature",
    "SeaBreezeContinuousStrobeFeature",
    "SeaBreezeDataBufferFeature",
    "SeaBreezeDHCPServerFeature",
    "SeaBreezeEEPROMFeature",
    "SeaBreezeEthernetConfigurationFeature",
    "SeaBreezeFastBufferFeature",
    "SeaBreezeGPIOFeature",
    "SeaBreezeI2CMasterFeature",
    "SeaBreezeIntrospectionFeature",
    "SeaBreezeIPv4Feature",
    "SeaBreezeIrradCalFeature",
    "SeaBreezeLightSourceFeature",
    "SeaBreezeMulticastFeature",
    "SeaBreezeNetworkConfigurationFeature",
    "SeaBreezeNonlinearityCoefficientsFeature",
    "SeaBreezeNumFeaturesError",
    "SeaBreezeOpticalBenchFeature",
    "SeaBreezePixelBinningFeature",
    "SeaBreezeRawUSBBusAccessFeature",
    "SeaBreezeRevisionFeature",
    "SeaBreezeShutterFeature",
    "SeaBreezeSpectrometerFeature",
    "SeaBreezeSpectrumProcessingFeature",
    "SeaBreezeStrayLightCoefficientsFeature",
    "SeaBreezeStrobeLampFeature",
    "SeaBreezeTemperatureFeature",
    "SeaBreezeThermoElectricFeature",
    "SeaBreezeWifiConfigurationFeature",
]

__seabreeze_backend__ = _backend_ = "cseabreeze"
