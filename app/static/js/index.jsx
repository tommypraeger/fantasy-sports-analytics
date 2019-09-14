import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Link, Redirect } from 'react-router-dom';

// eslint-disable-next-line no-unused-vars
import styles from '../css/base.scss';
import LeagueAnalysis from './pages/LeagueAnalysis';

function App() {
  return (
    <Router>
      <Route exact path="/" render={() => <Redirect push to="/league-analysis" />} />
      <Route path="/league-analysis" component={LeagueAnalysis} />
    </Router>
  );
}

// eslint-disable-next-line no-undef
ReactDOM.render(<App />, document.getElementById('app-container'));
