# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Initial `pyproject.toml` packaging with flit.
- Object-oriented inference runner.
- Basic test suite and documentation scaffold.
- Integration tests using external AlphaFold example dataset staged via fixtures.

### Changed
- Refactored project into `src/` layout and modern Python package.
- Tests generate synthetic fixtures instead of using bundled examples.

### Fixed
- Restored CLI banner, argument help, and copyright notice.

### Removed
- Legacy bytecode and obsolete paths.
- Large example output files from the repository; use external test data instead.
