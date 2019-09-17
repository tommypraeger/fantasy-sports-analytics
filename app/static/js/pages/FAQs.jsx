import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import NavBar from '../components/NavBar';

import espnLeagueId from '../../images/espn_league_id.png';
import viewCookies from '../../images/view_cookies.png';
import viewCookies2 from '../../images/view_cookies2.png';
import espnS2 from '../../images/espn_s2.png';
import leagueExample from '../../images/league_example.png';
import winDistExample from '../../images/win_dist_graph_example.png';
import matchupDataExample from '../../images/matchup_data_example.png';

function FAQs() {
  const defaultActive = 'how-calculate';
  const active = window.location.hash.split('#')[1] || defaultActive;
  return (
    <div>
      <NavBar />
      <Accordion id="faqs" defaultActiveKey={active}>
        <Card className="faq">
          <Accordion.Toggle as={Card.Header} eventKey="how-calculate">
            How do I calculate expected wins?
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="how-calculate">
            <Card.Body>
              <b>Expected win percentage of past games</b>
              <br />
              For each week, I treat your opponent&apos;s score as a random variable and calculate
              {' '}
              their average score and the standard deviation of the their scores. I then find the
              {' '}
              probability that the random variable representing their score is lower than
              {' '}
              what you scored that week. That probability as a percentage is your expected
              {' '}
              win percentage for that matchup. I do not take your opponent&apos;s actual score that
              {' '}
              week into account, as expected win percentage is supposed to account for you not
              {' '}
              having any control over how your opponent performs compared to average.
              <br />
              <br />
              <b>Expected win percentage of future games</b>
              <br />
              For future matchups, I perform the same calculation as for past matchups, except
              {' '}
              for one key difference. I can&apos;t use your actual score, so I also create a random
              {' '}
              variable out of your score. I then treat the two random variables (representing
              {' '}
              your score and your opponent&apos;s score) as independent and create a new random
              {' '}
              variable equal to yours minus their, according to the
              {' '}
              <a href="https://www.khanacademy.org/math/ap-statistics/random-variables-ap/
                       combining-random-variables/a/combining-random-variables-article"
              >
                rules of subtracting independent random variables
              </a>
              . I then find the probability of the random variable being greater than zero,
              {' '}
              and that probability as a percentage is the expected win percentage for that
              {' '}
              future matchup.
              <br />
              <br />
              <b>Expected wins</b>
              <br />
              To find expected wins, I sum up the expected win probability of each past matchup.
              <br />
              <br />
              <b>Projected wins</b>
              <br />
              To find projected wins, I sum up the expected win probability of each future matchup
              {' '}
              and add that to your current win total.
              <br />
              <br />
              <b>Expected win distribution</b>
              <br />
              To find expected win distribution, I treat all past expected win probabilities as a
              {' '}
              <a href="https://en.wikipedia.org/wiki/Poisson_binomial_distribution">
                Poission binomial distribution
              </a>
              . I then loop over each of
              {' '}
              <i>n</i>
              {' '}
              possible amount of wins and figure out the probability that there are exactly
              {' '}
              <i>n</i>
              {' '}
              wins, given your expected win probabilities.
              <br />
              <br />
              For projected wins, I do the same process, except I use future win expectancies.
              {' '}
              I figure the probability of ending with each number of wins, given how many wins
              {' '}
              you currently have.
            </Card.Body>
          </Accordion.Collapse>
        </Card>
        <Card className="faq">
          <Accordion.Toggle as={Card.Header} eventKey="how-calculate">
            Wait, doesn&apos;t that violate a ton of statistical assumptions?
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="how-calculate">
            <Card.Body>
              Well, yes, but it&apos;s no fun if I don&apos;t violate any statistical assumptions!
              <br />
              Fantasy scores cannot be accurately represented as random variables

              for a slew of reasons (injuries, varying lineups, owner effort), and that I am

              using a very small sample size for scores, so I try to reduce the confidence

              of the win probabilities by slightly adjusting the standard deviation of the scores

              upwards, with bigger adjustments earlier in the season.
            </Card.Body>
          </Accordion.Collapse>
        </Card>
        <Card className="faq">
          <Accordion.Toggle as={Card.Header} eventKey="espn-league-id">
            How do you figure out your ESPN league ID?
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="espn-league-id">
            <Card.Body>
              You can find your league ID by going to your league home on ESPN and looking
              {' '}
              at the URL for the leagueId.
              <br />
              <img src={espnLeagueId} alt="ESPN league ID example" />
            </Card.Body>
          </Accordion.Collapse>
        </Card>
        <Card className="faq">
          <Accordion.Toggle as={Card.Header} eventKey="espn-s2">
            How do you figure out your espn_s2?
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="espn-s2">
            <Card.Body>
              Here are instructions for Chrome. First, navigate to the ESPN website. Then,
              {' '}
              click the lock to the left of the URL.
              {' '}
              <br />
              <img src={viewCookies} alt="Click lock example" />
              <br />
              Then, click &quot;Cookies&quot;.
              <br />
              <img src={viewCookies2} alt="Open cookies example" width="320" />
              <br />
              Then, scroll down to espn.com and find the espn_s2 cookie. Copy and paste the whole
              {' '}
              thing from the &quot;Content&quot; field.
              <br />
              <img src={espnS2} alt="espn_s2 example" width="441" />
              <br />
              It is really long, much longer than you can see in the screenshot, so make sure
              {' '}
              you get all of it.
              <br />
              This is just a cookie ESPN uses for authentication and I can&apos;t access private
              {' '}
              leagues without. I promise I can&apos;t actually do anything malicious with it :)
            </Card.Body>
          </Accordion.Collapse>
        </Card>
        <Card className="faq">
          <Accordion.Toggle as={Card.Header} eventKey="other-platforms-sports">
            Am I planning on supporting other platforms/sports?
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="other-platforms-sports">
            <Card.Body>
              Yes, but no promises on when those come. I unfortunately don&apos;t have a ton
              {' '}
              of time to work on this. Hopefully, I can also add more pages besides just
              {' '}
              league analysis.
            </Card.Body>
          </Accordion.Collapse>
        </Card>
        <Card className="faq">
          <Accordion.Toggle as={Card.Header} eventKey="reenter-form">
            Do you have to reenter the form inputs every time you view a league?
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="reenter-form">
            <Card.Body>
              You can bookmark the URL after the league analysis page loads
              {' '}
              (i.e. when all the URL parameters are visible), but I do not actually store
              {' '}
              any data. If this site gains traction, I&apos;ll consider allowing users
              {' '}
              to create accounts and save leagues.
            </Card.Body>
          </Accordion.Collapse>
        </Card>
        <Card className="faq">
          <Accordion.Toggle as={Card.Header} eventKey="league-analysis-examples">
            Do you have any examples of what it might look like before I do it for my league?
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="league-analysis-examples">
            <Card.Body>
              Of course! Here are some screenshots pulled from one of my leagues
              {' '}
              (with team names covered for privacy).
              <br />
              <br />
              <img src={leagueExample} alt="League example" width="1088" />
              <br />
              <br />
              <img src={winDistExample} alt="Win distribution graph example" width="1036" />
              <br />
              <br />
              <img src={matchupDataExample} alt="Matchup data example" width="1007" />
            </Card.Body>
          </Accordion.Collapse>
        </Card>
      </Accordion>
    </div>
  );
}

export default FAQs;
