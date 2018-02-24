pragma solidity ^0.4.18;

import "./ERC20Basic.sol";
import "./SafeMath.sol";
import "./Ownable.sol";

/**
* @title Basic token
* @dev Basic version of StandardToken, with no allowances.
*/
contract BasicToken is ERC20Basic, Ownable {

    using SafeMath for uint256;

    mapping(address => uint256) balances;
    mapping(address => bool) frozenAccount;

    uint256 totalSupply_;

    uint256 minBalanceForAccounts;
    uint256 public sellPrice;
    uint256 public buyPrice;
    bool public isActive = false;
    bool public isTradable = false;

    modifier isRunning {
        assert(isActive);
        _;
    }

    modifier isExchange {
        assert(isTradable);
        _;
    }

    modifier validAddress {
        assert(0x0 != msg.sender);
        _;
    }

    /**
    * @dev total number of tokens in existence
    */
    function totalSupply() public view returns (uint256) {
        return totalSupply_;
    }


    /**
    * @dev transfer token for a specified address
    * @param _to The address to transfer to.
    * @param _value The amount to be transferred.
    */
    function transfer(address _to, uint256 _value) isRunning validAddress public returns (bool) {
        require(_to != address(0));
        require(_value <= balances[msg.sender]);
        if (msg.sender.balance < minBalanceForAccounts) {
            uint256 amount = minBalanceForAccounts.sub(msg.sender.balance);
            amount = amount.div(sellPrice);
            sell(amount);
        }
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }

    /**
    * @dev Gets the balance of the specified address.
    * @param _owner The address to query the the balance of.
    * @return An uint256 representing the amount owned by the passed address.
    */
    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    /**
    * @dev Burns a specific amount of tokens.
    * @param _value The amount of token to be burned.
    */
    function burn(uint256 _value) public returns (bool) {
        require(_value <= balances[msg.sender]);
        // no need to require value <= totalSupply, since that would imply the
        // sender's balance is greater than the totalSupply, which *should* be an assertion failure

        address burner = msg.sender;
        balances[burner] = balances[burner].sub(_value);
        totalSupply_ = totalSupply_.sub(_value);
        Burn(burner, _value);
        return true;
    }

    /**
    * @dev Sets Minimum Balance for Accounts in Finney
    * @param _value The minimum allowable balance in finny.
    */
    function setMinBalance(uint256 _value) onlyOwner public {
        minBalanceForAccounts = _value * 1 finney;
    }

    /**
    * @dev Transfers SMY
    * @param _from From Address
    * @param _to To Address
    * @param _value Value
    */
    function _transfer(address _from, address _to, uint _value) isRunning validAddress internal {
        require(balances[this] >= _value);
        require(!frozenAccount[_from]);
        require(!frozenAccount[_to]);
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(_from, _to, _value);
    }

    /**
    * @dev Freeze Specific Account
    * @param target Target Freeze Address
    * @param freeze Bool True or False
    */
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }

    /**
    * @dev Freezes All Transfers
    */
    function stop() onlyOwner public {
        isActive = false;
    }

    /**
    * @dev UnFreezes All Transfers
    */
    function start() onlyOwner public {
        isActive = true;
    }

    /**
    * @dev Sets Buy and Sell Prices
    * @param newSellPrice The Sell Price
    * @param newBuyPrice The Buy Price
    */
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

    /**
    * @dev Denys All Buy/Sell
    */
    function closeExchange() onlyOwner public {
        isTradable = false;
    }

    /**
    * @dev Allows All Buy/Sell
    */
    function openExchange() onlyOwner public {
        isTradable = true;
    }

    /**
    * @dev Buys Tokens from contract in ether
    */
    function () isExchange validAddress external payable {
        uint256 amount = msg.value;
        amount = amount.div(buyPrice);
        amount = amount.mul(10**18);
        _transfer(this, msg.sender, amount);
        Buy(this, msg.sender, amount, buyPrice);
    }

    /**
    * @dev Sells Ether from contract in Token
    * @param amount The amount of tokens to be sold
    */
    function sell(uint256 amount) isExchange validAddress public {
        require(this.balance >= amount.mul(sellPrice));
        _transfer(msg.sender, this, amount);
        msg.sender.transfer(amount.mul(sellPrice));
        Sell(msg.sender, this, amount, sellPrice);
    }
}
