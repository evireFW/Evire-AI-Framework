// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataIntegrity {
    // Struct to store data information
    struct DataRecord {
        string dataHash;
        uint256 timestamp;
    }

    // Mapping to link data hashes to the creators' addresses
    mapping(address => DataRecord[]) public dataRecords;

    // Events
    event DataAdded(address indexed creator, string dataHash, uint256 timestamp);
    event DataVerified(address indexed verifier, string dataHash, bool valid, uint256 timestamp);

    // Function to add a new data hash
    function addData(string memory dataHash) public {
        DataRecord memory newDataRecord = DataRecord({
            dataHash: dataHash,
            timestamp: block.timestamp
        });

        dataRecords[msg.sender].push(newDataRecord);
        emit DataAdded(msg.sender, dataHash, block.timestamp);
    }

    // Function to verify the integrity of data
    function verifyData(address creator, string memory dataHash) public returns (bool) {
        DataRecord[] memory records = dataRecords[creator];
        bool valid = false;
        uint256 timestamp = 0;

        for (uint256 i = 0; i < records.length; i++) {
            if (keccak256(abi.encodePacked(records[i].dataHash)) == keccak256(abi.encodePacked(dataHash))) {
                valid = true;
                timestamp = records[i].timestamp;
                break;
            }
        }

        emit DataVerified(msg.sender, dataHash, valid, block.timestamp);
        return valid;
    }

    // Function to get all records of a creator
    function getDataRecords(address creator) public view returns (DataRecord[] memory) {
        return dataRecords[creator];
    }
}
