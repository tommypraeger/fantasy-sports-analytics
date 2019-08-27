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
      //swid: '',
      espn_s2: '',
      isPrivateLeague: false,
      requestFailed: false,
      errorMessage: ''
    };
  }

  componentDidMount = () => {
    this.setState({ year: new Date().getFullYear() });
  }

  fetchLeague = (event) => {
    // Check form validation
    if (event.currentTarget.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
      event.currentTarget.classList.add('was-validated');
      return;
    }

    event.preventDefault();
    const self = this;

    // Make request to API
    this.setState({ fetchInProgress: true });
    axios.get('/api/v1/fantasy_league_analysis', {
        params: {
          platform: this.state.platform,
          sport: this.state.sport,
          league_id: this.state.leagueId,
          year: this.state.year,
          //swid: this.state.swid,
          espn_s2: this.state.espn_s2
        }
      })
      .then(function (response) {
        console.log(response.data);
        self.setState({
          league: response.data.league,
          teams: response.data.teams,
          fetchedLeague: true
        });
      })
      .catch(function (err) {
        console.error(err);
        self.setState({
          errorMessage: String(err),
          requestFailed: true
        });
      })
      .finally(function () {
        self.setState({ fetchInProgress: false });
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
          {/* SWID not needed apparently
            <Form.Group>
              <Form.Label>SWID</Form.Label>
              <Form.Control
                name='swid'
                value={this.state.swid}
                onChange={this.handleChange}
                placeholder='{123456AB-123D-5678-ABC4-123456789ABC}'
                required
              >
              </Form.Control>
          </Form.Group>*/}
          <Form.Group controlId='espn_s2'>
              <Form.Label>espn_s2</Form.Label>
              <Form.Control
                name='espn_s2'
                value={this.state.espn_s2}
                onChange={this.handleChange}
                placeholder='ADgDGFGDfgDFGDfgRTEFwecsYJUyrCWdcdsgRTHTbVEdSCdserVed...'
                required
              />
              <Form.Control.Feedback type='invalid'>
                Please provide the espn_s2 cookie for private leagues.
              </Form.Control.Feedback>
          </Form.Group>
        </div>
      )
    }

    let validYears = [];
    for (let i = this.state.year; i >= 2018; i--) {
      validYears.push(i);
    }

    const espnForm = (
      <div>
        <Form.Group controlId='espnSport'>
            <Form.Label>Sport</Form.Label>
            <Form.Control
              name='sport'
              value={this.state.sport}
              as='select'
              onChange={this.handleChange}
              required
            >
              <option value='football'>Football</option>
              <option value='baseball'>Baseball</option>
            </Form.Control>
        </Form.Group>
        <Form.Group controlId='espnLeagueId'>
            <Form.Label>League ID</Form.Label>
            <Form.Control
              name='leagueId'
              value={this.state.leagueId}
              onChange={this.handleChange}
              placeholder='12345678'
              required
            />
            <Form.Control.Feedback type='invalid'>
              Please provide a league ID.
            </Form.Control.Feedback>
        </Form.Group>
        <Form.Group controlId='espnYear'>
            <Form.Label>Year</Form.Label>
            <Form.Control
              name='year'
              value={this.state.year}
              as='select'
              onChange={this.handleChange}
              required
            >
              {
                validYears.map((year) => {
                  return (
                    <option value={year}>{year}</option>
                  );
                })
              }
            </Form.Control>
        </Form.Group>
        <Form.Group controlId='espnIsPrivateLeague'>
            <Form.Check
              name='isPrivateLeague'
              value={this.state.isPrivateLeague}
              onChange={this.handleCheckboxChange}
              label='This is a private league'
            >
            </Form.Check>
        </Form.Group>
        {espnAuth}
      </div>
    );

    const sleeperForm = (
      <div>
        <Form.Group controlId='sleeperLeagueId'>
            <Form.Label>League ID</Form.Label>
            <Form.Control
              name='leagueId'
              value={this.state.leagueId}
              onChange={this.handleChange}
              placeholder='123456789012345678'
              required
            />
            <Form.Control.Feedback type='invalid'>
              Please provide a league ID.
            </Form.Control.Feedback>
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

    if (this.state.requestFailed) {
      return (
        <div>
          {this.state.errorMessage}
        </div>
      );
    }

    if (this.state.fetchInProgress) {
      return loadingGif;
    }

    // Return config form
    return (
      <Form 
        className='form'
        noValidate
        onSubmit={this.fetchLeague}>
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
