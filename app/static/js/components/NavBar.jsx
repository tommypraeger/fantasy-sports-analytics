import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { NavLink } from 'react-router-dom';

function NavBar() {
  return (
    <Navbar bg="dark" variant="dark">
      <Navbar.Brand href="/">Fantasy Sports Analytics</Navbar.Brand>
      <Nav className="mr-auto">
        <Nav.Link>
          <NavLink
            to="/league-analysis"
            className="nav-link"
            activeClassName="nav-link-selected"
          >
            League Analysis
          </NavLink>
        </Nav.Link>
        <Nav.Link>
          <NavLink
            to="/faqs"
            className="nav-link"
            activeClassName="nav-link-selected"
          >
            FAQs
          </NavLink>
        </Nav.Link>
      </Nav>
    </Navbar>
  );
}

export default NavBar;
