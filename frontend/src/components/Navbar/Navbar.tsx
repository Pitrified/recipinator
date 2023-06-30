// Navbar and related components following
// https://www.geeksforgeeks.org/how-to-create-a-multi-page-website-using-react-js/

import React from "react";
import { Nav, NavLink, NavMenu } from "./Elements";

import "./Navbar.css";
 
const Navbar = () => {
    console.log("Navbar load");
    return (
        <>
            <Nav>
                <NavMenu>
                    {/* <NavLink to="/about" activeStyle> */}
                    <NavLink to="/">
                        Recipez
                    </NavLink>
                    <NavLink to="/about">
                        About
                    </NavLink>
                    <NavLink to="/dragme">
                        Drag sample
                    </NavLink>
                    <NavLink to="/searchme">
                        Search sample
                    </NavLink>
                    <NavLink to="/recipelist">
                        Recipe list
                    </NavLink>
                </NavMenu>
            </Nav>
        </>
    );
};
 
export default Navbar;