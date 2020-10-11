/* eslint-disable react/prop-types */
import querySearch from 'stringquery';

import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';

import LoadingGif from '../../components/LoadingGif';
import Table from '../../components/Table';
import BarGraph from '../../components/Graph';
import NavBar from '../../components/NavBar';

import getLambda from '../../api/v1';

import forms from './forms';
import utils from './utils';

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
      utils.colorMatchupsTable();
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

    let form = '';
    switch (platform) {
      case 'espn':
        form = forms.espnForm(validYears, state);
        break;
      case 'sleeper':
        form = forms.sleeperForm(state);
        break;
      default:
        form = forms.espnForm(validYears, state);
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
              <option value="sleeper">Sleeper</option>
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
    const barGraphOptions = {
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
    };
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
              data={utils.currentWinProbsGraphData(state)}
              options={barGraphOptions}
            />
          </div>
          <div className="win-probs-graph">
            <h3>Projected End Of Season Win Distribution</h3>
            <BarGraph
              data={utils.endWinProbsGraphData(state)}
              options={barGraphOptions}
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
