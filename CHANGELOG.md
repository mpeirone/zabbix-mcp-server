# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `history_get_aggregated()` - New function for retrieving aggregated historical data over extended time periods
  - Automatically selects between trend data (365-day retention) and history data (7-day retention)
  - Supports custom aggregation intervals (default: 60 minutes)
  - Returns min/avg/max values with data point counts
  - Handles both float and unsigned integer value types
  - Falls back gracefully when data is unavailable

- `host_metrics_30d()` - New function for comprehensive 30-day host metrics
  - Automatically discovers CPU, RAM, and Network monitoring items for any host
  - Returns 30 days of hourly trend data (up to 720 data points)
  - Smart pattern matching for item discovery (system.cpu.*, vm.memory.*, net.if.*)
  - Configurable metric selection (cpu, ram, network, or all)
  - Falls back to 7-day history data when trend data is unavailable
  - Limits to top 3 items per metric type to avoid payload bloat

### Changed
- Enhanced README.md with detailed examples for new aggregation functions
- Updated documentation to reflect trend vs history data retention policies

### Technical Details
- Both new functions leverage the Zabbix trend API for efficiency on long time ranges
- Automatic timezone handling between IST (Zabbix) and UTC (application logs)
- Optimized for log correlation analysis and infrastructure monitoring use cases

## [Previous Versions]

See git history for previous changes.
