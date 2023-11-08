import AWS from "aws-sdk";

import getLeagueAnaylsisParams from "./league_analysis";
import awsCredentials from "./aws_credentials";

const lambda = new AWS.Lambda({
  accessKeyId: awsCredentials.ACCESS_KEY_ID,
  secretAccessKey: awsCredentials.SECRET_ACCESS_KEY,
  region: "us-east-2",
});

const getLambda = (method, params) => {
  const response = { lambda };
  if (method === "league-analysis" || method === "wakeup-league-analysis") {
    response.params = getLeagueAnaylsisParams(params, method);
  }
  return response;
};

export default getLambda;
