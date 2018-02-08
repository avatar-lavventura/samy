pragma solidity ^0.4.18;

import "./SafeMath.sol";
import "./Ownable.sol";

contract RefundVault is Ownable {

    using SafeMath for uint256;

    enum State {
        Active,
        Refunding,
        Refunded,
        Closed
    }

    struct Contribution {
        uint amount;
        address addr;
    }

    //mapping (address => uint256) public deposited;

    Contribution[] funders;

    address public wallet;

    State public state;

    event Closed();
    event RefundsEnabled();
    event Refunded(address indexed beneficiary, uint256 weiAmount);

    function RefundVault(address _wallet) public {
        require(_wallet != address(0));
        wallet = _wallet;
        state = State.Active;
    }

    function deposit(address investor) onlyOwner public payable {
        require(state == State.Active);
        funders.push(
            Contribution({
                amount: msg.value,
                addr: investor
            })
        );
    }

    function close() onlyOwner public {
        require(state == State.Active);
        state = State.Closed;
        Closed();
        wallet.transfer(this.balance);
    }

    function enableRefunds() onlyOwner public {
        require(state == State.Active);
        state = State.Refunding;
        RefundsEnabled();
    }

    function refund() onlyOwner  public {
        require(state == State.Refunding);
        for (uint i = 0; i < funders.length; ++i) {
            if (!funders[i].addr.send(funders[i].amount)) {
                revert();
            }
            Refunded(funders[i].addr, funders[i].amount);
        }
        state = State.Refunded;
    }
}
