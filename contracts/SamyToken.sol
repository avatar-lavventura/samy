pragma solidity ^0.4.18;

import "./StandardToken.sol";

/**
* @title SimpleToken
* @dev Very simple ERC20 Token example, where all tokens are pre-assigned to the creator.
* Note they can later distribute these tokens as they wish using `transfer` and other
* `StandardToken` functions.
*/
contract SamyToken is StandardToken {

    string public constant name = "SAMY";
    string public constant symbol = "SMY";
    uint8 public constant decimals = 18;
    uint256 public constant initialSupply = 1000000000 * (10 ** uint256(decimals));

    /**
     * @dev Constructor that gives msg.sender all of existing tokens.
     */
    function SamyToken() public {
        totalSupply_ = initialSupply;
        balances[msg.sender] = initialSupply;
        Transfer(0x0, msg.sender, initialSupply);
    }
}
