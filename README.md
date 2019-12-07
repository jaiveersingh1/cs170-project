CS 170 Final Project Submission (Group 10).

## Initial Setup

### Local Repository
Begin by cloning this repository using `git clone https://github.com/ajain-23/berkeley-met.git` (or `git clone git@github.com:ajain-23/berkeley-met.git` if you have SSH enabled) into the local folder on your machine that you will be using for development on this project.

### Node JS ###
To work locally, you’ll need to have Node 8.16.0, Node 10.16.0, or any later version on your local development machine. Find the installation link at [https://nodejs.org](http://nodejs.org/en/)

This will provide us the command-line tools (e.g. `npm`, `npx`) to work with any of our server-side integrations (e.g. firebase) and build/run locally.

### Firebase CLI ###
Run the `npm install firebase --save` and the `npm install -g firebase-tools` commands, which installs firebase globally for use in your terminal. 

Next, run `firebase login --interactive` and login with your Berkeley email in the popup window to get access to the `berkeleymet` (key `metday-3a266`) project in firebase. This will allow you to deploy without hassle anytime you wish to publish changes.

## Running, Testing, and Building 

We will primarily be using the following commands:

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `firebase deploy`

We will be using this command in conjunction with `npm run build` anytime we want to release a new version of the project to our firebase-hosted website ([http://berkeley-met.web.app](http://berkeley-met.web.app)).

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

This is the command we will be using anytime we wish to work locally and want to view changes in real time.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

## Development (TODO)

This section will ideally eventually be a quick overview on how everything works within the project and how to use the development tools and technologies that constitue our stack (e.g. writing React code and using the Firebase integration).

Happy hacking!
