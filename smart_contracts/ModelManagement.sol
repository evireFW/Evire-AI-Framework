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

    /**
     * @dev Adds a new model to the sender's model list
     * @param modelHash The unique hash of the model
     * @param modelURI The URI pointing to the model's metadata
     */
    function addModel(string memory modelHash, string memory modelURI) public {
        require(bytes(modelHash).length > 0, "Model hash is required");
        require(bytes(modelURI).length > 0, "Model URI is required");

        models[msg.sender].push(Model({
            modelHash: modelHash,
            modelURI: modelURI,
            timestamp: block.timestamp
        }));

        emit ModelAdded(msg.sender, modelHash, modelURI, block.timestamp);
    }

    /**
     * @dev Updates an existing model in the sender's model list
     * @param modelHash The unique hash of the model to be updated
     * @param newModelURI The new URI pointing to the model's updated metadata
     */
    function updateModel(string memory modelHash, string memory newModelURI) public {
        require(bytes(modelHash).length > 0, "Model hash is required");
        require(bytes(newModelURI).length > 0, "New model URI is required");

        Model[] storage userModels = models[msg.sender];
        bool updated = false;

        for (uint256 i = 0; i < userModels.length; i++) {
            if (keccak256(abi.encodePacked(userModels[i].modelHash)) == keccak256(abi.encodePacked(modelHash))) {
                userModels[i].modelURI = newModelURI;
                userModels[i].timestamp = block.timestamp;
                updated = true;
                emit ModelUpdated(msg.sender, modelHash, newModelURI, block.timestamp);
                break;
            }
        }

        require(updated, "ModelManagement: model not found");
    }

    /**
     * @dev Returns all models created by the specified address
     * @param creator The address of the model creator
     * @return An array of Model structs
     */
    function getModels(address creator) public view returns (Model[] memory) {
        return models[creator];
    }

    /**
     * @dev Verifies the existence of a model by its hash and creator's address
     * @param creator The address of the model creator
     * @param modelHash The unique hash of the model
     * @return A boolean indicating whether the model exists
     */
    function verifyModel(address creator, string memory modelHash) public view returns (bool) {
        require(bytes(modelHash).length > 0, "Model hash is required");

        Model[] memory userModels = models[creator];
        for (uint256 i = 0; i < userModels.length; i++) {
            if (keccak256(abi.encodePacked(userModels[i].modelHash)) == keccak256(abi.encodePacked(modelHash))) {
                return true;
            }
        }
        return false;
    }
}