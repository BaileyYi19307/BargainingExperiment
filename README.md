
# oTree Bargaining Experiment

This repository contains the code for running a bargaining experiment using oTree. The project consists of two parts: the **Main Experiment** and the **Tutorial Experiment**.

## How to Run the Experiments

### 1. Clone the Repository
To get started, clone the repository to your local machine:

git clone https://github.com/BaileyYi19307/BargainingExperiment.git


### 2. Running the Main Experiment
1. Navigate to the **MainExperiment** directory:
   ```bash
   cd BargainingExperiment/MainExperiment
   ```

2. Run the experiment using oTree's development server:
   ```bash
   otree devserver
   ```

## Modifying the Triangle Parameters
To modify the parameters of the triangle generated in the experiment, you need to adjust the **config section** within the code. The configuration settings are located in the relevant files and allow you to control aspects of the triangle's behavior for the experiment.

## Requirements
To run the experiments, you'll need the following:

- Python 3.x
- oTree (installed via pip)

To install oTree, run the following command:
```bash
pip install otree
```

## Additional Notes
Make sure to configure the settings in both experiments as needed before running the experiments. If you want to switch between running the **Main Experiment** and the **Tutorial Experiment**, make sure to `cd` to the appropriate directory.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License (CC BY-NC-ND 4.0) - see the [LICENSE](LICENSE) file for details.

You may not modify or distribute this work without permission from Professor Andrzej Baranski.

