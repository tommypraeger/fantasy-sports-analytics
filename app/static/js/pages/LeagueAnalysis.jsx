/* eslint-disable react/prop-types */
import querySearch from 'stringquery';

import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';

import LoadingGif from '../components/LoadingGif';
import Table from '../components/Table';
import BarGraph from '../components/Graph';
import NavBar from '../components/NavBar';

import getLambda from '../api/v1';

// Request league stats from API
const fetchLeague = ({
  platform,
  sport,
  leagueId,
  year,
  espnS2,
  fetchesInProgress,
  setFetchesInProgress,
  setResponse,
}) => {
  setFetchesInProgress(fetchesInProgress + 1);
  const { lambda, params } = getLambda('league-analysis', {
    platform,
    sport,
    leagueId,
    year,
    espnS2,
  });
  lambda.invoke(params, (err, data) => {
    if (err) {
      setResponse(JSON.parse(err.Payload));
    }
    setResponse(JSON.parse(data.Payload));
  });
};

const setLeagueAfterFetch = ({
  response,
  fetchesInProgress,
  setErrorMessage,
  setRequestFailed,
  setLeague,
  setTeams,
  setFetchedLeague,
  setFetchesInProgress,
}) => {
  if (response.errorMessage) {
    setErrorMessage(response.errorMessage);
    setRequestFailed(true);
  } else {
    setLeague(response.league);
    setTeams(response.teams);
    setFetchedLeague(true);
  }
  setFetchesInProgress(fetchesInProgress - 1);
};

const redToGreen = (stringPercent) => {
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
};

const colorMatchupsTable = () => {
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
          redToGreen(tableRow.children[winPctIndex].innerText)
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
};

// Check form validation
const validateLeagueInputs = (event, state) => {
  event.preventDefault();
  if (event.currentTarget.checkValidity() === false) {
    event.stopPropagation();
    event.currentTarget.classList.add('was-validated');
    return;
  }

  const newUrl = `?platform=${state.platform}&sport=${state.sport}&leagueId=${state.leagueId}`
      + `&year=${state.year}&espnS2=${state.espnS2}&view=${state.view}`;
  window.history.pushState({}, '', newUrl);
  fetchLeague(state);
};

// Reset league info state and reload
const resetLeague = () => {
  window.location = window.location.pathname;
};

// Create data object to pass to chart.js
const currentWinProbsGraphData = ({ teams, view }) => {
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
};

// Create data object to pass to chart.js
const endWinProbsGraphData = ({ teams, view }) => {
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
};

const setViewAndUpdateUrl = (view, setView, state) => {
  setView(view);
  const newUrl = `?platform=${state.platform}&sport=${state.sport}`
      + `&leagueId=${state.leagueId}&year=${state.year}`
      + `&espnS2=${state.espnS2}&view=${view}`;
  window.history.pushState({}, '', newUrl);
};

const LeagueAnalysis = () => {
  const [fetchedLeague, setFetchedLeague] = useState(false);
  const [league, setLeague] = useState({});
  const [teams, setTeams] = useState([]);
  const [view, setView] = useState('league');
  const [platform, setPlatform] = useState('espn');
  const [sport, setSport] = useState('football');
  const [leagueId, setLeagueId] = useState('');
  const [currentYear, setCurrentYear] = useState('');
  const [year, setYear] = useState('');
  const [espnS2, setEspnS2] = useState('');
  const [isPrivateLeague, setIsPrivateLeague] = useState(false);
  const [requestFailed, setRequestFailed] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [fetchesInProgress, setFetchesInProgress] = useState(0);
  const [response, setResponse] = useState({});

  const state = {
    fetchedLeague,
    setFetchedLeague,
    league,
    setLeague,
    teams,
    setTeams,
    view,
    setView,
    platform,
    setPlatform,
    sport,
    setSport,
    leagueId,
    setLeagueId,
    currentYear,
    setCurrentYear,
    year,
    setYear,
    espnS2,
    setEspnS2,
    isPrivateLeague,
    setIsPrivateLeague,
    requestFailed,
    setRequestFailed,
    errorMessage,
    setErrorMessage,
    fetchesInProgress,
    setFetchesInProgress,
    response,
    setResponse,
  };

  useEffect(() => {
    setCurrentYear(new Date().getFullYear());
    if (window.location.search) {
      const urlParams = querySearch(window.location.search);
      setPlatform(urlParams.platform);
      setSport(urlParams.sport);
      setLeagueId(urlParams.leagueId);
      setYear(urlParams.year);
      setEspnS2(urlParams.espnS2);
      setView(decodeURI(urlParams.view));
    } else {
      setYear(new Date().getFullYear());
    }
  }, []);

  useEffect(() => {
    if (window.location.search
        && platform && sport && leagueId && year
        && (platform !== 'espn' || !isPrivateLeague || espnS2)) {
      fetchLeague(state);
    }
  }, [platform, sport, leagueId, year, espnS2, isPrivateLeague]);

  useEffect(() => {
    if (response && Object.keys(response).length) {
      setLeagueAfterFetch(state);
    }
  }, [response]);

  useEffect(() => {
    if (fetchedLeague && view !== 'league') {
      colorMatchupsTable();
    }
  }, [fetchedLeague, view]);

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
              onChange={(event) => setEspnS2(event.target.value)}
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
            onChange={(event) => setSport(event.target.value)}
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
            onChange={(event) => setLeagueId(event.target.value)}
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
            onChange={(event) => setYear(event.target.value)}
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
            onChange={(event) => setIsPrivateLeague(event.target.checked)}
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
            onChange={(event) => setLeagueId(event.target.value)}
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
          onSubmit={(event) => validateLeagueInputs(event, state)}
        >
          <Form.Group>
            <Form.Label>Platform</Form.Label>
            <Form.Control
              name="platform"
              value={platform}
              as="select"
              onChange={(event) => setPlatform(event.target.value)}
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
          onClick={() => setViewAndUpdateUrl('league', setView, state)}
        >
            League
        </Nav.Item>
        {
          teams.map((team) => (
            <Nav.Item
              onClick={() => setViewAndUpdateUrl(team.name, setView, state)}
              key={team.name}
            >
              {team.name}
            </Nav.Item>
          ))
        }
      </Nav>
    );

    const resetLeagueButton = (
      <Button
        variant="dark"
        onClick={resetLeague}
        className="reset-league-btn"
      >
          Re-enter League Info
      </Button>
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
          <div className="page-title">
            <h2>Expected Standings</h2>
            {resetLeagueButton}
          </div>
          <Table
            id="league-standings-table"
            data={league.standings_table}
            columns={leagueStandingsColumns}
          />
        </div>
      )
      : (
        <div className="league-analysis-page">
          <div className="page-title">
            <h2>{view}</h2>
            {resetLeagueButton}
          </div>
          <div className="win-probs-graph">
            <h3>Expected Win Distribution Through This Week</h3>
            <BarGraph
              data={currentWinProbsGraphData(state)}
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
              data={endWinProbsGraphData(state)}
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
};

export default LeagueAnalysis;
