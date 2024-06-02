// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ModelManagement {
    // Struct to store model information
    struct Model {
        string modelHash;
        string modelURI;
        uint256 timestamp;
    }

    // Mapping to link model hashes to the creators' addresses
    mapping(address => Model[]) public models;

    // Events
    event ModelAdded(address indexed creator, string modelHash, string modelURI, uint256 timestamp);
    event ModelUpdated(address indexed creator, string modelHash, string newModelURI, uint256 timestamp);

    // Function to add a new model
    function addModel(string memory modelHash, string memory modelURI) public {
        Model memory newModel = Model({
            modelHash: modelHash,
            modelURI: modelURI,
            timestamp: block.timestamp
        });

        models[msg.sender].push(newModel);
        emit ModelAdded(msg.sender, modelHash, modelURI, block.timestamp);
    }

    // Function to update an existing model
    function updateModel(string memory modelHash, string memory newModelURI) public {
        Model[] storage userModels = models[msg.sender];
        bool updated = false;
        uint256 timestamp = 0;

        for (uint256 i = 0; i < userModels.length; i++) {
            if (keccak256(abi.encodePacked(userModels[i].modelHash)) == keccak256(abi.encodePacked(modelHash))) {
                userModels[i].modelURI = newModelURI;
                userModels[i].timestamp = block.timestamp;
                updated = true;
                timestamp = block.timestamp;
                break;
            }
        }

        require(updated, "ModelManagement: model not found");
        emit ModelUpdated(msg.sender, modelHash, newModelURI, timestamp);
    }

    // Function to get all models of a creator
    function getModels(address creator) public view returns (Model[] memory) {
        return models[creator];
    }

    // Function to verify the existence of a model
    function verifyModel(address creator, string memory modelHash) public view returns (bool) {
        Model[] memory userModels = models[creator];
        for (uint256 i = 0; i < userModels.length; i++) {
            if (keccak256(abi.encodePacked(userModels[i].modelHash)) == keccak256(abi.encodePacked(modelHash))) {
                return true;
            }
        }
        return false;
    }
}
