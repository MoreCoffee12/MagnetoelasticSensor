# Magnetoelastic Sensor Python Library - AI Agent Instructions

## Project Overview
This is a Python library for modeling magnetoelastic (inverse magnetostrictive) sensors used in turbomachinery torque and stress measurement. The project is in early development with placeholder structure.

## Architecture & Key Components
- **Focus Areas**: Sensor modeling, signal processing, and experimental data integration for magnetoelastic sensors
- **Purpose**: Model the physics behavior, process signals, and integrate experimental data from magnetoelastic sensors that measure stress through magnetic permeability changes in ferromagnetic materials
- **Target Users**: Engineers and physicists designing, analyzing, and validating magnetoelastic sensors
- **Core Domain Knowledge Needed**:
  - Magnetostriction: ferromagnetic material shape/property changes under magnetic fields
  - Inverse magnetostriction: stress-induced changes in magnetic permeability (tensile = ↑permeability, compressive = ↓permeability)
  - Target sensor architecture: [specific design being implemented] (see README for context)
  - Physics: magnetic circuits, domain alignment, crystal lattice effects
  - Signal processing: coil coupling, voltage/current relationships, frequency response

## Development Patterns & Conventions
- **Language**: Python (based on `.gitignore` indicating `__pycache__`, `.egg-info`, `setup.py` patterns)
- **License**: MIT (Copyright 2026 Brian Howard)
- **Documentation**: Use `README.md` as primary reference; physics principles documented there with vendor attribution (Adobe Stock images)

## Project Structure
- `README.md`: Physics principles, sensor theory, architecture overview
- `media/`: Technical diagrams and illustrations
- `magnetoelasticsensor/`: Single package containing all library code
  - `__init__.py`: Package exports and version
  - Core modules for physics modeling and signal processing
- `tests/`: Unit tests (expected)
- `setup.py` or `pyproject.toml`: Package configuration

## Build & Test Setup (When Available)
- Standard Python packaging expected (setup.py, pyproject.toml) based on `.gitignore`
- Unit tests likely in `tests/` directory
- Coverage reports in `htmlcov/` (from `.gitignore` patterns)

## When Adding New Features
1. Reference physics principles from README when modeling sensor behavior
2. Keep domain logic (physics calculations) separate from I/O and visualization
3. Document sensor architectures (solenoid/cross/multi-branch/hybrid) in code comments with README references
4. Include docstrings explaining physical meaning of parameters, not just data types

## Critical Integration Points
- Magnetic circuit modeling (core + target interaction)
- Stress-to-permeability transformation (the inverse magnetostriction relationship)
- Coil coupling models (drive coil → ferrite core → target → sensing coil)
- Tensile vs. compressive stress symmetry handling
- Experimental data integration: Loading measured sensor outputs and comparing against model predictions
- Calibration workflows: Fitting model parameters to experimental measurements

## External Context
- See [robotsquirrelproductions.com](https://robotsquirrelproductions.com/vibration-transducers/#section-13) for detailed background
- Images sourced from Adobe Stock (reference IDs in README)
