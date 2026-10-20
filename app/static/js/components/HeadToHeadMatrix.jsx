/* eslint-disable react/no-array-index-key */
import React from 'react';
import ReactTable from 'react-bootstrap/Table';
import PropTypes from 'prop-types';

import utils from '../pages/LeagueAnalysis/utils';

const formatRecord = ({ wins, losses, ties }) => (
  ties ? `${wins}-${losses}-${ties}` : `${wins}-${losses}`
);

const winPercent = ({ wins, losses, ties }) => {
  const games = wins + losses + ties;
  return games ? ((wins + ties / 2) / games) * 100 : 50;
};

// Sum a team's records against every opponent
const cumulativeRecord = (row) => row.filter(Boolean).reduce(
  (total, record) => ({
    wins: total.wins + record.wins,
    losses: total.losses + record.losses,
    ties: total.ties + record.ties,
  }),
  { wins: 0, losses: 0, ties: 0 },
);

const recordCell = (record, key, title) => (
  <td
    key={key}
    style={{ backgroundColor: utils.redToGreen(winPercent(record)) }}
    title={title}
  >
    {formatRecord(record)}
  </td>
);

const rotatedHeader = (name, key, className = '') => (
  <th key={key} className={`rotated-header ${className}`}>
    <div>
      <span>{name}</span>
    </div>
  </th>
);

// Rows are teams (y), columns are opponents (x).
// Each cell is the row team's record against the column opponent.
const HeadToHeadMatrix = ({ teams, records }) => (
  <ReactTable
    id="head-to-head-table"
    className="head-to-head-table"
    bordered
    variant="dark"
  >
    <thead>
      <tr>
        <th className="corner-cell">Team ↓ / Opponent →</th>
        {teams.map((opponent, x) => rotatedHeader(opponent, `header-${x}`))}
        {rotatedHeader('Total', 'header-total', 'total-cell')}
      </tr>
    </thead>
    <tbody>
      {teams.map((team, y) => (
        <tr key={`row-${y}`}>
          <th>{team}</th>
          {teams.map((opponent, x) => {
            const record = records[y][x];
            if (!record) {
              return <td key={`cell-${x}-${y}`} className="self-cell" />;
            }
            return recordCell(record, `cell-${x}-${y}`, `${team} vs. ${opponent}`);
          })}
          {recordCell(cumulativeRecord(records[y]), `total-${y}`, `${team} vs. everyone`)}
        </tr>
      ))}
    </tbody>
  </ReactTable>
);
HeadToHeadMatrix.propTypes = {
  teams: PropTypes.arrayOf(PropTypes.string).isRequired,
  records: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.object)).isRequired,
};

export default HeadToHeadMatrix;
