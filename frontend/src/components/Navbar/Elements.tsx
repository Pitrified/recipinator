import { NavLink as Link } from "react-router-dom";

import React from "react";

const Nav = ({ children }) => {
  return <nav className="nav">{children}</nav>;
};

const NavMenu = ({ children }) => {
  return <div className="nav-menu">{children}</div>;
};

const NavLink = ({ to, children }) => {
  return <Link to={to} className="nav-link">{children}</Link>;
};

export { Nav, NavMenu, NavLink };
