# `gps-time`

## Purpose

Use a GNSS receiver as a local timing reference with **gpsd + chrony**, and
optionally serve that disciplined time to other HamStack nodes on selected LAN
networks.

A GPS/PPS source is a stratum-0 reference; the HamStack host disciplined from it
serves NTP as stratum 1. Client access is closed by default. Add CIDRs to
`hamstack_gps_time_allow_networks` to make chrony answer remote clients.

## Device model

`hamstack_gps_time_device` names an entry in `hamstack_devices`. The resource
must provide `endpoints.serial`; PPS-capable receivers may also provide
`endpoints.pps`.

With PPS enabled, `auto` uses a compatibility-oriented pairing: gpsd SHM 0
provides the coarse NMEA second and the gpsd chrony SOCK associated with the PPS
device provides the high-precision pulse. `shm` is also available explicitly,
using SHM 0/1. For modern gpsd (3.25+) an operator may choose `sock` for the NMEA
serial-data source and validate the receiver's offset/delay.

The role does not expose gpsd itself on the LAN; only NTP service is intended.

### Stratum semantics

The GPS/GNSS receiver and PPS signal are **stratum-0 reference sources**.
The HamStack host running chrony is not itself "stratum 0"; chrony advertises
the appropriate derived NTP stratum to clients.

`hamstack_gps_time_allow_networks` controls which client networks chrony will
serve. It defaults to an empty list, so enabling this role does not
automatically expose an NTP server to every attached LAN.
