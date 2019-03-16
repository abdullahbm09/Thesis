var Migrations = artifacts.require("./AdditionContract.sol");

module.exports = function(deployer) {
  deployer.deploy(Migrations);
};
