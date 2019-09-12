import React from 'react';
import PropTypes from 'prop-types';
import { Bar } from 'react-chartjs-2';

function BarGraph({
  data, options, id, className,
}) {
  console.log(data);
  return (
    <Bar
      id={id}
      className={className}
      data={data}
      options={options}
    />
  );
}
BarGraph.propTypes = {
  data: PropTypes.objectOf(PropTypes.any).isRequired,
  options: PropTypes.objectOf(PropTypes.any),
  id: PropTypes.string.isRequired,
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
