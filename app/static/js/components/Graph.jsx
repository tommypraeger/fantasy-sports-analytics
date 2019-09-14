import React from 'react';
import PropTypes from 'prop-types';
import { Bar } from 'react-chartjs-2';

function BarGraph({
  data, options,
}) {
  return (
    <Bar
      data={data}
      options={options}
    />
  );
}
BarGraph.propTypes = {
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  options: PropTypes.objectOf(PropTypes.any),
};
BarGraph.defaultProps = {
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
        },
      }],
    },
  },
};

export default BarGraph;
