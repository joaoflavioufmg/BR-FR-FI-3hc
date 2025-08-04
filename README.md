# Healthcare

**Hierarchical (3-level) model for minimum cost and universal coverage health care planning**

## Overview

This project provides a computational framework for planning health care systems using a hierarchical, three-level model. The goal is to achieve universal coverage at minimum cost, supporting evidence-based decisions for infrastructure, workforce, and logistics investments.

## Features

- **Three-level care model:** Primary, secondary, and tertiary care levels.
- **Cost optimization:** Calculates minimum investment required for universal coverage.
- **Infrastructure planning:** Identifies municipalities needing additional infrastructure.
- **Workforce and equipment analysis:** Supports planning for health professionals and medical equipment.
- **Scenario comparison:** Enables analysis of different states, regions, or countries.
- **Data-driven:** Uses real demographic and health system data.

## Directory Structure

- `*.dat` / `*.txt` — Input and output data files for each scenario or region.
- `charts/` — Scripts for visualizing results with geoplotlib.
- `Resultado/` — Output folders with results and notes for each scenario.

## Example Output

- **Coverage summary:** Number of municipalities covered at each care level.
- **Infrastructure needs:** List of municipalities requiring new investments, with cost breakdowns.
- **Cost per capita:** Current and projected health care costs per person.

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd venv_br
   ```

2. **Prepare input data:**  
   Place demographic and health system data in the appropriate `.dat` or `.txt` files as described in the documentation and `ref/` folder.

3. **Run the code:**  
   Use the provided Python scripts or notebooks to process the data and generate results. See instructions in the relevant script or notebook files.

4. **Visualize results:**  
   Use the scripts in `charts/` to generate maps and plots with geoplotlib.

## Requirements

- Python 3.10
- geoplotlib (for visualization)
- NumPy, pandas, and other standard scientific libraries (if applicable)

## License

This repository is provided for academic and research purposes only.

---

*For questions or contributions, please contact the corresponding
