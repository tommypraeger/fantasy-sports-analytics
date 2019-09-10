import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import styles from '../css/base.scss';
import LeagueAnalysis from './pages/LeagueAnalysis';

function Home() {
  return (
    <Link to="/league-analysis">League Analysis</Link>
  );
}

function App() {
  return (
    <Router>
      <Route exact path="/" component={Home} />
      <Route path="/league-analysis" component={LeagueAnalysis} />
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById('app-container'));
