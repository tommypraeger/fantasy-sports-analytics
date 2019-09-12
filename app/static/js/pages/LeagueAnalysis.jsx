import React from 'react';
import axios from 'axios';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';

import { LoadingGif, incrementFetches, decrementFetches } from '../components/LoadingGif';
import Table from '../components/Table';
import BarGraph from '../components/Graph';

class LeagueAnalysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fetchedLeague: false,
      league: {},
      teams: [],
      view: 'league',
      platform: 'espn',
      sport: 'football',
      leagueId: '',
      currentYear: '',
      year: '',
      // swid: '',
      espnS2: '',
      isPrivateLeague: false,
      requestFailed: false,
      errorMessage: '',
      fetchesInProgress: 0,
    };
    this.loadingGif = React.createRef();
  }

  componentDidMount = () => {
    const currentYear = new Date().getFullYear();
    this.setState({
      currentYear,
      year: currentYear,
    });
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

    // Make request to API
    incrementFetches(this);
    const self = this;
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
        self.setState({
          league: response.data.league,
          teams: response.data.teams,
          fetchedLeague: true,
        });
      })
      .catch((err) => {
        // console.error(err);
        self.setState({
          errorMessage: String(err),
          requestFailed: true,
        });
      })
      .finally(() => {
        decrementFetches(self);
      });
  }

  currentWinProbsGraphData = () => {
    const { teams, view } = this.state;
    const team = teams.find((currTeam) => view === currTeam.name);
    const winProbsData = team.win_total_probs.curr_probs;
    const dataLength = winProbsData.length;
    const colors = Array(dataLength).fill('rgba(0, 85, 212, 0.5)');
    colors[team.win_total_probs.curr_wins] = 'rgba(212, 0, 0, 1)';
    const borderColors = Array(dataLength).fill('rgba(0, 85, 212, 0.5)');
    borderColors[team.win_total_probs.curr_wins] = 'rgba(212, 0, 0, 1)';
    return {
      labels: [...Array(dataLength).keys()],
      datasets: [{
        label: 'Test',
        data: winProbsData,
        backgroundColor: colors,
        borderColor: borderColors,
        borderWidth: 1,
      }],
    };
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  }

  handleCheckboxChange = (event) => {
    this.setState({ [event.target.name]: event.target.checked });
  }

  setView = (viewName) => {
    this.setState({ view: viewName });
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
      currentYear,
      fetchesInProgress,
      league,
      teams,
      view,
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
          <Form.Group controlId="espnS2">
            <Form.Label>espn_s2</Form.Label>
            <Form.Control
              name="espnS2"
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
    for (let i = currentYear; i >= 2018; i -= 1) {
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
      const sideNav = (
        <Nav defaultActiveKey="/home" className="flex-column">
          <Nav.Item
            onClick={() => this.setView('league')}
            eventKey="league"
          >
            League
          </Nav.Item>
          {
            teams.map((team) => (
              <Nav.Item
                onClick={() => this.setView(team.name)}
                eventKey={team.name}
              >
                {team.name}
              </Nav.Item>
            ))
          }
        </Nav>
      );

      const leagueStandingsColumns = [
        'Expected Ranking',
        'Name',
        'Expected Wins',
        'Expected Losses',
        'Actual Wins',
        'Win Differential',
        'Projected Wins',
        'Projected Losses',
        'Average Score',
      ];
      const teamMatchupsColumns = [
        'Week',
        'Points For',
        'Opponent',
        'Opponent Average Score',
        'Opponent Adj. Std. Dev.',
        'Expected Win %',
      ];
      const statsPage = view === 'league'
        ? (
          <div>
            <Table
              id="league-standings-table"
              data={league.standings_table}
              columns={leagueStandingsColumns}
            />
          </div>
        )
        : (
          <div>
            <Table
              className="team-matchups-table"
              data={teams.find((team) => view === team.name).matchup_table}
              columns={teamMatchupsColumns}
            />
            <BarGraph
              id={`current-win-probs-graph-${view}`}
              className="current-win-probs-graph"
              data={this.currentWinProbsGraphData}
            />
          </div>
        );

      return (
        <div>
          {sideNav}
          {statsPage}
        </div>
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
      <div>
        <LoadingGif fetchesInProgress={fetchesInProgress} />
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
              <option value="espn">ESPN</option>
              {/* <option value='sleeper'>Sleeper</option> */}
            </Form.Control>
          </Form.Group>
          {form}
          <Button type="submit">Submit</Button>
        </Form>
      </div>
    );
  }
}

export default LeagueAnalysis;
