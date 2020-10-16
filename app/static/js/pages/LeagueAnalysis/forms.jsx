import React from 'react';
import Form from 'react-bootstrap/Form';

const espnForm = (validYears, {
  isPrivateLeague,
  setIsPrivateLeague,
  sport,
  setSport,
  leagueId,
  setLeagueId,
  year,
  setYear,
  espnS2,
  setEspnS2,
}) => (
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
    {!isPrivateLeague ? ''
      : (
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
      )}
  </div>
);

const sleeperForm = ({ leagueId, setLeagueId }) => (
  <div>
    <Form.Group controlId="sleeperLeagueId">
      <Form.Label>League ID</Form.Label>
      <div className="help-tip">
        <p>
            League ID is how Sleeper uniquely identifies fantasy leagues.
            Click
          {' '}
          <a href="/faqs#sleeper-league-id">here</a>
          {' '}
            for more information on how to find it.
        </p>
      </div>
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

export default {
  espnForm,
  sleeperForm,
};
