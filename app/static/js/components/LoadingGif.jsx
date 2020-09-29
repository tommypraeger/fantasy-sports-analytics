import React from 'react';

const LoadingGif = ({ fetchesInProgress }) => {
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
};

export default LoadingGif;
