/* eslint-disable react/no-array-index-key */
import React from "react";
import ReactTable from "react-bootstrap/Table";
import PropTypes from "prop-types";

const Table = ({ data, columns, id, className }) => (
  <ReactTable
    id={id}
    className={className}
    striped
    bordered
    hover
    variant="dark"
  >
    <thead>
      <tr>
        {columns.map((columnName, i) => (
          <th key={`header-${i}`}>{columnName}</th>
        ))}
      </tr>
    </thead>
    <tbody>
      {data.map((row, i) => (
        <tr key={`row-${i}`}>
          {columns.map((columnName, j) => (
            <td key={`cell-${i * j + j}`}>{row[columnName]}</td>
          ))}
        </tr>
      ))}
    </tbody>
  </ReactTable>
);
Table.propTypes = {
  data: PropTypes.arrayOf(PropTypes.objectOf(PropTypes.any)).isRequired,
  columns: PropTypes.arrayOf(PropTypes.string).isRequired,
  id: PropTypes.string,
  className: PropTypes.string,
};
Table.defaultProps = {
  id: "",
  className: "",
};

export default Table;
