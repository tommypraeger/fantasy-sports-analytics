import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

// eslint-disable-next-line no-unused-vars
import styles from '../css/base.scss';
import LeagueAnalysis from './pages/LeagueAnalysis';
import FAQs from './pages/FAQs';

function App() {
  return (
    <Router>
      <Route exact path="/" render={() => <Redirect push to="/league-analysis" />} />
      <Route path="/league-analysis" component={LeagueAnalysis} />
      <Route path="/faqs" component={FAQs} />
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById('app-container'));
