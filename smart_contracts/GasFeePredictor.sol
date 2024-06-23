// SPDX-License-Identifier: UNKNOWN 
// v 0.0.3 Update 23 jun 24
pragma solidity ^0.8.0;

import "./EvireClient.sol"; // Still private - to be release

contract GasFeePredictor is EvireClient {
    using Evire for Evire.Request;

    address public owner;
    uint256 public latestGasFeePrediction;
    bytes32 private jobId;
    uint256 private fee;

    event GasFeePredicted(uint256 predictedGasFee);
    event JobIdUpdated(bytes32 newJobId);
    event FeeUpdated(uint256 newFee);
    event OracleUpdated(address newOracle);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor(address _oracle, bytes32 _jobId, uint256 _fee) {
        owner = msg.sender;
        setEvireToken(); // Use the method to set the Evire token
        setEvireOracle(_oracle); // Use the method to set the Evire oracle
        jobId = _jobId;
        fee = _fee;
    }

    /**
     * @notice Request a gas fee prediction from the Evire oracle
     * @param _url The API endpoint URL
     * @param _path The JSON path to extract the prediction
     */
    function requestGasFeePrediction(string memory _url, string memory _path) public onlyOwner {
        Evire.Request memory request = buildEvireRequest(jobId, address(this), this.fulfill.selector);
        request.add("get", _url);
        request.add("path", _path);
        sendEvireRequest(request, fee);
    }

    /**
     * @notice Fulfill the Evire request
     * @param _requestId The ID of the request
     * @param _gasFeePrediction The predicted gas fee
     */
    function fulfill(bytes32 _requestId, uint256 _gasFeePrediction) public recordEvireFulfillment(_requestId) {
        latestGasFeePrediction = _gasFeePrediction;
        emit GasFeePredicted(_gasFeePrediction);
    }

    /**
     * @notice Get the latest gas fee prediction
     * @return The latest predicted gas fee
     */
    function getGasFeePrediction() external view returns (uint256) {
        return latestGasFeePrediction;
    }

    /**
     * @notice Update the Evire job ID
     * @param _jobId The new job ID
     */
    function updateJobId(bytes32 _jobId) external onlyOwner {
        jobId = _jobId;
        emit JobIdUpdated(_jobId);
    }

    /**
     * @notice Update the Evire fee
     * @param _fee The new fee
     */
    function updateFee(uint256 _fee) external onlyOwner {
        fee = _fee;
        emit FeeUpdated(_fee);
    }

    /**
     * @notice Update the Evire oracle address
     * @param _oracle The new oracle address
     */
    function updateOracle(address _oracle) external onlyOwner {
        setEvireOracle(_oracle);
        emit OracleUpdated(_oracle);
    }

    /**
     * @notice Withdraw EVIRE tokens from the contract
     */
    function withdrawEvire() external onlyOwner {
        EvireTokenInterface evire = EvireTokenInterface(evireTokenAddress());
        require(evire.transfer(msg.sender, evire.balanceOf(address(this))), "Unable to transfer");
    }
}