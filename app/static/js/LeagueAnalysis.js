import React from 'react';
import axios from 'axios';

class LeagueAnalysis extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          league: {},
          teams: []
      };

      this.componentDidMount = this.componentDidMount.bind(this);
  }

  componentDidMount() {
    const self = this;
    axios.get('/api/v1/fantasy_league_analysis')
      .then(function (response) {
        console.log(response.data);
        self.setState({league: response.data.league});
        self.setState({teams: response.data.teams});
      })
      .catch(function (err) {
        console.error(err);
      });
  }

  render() {

    const x = Object.keys(this.state.league).length?
      this.state.league.name : 'fuck';

    return (
        <div>
          {x}
        </div>
    );
  }

}

export default LeagueAnalysis;
