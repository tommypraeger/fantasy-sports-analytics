import React from 'react';
import PropTypes from 'prop-types';
import { Bar } from 'react-chartjs-2';

function BarGraph({
  data, options, className,
}) {
  return (
    <Bar
      className={className}
      data={data}
      options={options}
    />
  );
}
BarGraph.propTypes = {
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  options: PropTypes.objectOf(PropTypes.any),
  className: PropTypes.string,
};
BarGraph.defaultProps = {
  className: '',
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
