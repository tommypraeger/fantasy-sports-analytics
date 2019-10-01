import React from 'react';
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  Switch,
} from 'react-router-dom';

// eslint-disable-next-line no-unused-vars
import styles from '../css/base.scss';
import LeagueAnalysis from './pages/LeagueAnalysis';
import FAQs from './pages/FAQs';

function NotFound() {
  return (
    <div>
      The page you are looking for does not exist.
    </div>
  );
}

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" render={() => <Redirect to="/league-analysis" />} />
        <Route path="/league-analysis" component={LeagueAnalysis} />
        <Route path="/faqs" component={FAQs} />
        <Route component={NotFound} />
      </Switch>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById('app-container'));
