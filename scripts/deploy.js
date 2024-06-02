async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
  
    const balance = await deployer.getBalance();
    console.log("Account balance:", balance.toString());
  
    const AccessControl = await ethers.getContractFactory("AccessControl");
    const accessControl = await AccessControl.deploy();
    console.log("AccessControl contract address:", accessControl.address);
  
    const DataIntegrity = await ethers.getContractFactory("DataIntegrity");
    const dataIntegrity = await DataIntegrity.deploy();
    console.log("DataIntegrity contract address:", dataIntegrity.address);
  
    const ModelManagement = await ethers.getContractFactory("ModelManagement");
    const modelManagement = await ModelManagement.deploy();
    console.log("ModelManagement contract address:", modelManagement.address);
  }
  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
  