const getLeagueAnalysisParams = ({
  platform, sport, leagueId, year, espnS2,
}) => ({
  FunctionName: 'arn:aws:lambda:us-east-2:911328362781:function:fantasy-sports-analytics',
  InvocationType: 'RequestResponse',
  Payload: JSON.stringify({
    platform, sport, leagueId, year, espnS2,
  }),
});

export default getLeagueAnalysisParams;
