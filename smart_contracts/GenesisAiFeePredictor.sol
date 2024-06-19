// SPDX-License-Identifier: MIT 
// Work in progress 0.0.21 - Updated 3 Jun
pragma solidity ^0.8.0;

import "./GasFeePredictor.sol";

contract IntelligentGasFeeManager {
    GasFeePredictor public gasFeePredictor;

    event GasFeeUpdated(uint256 newGasFee);

    constructor(address _gasFeePredictorAddress) {
        gasFeePredictor = GasFeePredictor(_gasFeePredictorAddress);
    }

    function updateGasFee() public {
        uint256 predictedGasFee = gasFeePredictor.getGasFeePrediction();
        // Logica pentru ajustarea automată a taxei de gaz pe baza predicției
        emit GasFeeUpdated(predictedGasFee);
    }
}