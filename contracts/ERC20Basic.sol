pragma solidity ^0.4.18;


contract ERC20Basic {
    function totalSupply() public view returns (uint256);
    function balanceOf(address who) public view returns (uint256);
    function transfer(address to, uint256 value) public returns (bool);
    function burn(uint256 value) public returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Buy(address indexed from, address indexed to, uint256 value, uint256 price);
    event Sell(address indexed from, address indexed to, uint256 value, uint256 price);
    event FrozenFunds(address target, bool frozen);
    event Funded(address indexed owner, uint256 value);
    event Burn(address indexed burner, uint256 value);
}