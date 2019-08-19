import React from 'react';
import ReactDOM from 'react-dom'
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import axios from 'axios';

axios.get('/api/v1/fantasy_league_analysis')
  .then(function (response) {
    console.log(response.data)
  })
  .catch(function (err) {
    console.error(err);
  });


function App() {
  return (
    <Router>
      <Route exact path="/" component={Home} />
    </Router>
  );
}

function Home() {
  return (
    <h1>Home</h1>
  )
}

ReactDOM.render(<App />, document.getElementById('app-container'));
