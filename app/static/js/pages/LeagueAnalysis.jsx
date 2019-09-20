/* eslint-disable react/prop-types */
import axios from 'axios';
import querySearch from 'stringquery';

import React from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';

import { LoadingGif, incrementFetches, decrementFetches } from '../components/LoadingGif';
import Table from '../components/Table';
import BarGraph from '../components/Graph';
import NavBar from '../components/NavBar';

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
    const { location } = this.props;
    if (location.search) {
      const urlParams = querySearch(location.search);
      this.setState({
        platform: urlParams.platform,
        sport: urlParams.sport,
        leagueId: urlParams.leagueId,
        year: urlParams.year,
        espnS2: urlParams.espnS2,
        view: decodeURI(urlParams.view),
      }, this.fetchLeague);
    } else {
      const currentYear = new Date().getFullYear();
      this.setState({
        currentYear,
        year: currentYear,
      });
    }
  }

  componentDidUpdate = () => {
    const { fetchedLeague, view } = this.state;
    if (fetchedLeague && view !== 'league') {
      this.colorMatchupsTable();
    }
  }

  colorMatchupsTable = () => {
    const matchupsTable = document.getElementById('team-matchups-table');
    const winPctIndex = 5;
    const wonIndex = 6;
    let tableChild;
    let tableRow;
    for (let i = 0; i < matchupsTable.children.length; i += 1) {
      tableChild = matchupsTable.children[i];
      if (tableChild.tagName === 'TBODY') {
        for (let j = 0; j < tableChild.children.length; j += 1) {
          tableRow = tableChild.children[j];
          // Color expected win percent column
          tableRow.children[winPctIndex].style.backgroundColor = (
            this.redToGreen(tableRow.children[winPctIndex].innerText)
          );
          // Color actual win column
          if (tableRow.children[wonIndex].innerText === 'Yes') {
            tableRow.children[wonIndex].style.backgroundColor = 'rgba(0,255,0,0.5)';
          } else if (tableRow.children[wonIndex].innerText === 'No') {
            tableRow.children[wonIndex].style.backgroundColor = 'rgba(255,0,0,0.5)';
          }
        }
      }
    }
  }

  redToGreen = (stringPercent) => {
    let r;
    let g;
    const b = 0;

    const percent = parseFloat(stringPercent);
    if (percent < 50) {
      // red to yellow
      r = 255;
      g = Math.floor(255 * (percent / 50));
    } else {
      // yellow to green
      r = Math.floor(255 - (255 * ((percent - 50) / 50)));
      g = 255;
    }

    return `rgba(${r},${g},${b},0.5)`;
  }

  // Check form validation
  validateLeagueInputs = (event) => {
    event.preventDefault();
    if (event.currentTarget.checkValidity() === false) {
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
      view,
    } = this.state;
    const { history } = this.props;
    const newUrl = `?platform=${platform}&sport=${sport}&leagueId=${leagueId}`
      + `&year=${year}&espnS2=${espnS2}&view=${view}`;
    history.push(newUrl);
    this.fetchLeague();
  }

  // Request league stats from API
  fetchLeague = () => {
    const {
      platform,
      sport,
      leagueId,
      year,
      espnS2,
    } = this.state;

    // Make request to API
    incrementFetches(this);
    const self = this;
    axios.get('api/v1/fantasy_league_analysis', {
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
        self.setState({
          league: response.data.league,
          teams: response.data.teams,
          fetchedLeague: true,
        });
      })
      .catch((err) => {
        self.setState({
          errorMessage: err.response.data.message,
          requestFailed: true,
        });
      })
      .finally(() => {
        decrementFetches(self);
      });
  }

  // Create data object to pass to chart.js
  currentWinProbsGraphData = () => {
    const { teams, view } = this.state;
    const team = teams.find((currTeam) => view === currTeam.name);
    const winProbsData = team.win_total_probs.curr_probs.slice(0);
    const dataLength = winProbsData.length;
    const colors = Array(dataLength).fill('rgba(0, 85, 212, 0.8)');
    colors[team.win_total_probs.curr_wins] = 'rgba(212, 0, 0, 0.8)';
    const borderColors = Array(dataLength).fill('rgba(0, 85, 212, 1)');
    borderColors[team.win_total_probs.curr_wins] = 'rgba(212, 0, 0, 1)';
    return {
      labels: [...Array(dataLength).keys()],
      datasets: [{
        label: 'Chance of having # of wins through this week, actual wins in red',
        data: winProbsData,
        backgroundColor: colors,
        borderColor: borderColors,
        borderWidth: 1,
      }],
    };
  }

  // Create data object to pass to chart.js
  endWinProbsGraphData = () => {
    const { teams, view } = this.state;
    const team = teams.find((currTeam) => view === currTeam.name);
    const winProbsData = team.win_total_probs.end_probs.slice(0);
    const dataLength = winProbsData.length;
    const colors = Array(dataLength).fill('rgba(0, 85, 212, 0.8)');
    const borderColors = Array(dataLength).fill('rgba(0, 85, 212, 1)');
    return {
      labels: [...Array(dataLength).keys()],
      datasets: [{
        label: 'Chance of ending with # of wins',
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
    this.setState({ view: viewName },
      () => {
        const {
          platform,
          sport,
          leagueId,
          year,
          espnS2,
          view,
        } = this.state;
        const { history } = this.props;
        const newUrl = `?platform=${platform}&sport=${sport}&leagueId=${leagueId}`
          + `&year=${year}&espnS2=${espnS2}&view=${view}`;
        history.push(newUrl);
      });
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

    let returnedPage;

    if (requestFailed) {
      returnedPage = (
        <div>
          {errorMessage}
          <br />
          <a href="/league-analysis">Try again</a>
        </div>
      );
    } else if (!fetchedLeague) {
      const validYears = [];
      for (let i = currentYear; i >= 2018; i -= 1) {
        validYears.push(i);
      }

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
              <div className="help-tip">
                <p>
                  espn_s2 is a cookie that ESPN uses for authentication.
                  I need to use it to access private leagues.
                  Click
                  {' '}
                  <a href="/faqs#espn-s2">here</a>
                  {' '}
                  for more information on how to find it.
                </p>
              </div>
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
            <div className="help-tip">
              <p>
                League ID is how ESPN uniquely identifies fantasy leagues.
                Click
                {' '}
                <a href="/faqs#espn-league-id">here</a>
                {' '}
                for more information on how to find it.
              </p>
            </div>
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
                  <option value={validYear} key={validYear}>{validYear}</option>
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

      // Return config form
      returnedPage = (
        <div>
          <LoadingGif fetchesInProgress={fetchesInProgress} />
          <Form
            className="form"
            noValidate
            onSubmit={this.validateLeagueInputs}
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
    } else if (fetchedLeague) {
      // Return league page
      const sideNav = (
        <Nav defaultActiveKey="/home" className="flex-column side-nav">
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
        'Actual Win?',
      ];
      const statsPage = view === 'league'
        ? (
          <div className="league-analysis-page">
            <h2>Expected Standings</h2>
            <Table
              id="league-standings-table"
              data={league.standings_table}
              columns={leagueStandingsColumns}
            />
          </div>
        )
        : (
          <div className="league-analysis-page">
            <h2>{view}</h2>
            <div className="win-probs-graph">
              <h3>Expected Win Distribution Through This Week</h3>
              <BarGraph
                data={this.currentWinProbsGraphData()}
                options={{
                  scales: {
                    yAxes: [{
                      ticks: {
                        callback(value) {
                          return `${value}%`;
                        },
                        beginAtZero: true,
                      },
                      scaleLabel: {
                        display: true,
                        labelString: 'Percent Chance',
                        fontSize: 18,
                      },
                    }],
                    xAxes: [{
                      ticks: {
                        beginAtZero: true,
                      },
                      scaleLabel: {
                        display: true,
                        labelString: 'Number of wins',
                        fontSize: 18,
                      },
                    }],
                  },
                }}
              />
            </div>
            <div className="win-probs-graph">
              <h3>Projected End Of Season Win Distribution</h3>
              <BarGraph
                data={this.endWinProbsGraphData()}
                options={{
                  scales: {
                    yAxes: [{
                      ticks: {
                        callback(value) {
                          return `${value}%`;
                        },
                        beginAtZero: true,
                      },
                      scaleLabel: {
                        display: true,
                        labelString: 'Percent Chance',
                        fontSize: 18,
                      },
                    }],
                    xAxes: [{
                      ticks: {
                        beginAtZero: true,
                      },
                      scaleLabel: {
                        display: true,
                        labelString: 'Number of wins',
                        fontSize: 18,
                      },
                    }],
                  },
                }}
              />
            </div>
            <h3>Matchup Data</h3>
            <Table
              id="team-matchups-table"
              data={teams.find((team) => view === team.name).matchup_table}
              columns={teamMatchupsColumns}
            />
          </div>
        );

      returnedPage = (
        <div>
          {sideNav}
          {statsPage}
        </div>
      );
    }

    return (
      <div>
        <NavBar />
        {returnedPage}
      </div>
    );
  }
}

export default LeagueAnalysis;
