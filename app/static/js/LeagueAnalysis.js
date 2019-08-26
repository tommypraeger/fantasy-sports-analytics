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
      fetchInProgress: false,
      platform: '',
      sport: 'football',
      leagueId: '',
      year: '',
      swid: '',
      espn_s2: '',
      isPrivateLeague: false
    };
  }

  fetchLeague = (event) => {
    event.preventDefault();
    const self = this;
    this.setState({ fetchInProgress: true });
    axios.get('/api/v1/fantasy_league_analysis', {
        params: {
          platform: this.state.platform,
          sport: this.state.sport,
          league_id: this.state.leagueId,
          year: this.state.year,
          swid: this.state.swid,
          espn_s2: this.state.espn_s2
        }
      })
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

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value })
  }

  handleCheckboxChange = (event) => {
    this.setState({ [event.target.name]: event.target.checked });
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

    let espnAuth = '';
    if (this.state.isPrivateLeague) {
      espnAuth = (
        <div>
          <Form.Group>
              <Form.Label>SWID</Form.Label>
              <Form.Control
                name='swid'
                value={this.state.swid}
                onChange={this.handleChange}
              >
              </Form.Control>
          </Form.Group>
          <Form.Group>
              <Form.Label>espn_s2</Form.Label>
              <Form.Control
                name='espn_s2'
                value={this.state.espn_s2}
                onChange={this.handleChange}
              >
              </Form.Control>
          </Form.Group>
        </div>
      )
    }

    const espnForm = (
      <div>
        <Form.Group>
            <Form.Label>Sport</Form.Label>
            <Form.Control
              name='sport'
              value={this.state.sport}
              as='select'
              onChange={this.handleChange}
            >
              <option value='football'>Football</option>
              <option value='baseball'>Baseball</option>
            </Form.Control>
        </Form.Group>
        <Form.Group>
            <Form.Label>League ID</Form.Label>
            <Form.Control
              name='leagueId'
              value={this.state.leagueId}
              onChange={this.handleChange}
            >
            </Form.Control>
        </Form.Group>
        <Form.Group>
            <Form.Label>Year</Form.Label>
            <Form.Control
              name='year'
              value={this.state.year}
              onChange={this.handleChange}
            >
            </Form.Control>
        </Form.Group>
        <Form.Group>
            <Form.Check
              name='isPrivateLeague'
              value={this.state.isPrivateLeague}
              onChange={this.handleCheckboxChange}
              label='Is this a private league?'
            >
            </Form.Check>
        </Form.Group>
        {espnAuth}
      </div>
    );

    const sleeperForm = (
      <div>
        <Form.Group>
            <Form.Label>League ID</Form.Label>
            <Form.Control
              name='leagueId'
              value={this.state.leagueId}
              onChange={this.handleChange}
              placeholder='123456789012345678'
            >
            </Form.Control>
        </Form.Group>
      </div>
    );

    let form = '';
    switch (this.state.platform) {
      case 'espn':
        form = espnForm;
        break;
      case 'sleeper':
        form = sleeperForm;
        break;
    }

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
      <Form className='form' onSubmit={this.fetchLeague}>
        <Form.Group>
          <Form.Label>Platform</Form.Label>
          <Form.Control
            name='platform'
            value={this.state.platform}
            as='select'
            onChange={this.handleChange}
          >
            <option value='' disabled>Choose a platform...</option>
            <option value='espn'>ESPN</option>
            <option value='sleeper'>Sleeper</option>
          </Form.Control>
        </Form.Group>
        {form}
        <Button type='submit'>Submit</Button>
      </Form>
    );
  }

}

export default LeagueAnalysis;
