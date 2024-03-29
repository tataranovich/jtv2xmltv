# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2022-12-15

### Fixed

- Fix incorrect program names when the same PDT record referenced multiple times in NDX file
- Include missing JTV example artifact into source distribution for tests

### Added

- CI pipeline to build source distribution and debian binary package

### Changed

- Change default Python 3.x version from 3.7 to 3.9 to run tests

## [v0.2.1] - 2019-11-05

### Changed

- Change default Python 3.x version from 3.5 to 3.7

## [v0.2.0] - 2019-11-04

### Added

- Support both Python 2.7.x and Python 3.x
- Add support for alternative JTV data header
- Support for different encoding (default is CP1251)

### Changed

- Change license from GPL-3 to MIT

## [v0.1.1] - 2019-05-01

### Fixed

- Setuptools cleanup

## [v0.1.0] - 2019-05-01

### Added

- Add Python 3.x support
- Add Setuptools support
- Add tests

### Fixed

- Fix the last program absence in XML output
