const getLeagueAnalysisParams = (
  { platform, sport, leagueId, year, espnS2 },
  method
) => ({
  FunctionName:
    "arn:aws:lambda:us-east-2:911328362781:function:fantasy-sports-analytics",
  InvocationType: "RequestResponse",
  Payload: JSON.stringify({
    method,
    platform,
    sport,
    leagueId,
    year,
    espnS2,
  }),
});

export default getLeagueAnalysisParams;
