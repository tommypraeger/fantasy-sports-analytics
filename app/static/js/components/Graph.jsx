import React from 'react';
import { Bar } from 'react-chartjs-2';

const BarGraph = ({ data, options }) => (
  <Bar
    data={data}
    options={options}
  />
);

export default BarGraph;
