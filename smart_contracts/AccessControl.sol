// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControl {
    // Define two roles: admin and user
    address public admin;
    mapping(address => bool) public users;

    // Events
    event AdminChanged(address indexed previousAdmin, address indexed newAdmin);
    event UserAdded(address indexed user);
    event UserRemoved(address indexed user);

    // Modifier to check if the caller is the admin
    modifier onlyAdmin() {
        require(msg.sender == admin, "AccessControl: caller is not the admin");
        _;
    }

    // Modifier to check if the caller is a user
    modifier onlyUser() {
        require(users[msg.sender], "AccessControl: caller is not a user");
        _;
    }

    constructor() {
        // The deployer of the contract is the initial admin
        admin = msg.sender;
        emit AdminChanged(address(0), admin);
    }

    // Function to change the admin
    function changeAdmin(address newAdmin) external onlyAdmin {
        require(newAdmin != address(0), "AccessControl: new admin is the zero address");
        emit AdminChanged(admin, newAdmin);
        admin = newAdmin;
    }

    // Function to add a new user
    function addUser(address user) external onlyAdmin {
        require(user != address(0), "AccessControl: user is the zero address");
        users[user] = true;
        emit UserAdded(user);
    }

    // Function to remove a user
    function removeUser(address user) external onlyAdmin {
        require(users[user], "AccessControl: user does not exist");
        users[user] = false;
        emit UserRemoved(user);
    }

    // Example of a function restricted to users
    function userFunction() external onlyUser {
        // Function logic for users
    }

    // Example of a function restricted to the admin
    function adminFunction() external onlyAdmin {
        // Function logic for admin
    }
}
