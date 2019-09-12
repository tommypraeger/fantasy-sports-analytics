import React from 'react';
import PropTypes from 'prop-types';

function LoadingGif({ fetchesInProgress }) {
  const loadingGif = (
    <div className="lds-ring">
      <div />
      <div />
      <div />
      <div />
    </div>
  );
  return fetchesInProgress > 0
    ? loadingGif
    : <div />;
}
LoadingGif.propTypes = {
  fetchesInProgress: PropTypes.string.isRequired,
};

function incrementFetches(self) {
  self.setState((prevState) => ({ fetchesInProgress: prevState.fetchesInProgress + 1 }));
}

function decrementFetches(self) {
  self.setState((prevState) => ({ fetchesInProgress: prevState.fetchesInProgress - 1 }));
}

export {
  LoadingGif,
  incrementFetches,
  decrementFetches,
};
