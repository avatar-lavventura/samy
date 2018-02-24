pragma solidity ^0.4.18;

import "./SafeMath.sol";
import "./RefundVault.sol";
import "./ERC20Basic.sol";
import "./SafeERC20.sol";

contract Crowdsale is Ownable {

    using SafeERC20 for ERC20Basic;
    using SafeMath for uint256;

    address public beneficiary;
    uint256 public fundingGoal;
    uint256 public cap;
    uint256 public weiAmountRaised;
    uint256 public rate;
    uint256 public startTime;
    uint256 public endTime;
    uint256 public bonusStart;
    uint256 public bonusEnd;
    uint256 public bonus;

    ERC20Basic public token;

    RefundVault public vault;
    bool public isFinalized = false;

    event TokenContribution(address backer, uint256 weiAmount, uint256 tokens, bool isBonus);

    event Finalized(bool isFinalized);

    function Crowdsale(
        address _beneficiary,
        uint256 _fundingGoal,
        uint256 _cap,
        uint256 _rate,
        uint256 _startTime,
        uint256 _endTime,
        uint256 _bonusStart,
        uint256 _bonusEnd,
        uint256 _bonus,
        ERC20Basic _token
    )  public {
        require(_fundingGoal > 0);
        require(_cap > 0);
        require(_fundingGoal < _cap);
        require(_rate > 0);
        require(_token != address(0));
        require(_beneficiary != address(0));

        beneficiary = _beneficiary;
        fundingGoal = _fundingGoal;
        cap = _cap;
        rate = _rate;
        startTime = _startTime;
        endTime = _endTime;
        bonusStart = _bonusStart;
        bonusEnd = _bonusEnd;
        bonus = _bonus;
        token = _token;
        vault = new RefundVault(beneficiary);
    }

    function buyTokens(address _to) public payable {
        require(_to != address(0));
        require(validPurchase());

        uint256 weiAmount = msg.value;

        uint256 tokens = getTokenAmount(weiAmount);
        weiAmountRaised = weiAmountRaised.add(msg.value);
        token.safeTransfer(_to, tokens);
        bool isBonus = now >= bonusStart && now <= bonusEnd;
        TokenContribution(_to, weiAmount, tokens, isBonus);

        forwardFunds();
    }

    function () external payable {
        buyTokens(msg.sender);
    }

    // @return tokens purchase amount
    function getTokenAmount(uint256 weiAmount) internal view returns(uint256) {
        if (now >= bonusStart && now <= bonusEnd) {
            uint256 weiBonus = weiAmount.div(bonus);
            weiAmount = weiAmount.add(weiBonus);
        }

        return weiAmount.mul(rate);
    }

    function forwardFunds() internal {
        vault.deposit.value(msg.value)(msg.sender);
    }

    function sendRefunds() onlyOwner  public {
        require(isFinalized);
        require(!goalReached());
        vault.refund();
    }

    function finalization() onlyOwner public {

        require(!isFinalized);
        require(hasEnded());

        if (goalReached()) {
            vault.close();
            burnRemaining();
        } else {
            vault.enableRefunds();
            transferRemaining();
        }

        Finalized(isFinalized);
        isFinalized = true;
    }

    // @return true if goal was reached
    function goalReached() public view returns (bool) {
        return weiAmountRaised >= fundingGoal;
    }

    // @return true if crowdsale has ended
    function hasEnded() public view returns (bool) {
        bool capReached = weiAmountRaised >= cap;
        return now >= endTime || capReached;
    }

    // Burn remaining tokens left in crowdsale
    function burnRemaining() onlyOwner  public {
        uint256 amount = token.balanceOf(this);
        token.burn(amount);
    }

    // Transfer remaining tokens left in crowdsale
    function transferRemaining() onlyOwner  public {
        address to = msg.sender;
        uint256 amount = token.balanceOf(this);
        token.safeTransfer(to, amount);
    }

    // @return true if the transaction can buy tokens
    function validPurchase() internal view returns (bool) {
        bool withinCap = weiAmountRaised.add(msg.value) <= cap;
        bool aboveMinimumPurchase = msg.value >= 10000000000000000;
        return withinCap && aboveMinimumPurchase;
    }
}
