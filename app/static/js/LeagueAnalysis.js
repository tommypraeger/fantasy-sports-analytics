import React from 'react';
import axios from 'axios';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import FormCheck from 'react-bootstrap/FormCheck';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class LeagueAnalysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fetchedLeague: false,
      league: {},
      teams: [],
      fetchInProgress: false
    };
  }

  fetchLeague = () => {
    const self = this;
    this.setState({ fetchInProgress: true });
    axios.get('/api/v1/fantasy_league_analysis')
      .then(function (response) {
        console.log(response.data);
        self.setState({ league: response.data.league });
        self.setState({ teams: response.data.teams });
        self.setState({ fetchInProgress: false });
        self.setState({ fetchedLeague: true });
      })
      .catch(function (err) {
        console.error(err);
      });
  }

  render() {

    const loadingGif = (
      <div class="lds-ring">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    );

    // Return league page
    if (this.state.fetchedLeague) {
      return (
        <div>Hi</div>
      );
    }

    if (this.state.fetchInProgress) {
      return loadingGif;
    }

    // Return config form
    return (
      <Form className='form'>
        <Form.Group>
          <Form.Label>Platform</Form.Label>
          <Form.Control as='select'>
            <option>ESPN</option>
          </Form.Control>
        </Form.Group>
      </Form>
    );
  }

}

export default LeagueAnalysis;
