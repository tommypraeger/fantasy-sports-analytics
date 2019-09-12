import React from 'react';
import ReactTable from 'react-bootstrap/Table';
import PropTypes from 'prop-types';

function Table({
  data, columns, id, className,
}) {
  return (
    <ReactTable id={id} className={className} striped bordered hover variant="dark">
      <thead>
        <tr>
          {columns.map((columnName) => (
            <th>{columnName}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr>
            {columns.map((columnName) => (
              <td>
                {row[columnName]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </ReactTable>
  );
}
Table.propTypes = {
  data: PropTypes.arrayOf(PropTypes.objectOf(PropTypes.number)).isRequired,
  columns: PropTypes.string.isRequired,
  id: PropTypes.string,
  className: PropTypes.string,
};
Table.defaultProps = {
  id: '',
  className: '',
};

export default Table;
