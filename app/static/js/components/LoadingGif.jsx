import React from 'react';

class LoadingGif extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fetchesInProgress: 0,
    };
  }

  incrementFetches = () => {
    this.setState((prevState) => ({ fetchesInProgress: prevState.fetchesInProgress + 1 }));
  }

  decrementFetches = () => {
    this.setState((prevState) => ({ fetchesInProgress: prevState.fetchesInProgress - 1 }));
  }

  render = () => {
    const { fetchesInProgress } = this.state;

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
}

export default LoadingGif;
