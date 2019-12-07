CS 170 Final Project Submission (Group 10). Team Members: Ayush Jain, Manav Rathod, Jaiveer Singh.

## Initial Setup

### Local Repository
Begin by cloning this repository using `git clone https://github.com/jaiveersingh1/cs170-project.git` (or `git@github.com:jaiveersingh1/cs170-project.git` if you have SSH enabled) into the local folder on your machine that you will be using to run the code in this project.

### Gurobi Optimization
To run the solver efficiently, download the optimizer engine provided by Gurobi Optimization's academic license, which can be activated for free using an account created with a `....@berkeley.edu` email. This can be done at the following link to the Gurobi Optimizer EULA page: `https://www.gurobi.com/downloads/gurobi-optimizer-eula/`. Be sure to specify that your account is an Academic account by choosing the appropriate option when registering for an account. 

Return to the aforementioned EULA link, and click the prompt labeled `I Accept the End User License Agreement`. Now continue on to the downloads page at `https://www.gurobi.com/downloads/gurobi-software/` and download the version 9.0.0 software installer for your operating system. Unzip if necessary, and install Gurobi Optimizer on your machine using the downloaded installer. Make sure that your PATH has been updated with `gurobi900` after the installation has been completed.

### `grbgetkey ACADEMIC_LICENSE_KEY`
Proceed by registering for an Academic License at `https://www.gurobi.com/downloads/end-user-license-agreement-academic/`. Click the prompt labeled `I Accept These Conditions`, and copy the license key at the bottom of the page this prompt redirects to (e.g. `754380a8-18b5-11ea-843b-020d093b5256`). 

Now, open your terminal of choice (e.g. `Git Bash`, `ITerm2`) and run the command `grbgetkey ACADEMIC_LICENSE_KEY`, where `ACADEMIC_LICENSE_KEY` is the key you copied earlier. This command must be run while conncted to a UC Berkeley academic network (i.e. `AirBears2`).

## Running the Solver 

### `python3 solver.py --all batches/inputs`
