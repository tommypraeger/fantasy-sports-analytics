const redToGreen = (stringPercent) => {
  let r;
  let g;
  const b = 0;

  const percent = parseFloat(stringPercent);
  if (percent < 50) {
    // red to yellow
    r = 255;
    g = Math.floor(255 * (percent / 50));
  } else {
    // yellow to green
    r = Math.floor(255 - (255 * ((percent - 50) / 50)));
    g = 255;
  }

  return `rgba(${r},${g},${b},0.5)`;
};

const colorMatchupsTable = () => {
  const matchupsTable = document.getElementById('team-matchups-table');
  const winPctIndex = 5;
  const wonIndex = 6;
  let tableChild;
  let tableRow;
  for (let i = 0; i < matchupsTable.children.length; i += 1) {
    tableChild = matchupsTable.children[i];
    if (tableChild.tagName === 'TBODY') {
      for (let j = 0; j < tableChild.children.length; j += 1) {
        tableRow = tableChild.children[j];
        // Color expected win percent column
        tableRow.children[winPctIndex].style.backgroundColor = (
          redToGreen(tableRow.children[winPctIndex].innerText)
        );
        // Color actual win column
        if (tableRow.children[wonIndex].innerText === 'Yes') {
          tableRow.children[wonIndex].style.backgroundColor = 'rgba(0,255,0,0.5)';
        } else if (tableRow.children[wonIndex].innerText === 'No') {
          tableRow.children[wonIndex].style.backgroundColor = 'rgba(255,0,0,0.5)';
        }
      }
    }
  }
};

// Create data object to pass to chart.js
const currentWinProbsGraphData = ({ teams, view }) => {
  const team = teams.find((currTeam) => view === currTeam.name);
  const winProbsData = team.win_total_probs.curr_probs.slice(0);
  const dataLength = winProbsData.length;
  const colors = Array(dataLength).fill('rgba(0, 85, 212, 0.8)');
  colors[team.win_total_probs.curr_wins] = 'rgba(212, 0, 0, 0.8)';
  const borderColors = Array(dataLength).fill('rgba(0, 85, 212, 1)');
  borderColors[team.win_total_probs.curr_wins] = 'rgba(212, 0, 0, 1)';
  return {
    labels: [...Array(dataLength).keys()],
    datasets: [{
      label: 'Chance of having # of wins through this week, actual wins in red',
      data: winProbsData,
      backgroundColor: colors,
      borderColor: borderColors,
      borderWidth: 1,
    }],
  };
};

// Create data object to pass to chart.js
const endWinProbsGraphData = ({ teams, view }) => {
  const team = teams.find((currTeam) => view === currTeam.name);
  const winProbsData = team.win_total_probs.end_probs.slice(0);
  const dataLength = winProbsData.length;
  const colors = Array(dataLength).fill('rgba(0, 85, 212, 0.8)');
  const borderColors = Array(dataLength).fill('rgba(0, 85, 212, 1)');
  return {
    labels: [...Array(dataLength).keys()],
    datasets: [{
      label: 'Chance of ending with # of wins',
      data: winProbsData,
      backgroundColor: colors,
      borderColor: borderColors,
      borderWidth: 1,
    }],
  };
};

export default {
  redToGreen,
  colorMatchupsTable,
  currentWinProbsGraphData,
  endWinProbsGraphData,
};
