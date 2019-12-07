CS 170 Final Project Submission (Group 10). Team Members: Ayush Jain, Manav Rathod, Jaiveer Singh.

## Initial Setup

### Local Project Setup
Begin by unzip your machine that you will be using to run the code in this project.

### Gurobi Optimization Installation
To run the solver efficiently, download the optimizer engine provided by Gurobi Optimization's academic license, which can be activated for free using an account created with a `....@berkeley.edu` email. This can be done at the following link to the Gurobi Optimizer EULA page: `https://www.gurobi.com/downloads/gurobi-optimizer-eula/`. Be sure to specify that your account is an Academic account by choosing the appropriate option when registering for an account. 

Return to the aforementioned EULA link, and click the prompt labeled `I Accept the End User License Agreement`. Now continue on to the downloads page at `https://www.gurobi.com/downloads/gurobi-software/` and download the version 9.0.0 software installer for your operating system. Unzip if necessary, and install Gurobi Optimizer on your machine using the downloaded installer. Make sure that your PATH has been updated with `gurobi900` after the installation has been completed.

### Academic License Setup
Proceed by registering for an Academic License at `https://www.gurobi.com/downloads/end-user-license-agreement-academic/`. Click the prompt labeled `I Accept These Conditions`, and copy the license key at the bottom of the page this prompt redirects to (e.g. `754380a8-18b5-11ea-843b-020d093b5256`). 

Now, open your terminal of choice (e.g. `Git Bash`, `ITerm2`) and run the command `grbgetkey ACADEMIC_LICENSE_KEY`, where `ACADEMIC_LICENSE_KEY` is the key you copied earlier. This command must be run while conncted to a UC Berkeley academic network (i.e. `AirBears2`).

## Running the Solver 

### Module Installation
Continue now by opening To run the solver properly, you will need to make sure that you have downloaded all the modules used in the code. To do so, run the command `pip install -r requirements.txt`.

### `cp models/models_baseline.sqlite models.sqlite`
Create a local version of the baseline SQLite table used to keep track of optimality and cost across all input files. This table will self-update by the solver as it runs through all the provided inputs.

### `python3 solver.py --all input_dir output_dir`
At last, the moment of truth! To run the solver, run the command `python3 solver.py --all input_dir output_dir`, where `input_dir` is the directory where the inputs are to be fetched from (to run all inputs, you may opt to use the directory `batches/inputs/` as `input_dir`) and `output_dir` is the directory where you would like output files to be stored. If you wish to set other parameters, please choose them from among the following choices:

`-t num_seconds`: Timeout, in seconds. The solver will run for `num_seconds` on each input or until optimality is achieved, whichever is shorter. Default timeout is 300 seconds. Set `num_seconds` to -1 for infinite timeout (all inputs run to optimality).

`--no-model-start`: Do not seed the solver with a starting solution in the code using `model.start`.

`-r num_iters`: Randomize the starter soultion provided to `model.start` (i.e. generate new seed). Generates new seed `num_iters` times before setting starter solution.

`--no-prev`: Do not use a previously stored solution to a given input file as the starter solution if such an input with a previously existing soultion is run.

`--no-skip`: Do not skip files that have already been recorded as optimal in the SQL table.

`--approx`: Scales all edge weights down by dividing each by a factor of 10,000 as an intermediate solver step, to make computations simpler.

`--force-write`: Forces every solution found to be written to the output directory, even if it would overwrite an existing output.

`-m mode_type`: Choose `mode_type` from `all` (runs ILP Solver, Brute Force Solver, and Naive Solver), `ilp` (ILP Only), `bf` (Brute Force Only), naive (Naive Only).

`-v`: Verbose. Print all decision matrices and their solutions from the ILP solver.

`-s`: Silent. Minimize output as much as possible.

### `tail -f logfiles/logfile_DD-MM-YY_HH-MM-SS.txt`
Use the command `tail -f logfiles/logfile_DD-MM-YY_HH-MM-SS.txt` (Note: `HH` is in 24 hour format) to view real-time updates (e.g. optimality status, solution cost, etc.)  from the solver as it runs over all the files. 

That's all! Thanks for reading.
