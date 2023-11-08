import React from "react";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import { NavLink } from "react-router-dom";

const NavBar = () => (
  <Navbar bg="dark" variant="dark">
    <Navbar.Brand>
      <NavLink to="/" className="nav-link" activeClassName="nav-link-selected">
        Fantasy Sports Analytics
      </NavLink>
    </Navbar.Brand>
    <Nav className="mr-auto">
      <NavLink
        to="/league-analysis"
        className="nav-link"
        activeClassName="nav-link-selected"
      >
        League Analysis
      </NavLink>
      <NavLink
        to="/faqs"
        className="nav-link"
        activeClassName="nav-link-selected"
      >
        FAQs
      </NavLink>
    </Nav>
  </Navbar>
);

export default NavBar;
