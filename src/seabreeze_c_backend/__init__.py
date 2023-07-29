"""This is a wrapper for the c-implementation of the seabreeze-library

"""
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeAcquisitionDelayFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeAPI
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeContinuousStrobeFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeDataBufferFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeDevice
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeDHCPServerFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeEEPROMFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeError
from seabreeze_c_backend._libseabreeze_wrapper import (
    SeaBreezeEthernetConfigurationFeature,
)
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeFastBufferFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeGPIOFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeI2CMasterFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeIntrospectionFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeIPv4Feature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeIrradCalFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeLightSourceFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeMulticastFeature
from seabreeze_c_backend._libseabreeze_wrapper import (
    SeaBreezeNetworkConfigurationFeature,
)
from seabreeze_c_backend._libseabreeze_wrapper import (
    SeaBreezeNonlinearityCoefficientsFeature,
)
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeNumFeaturesError
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeOpticalBenchFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezePixelBinningFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeRawUSBBusAccessFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeRevisionFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeShutterFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeSpectrometerFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeSpectrumProcessingFeature
from seabreeze_c_backend._libseabreeze_wrapper import (
    SeaBreezeStrayLightCoefficientsFeature,
)
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeStrobeLampFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeTemperatureFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeThermoElectricFeature
from seabreeze_c_backend._libseabreeze_wrapper import SeaBreezeWifiConfigurationFeature

try:
    from seabreeze_c_backend._version import __version__ as __version__
except ImportError:
    __version__ = "not-installed"


__all__ = [
    "_backend_",
    "SeaBreezeAcquisitionDelayFeature",
    "SeaBreezeAPI",
    "SeaBreezeContinuousStrobeFeature",
    "SeaBreezeDataBufferFeature",
    "SeaBreezeDevice",
    "SeaBreezeDHCPServerFeature",
    "SeaBreezeEEPROMFeature",
    "SeaBreezeError",
    "SeaBreezeEthernetConfigurationFeature",
    "SeaBreezeFastBufferFeature",
    "SeaBreezeFeature",
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

_backend_ = "cseabreeze"
