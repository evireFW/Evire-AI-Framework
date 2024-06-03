// Work in progress 0.0.21 - Updated 3 Jun
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract GasFeePredictor is ChainlinkClient {
    using Chainlink for Chainlink.Request;

    address public owner;
    uint256 public latestGasFeePrediction;

    bytes32 private jobId;
    uint256 private fee;

    event GasFeePredicted(uint256 predictedGasFee);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
        setPublicChainlinkToken();
        jobId = "YOUR_JOB_ID";  // TBD
        fee = 0.1 * 10 ** 18;   // 0.1 EVIRE
    }

    function requestGasFeePrediction(string memory _url, string memory _path) public onlyOwner {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        request.add("get", _url);
        request.add("path", _path);
        sendChainlinkRequest(request, fee);
    }

    function fulfill(bytes32 _requestId, uint256 _gasFeePrediction) public recordChainlinkFulfillment(_requestId) {
        latestGasFeePrediction = _gasFeePrediction;
        emit GasFeePredicted(_gasFeePrediction);
    }

    function getGasFeePrediction() external view returns (uint256) {
        return latestGasFeePrediction;
    }
}