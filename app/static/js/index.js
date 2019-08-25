import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import LeagueAnalysis from './LeagueAnalysis';

function App() {
  return (
    <Router>
      <Route exact path='/' component={Home} />
      <Route path='/league-analysis' component={LeagueAnalysis} />
    </Router>
  );
}

function Home() {
  return (
    <Link to='/league-analysis'>League Analysis</Link>
  );
}

ReactDOM.render(<App />, document.getElementById('app-container'));
