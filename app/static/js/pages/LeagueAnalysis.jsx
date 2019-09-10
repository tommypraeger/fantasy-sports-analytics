import React from 'react';
import axios from 'axios';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

class LeagueAnalysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fetchedLeague: false,
      league: {},
      teams: [],
      platform: '',
      sport: 'football',
      leagueId: '',
      year: '',
      // swid: '',
      espnS2: '',
      isPrivateLeague: false,
      requestFailed: false,
      errorMessage: '',
    };
    this.loadingGif = React.createRef();
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

    const {
      platform,
      sport,
      leagueId,
      year,
      espnS2,
    } = this.state;

    event.preventDefault();

    const {
      setState,
      loadingGif,
    } = this;

    // Make request to API
    this.loadingGif.current.incrementFetches();
    axios.get('/api/v1/fantasy_league_analysis', {
      params: {
        platform,
        sport,
        league_id: leagueId,
        year,
        // swid: swid,
        espn_s2: espnS2,
      },
    })
      .then((response) => {
        // console.log(response.data);
        setState({
          league: response.data.league,
          teams: response.data.teams,
          fetchedLeague: true,
        });
      })
      .catch((err) => {
        // console.error(err);
        setState({
          errorMessage: String(err),
          requestFailed: true,
        });
      })
      .finally(() => {
        loadingGif.current.decrementFetches();
      });
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  }

  handleCheckboxChange = (event) => {
    this.setState({ [event.target.name]: event.target.checked });
  }

  render() {
    const {
      isPrivateLeague,
      espnS2,
      year,
      fetchedLeague,
      errorMessage,
      requestFailed,
      platform,
      leagueId,
      sport,
    } = this.state;

    let espnAuth = '';
    if (isPrivateLeague) {
      espnAuth = (
        <div>
          {/* SWID not needed apparently
            <Form.Group>
              <Form.Label>SWID</Form.Label>
              <Form.Control
                name='swid'
                value={swid}
                onChange={this.handleChange}
                placeholder='{123456AB-123D-5678-ABC4-123456789ABC}'
                required
              >
              </Form.Control>
          </Form.Group> */}
          <Form.Group controlId="espn_s2">
            <Form.Label>espn_s2</Form.Label>
            <Form.Control
              name="espn_s2"
              value={espnS2}
              onChange={this.handleChange}
              placeholder="ADgDGFGDfgDFGDfgRTEFwecsYJUyrCWdcdsgRTHTbVEdSCdserVed..."
              required
            />
            <Form.Control.Feedback type="invalid">
              Please provide the espn_s2 cookie for private leagues.
            </Form.Control.Feedback>
          </Form.Group>
        </div>
      );
    }

    const validYears = [];
    for (let i = year; i >= 2018; i -= 1) {
      validYears.push(i);
    }

    const espnForm = (
      <div>
        <Form.Group controlId="espnSport">
          <Form.Label>Sport</Form.Label>
          <Form.Control
            name="sport"
            value={sport}
            as="select"
            onChange={this.handleChange}
            required
          >
            <option value="football">Football</option>
            <option value="baseball">Baseball</option>
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="espnLeagueId">
          <Form.Label>League ID</Form.Label>
          <Form.Control
            name="leagueId"
            value={leagueId}
            onChange={this.handleChange}
            placeholder="12345678"
            required
          />
          <Form.Control.Feedback type="invalid">
            Please provide a league ID.
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group controlId="espnYear">
          <Form.Label>Year</Form.Label>
          <Form.Control
            name="year"
            value={year}
            as="select"
            onChange={this.handleChange}
            required
          >
            {
              validYears.map((validYear) => (
                <option value={validYear}>{validYear}</option>
              ))
            }
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="espnIsPrivateLeague">
          <Form.Check
            name="isPrivateLeague"
            value={isPrivateLeague}
            onChange={this.handleCheckboxChange}
            label="This is a private league"
          >
          </Form.Check>
        </Form.Group>
        {espnAuth}
      </div>
    );

    const sleeperForm = (
      <div>
        <Form.Group controlId="sleeperLeagueId">
          <Form.Label>League ID</Form.Label>
          <Form.Control
            name="leagueId"
            value={leagueId}
            onChange={this.handleChange}
            placeholder="123456789012345678"
            required
          />
          <Form.Control.Feedback type="invalid">
            Please provide a league ID.
          </Form.Control.Feedback>
        </Form.Group>
      </div>
    );

    let form = '';
    switch (platform) {
      case 'espn':
        form = espnForm;
        break;
      case 'sleeper':
        form = sleeperForm;
        break;
      default:
        form = espnForm;
    }

    // Return league page
    if (fetchedLeague) {
      return (
        <div>Hi</div>
      );
    }

    if (requestFailed) {
      return (
        <div>
          {errorMessage}
        </div>
      );
    }

    // Return config form
    return (
      <Form
        className="form"
        noValidate
        onSubmit={this.fetchLeague}
      >
        <Form.Group>
          <Form.Label>Platform</Form.Label>
          <Form.Control
            name="platform"
            value={platform}
            as="select"
            onChange={this.handleChange}
          >
            <option value="" disabled>Choose a platform...</option>
            <option value="espn">ESPN</option>
            {/* <option value='sleeper'>Sleeper</option> */}
          </Form.Control>
        </Form.Group>
        {form}
        <Button type="submit">Submit</Button>
      </Form>
    );
  }
}

export default LeagueAnalysis;
