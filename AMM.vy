from vyper.interfaces import ERC20

tokenAQty: public(uint256) #Quantity of tokenA held by the contract
tokenBQty: public(uint256) #Quantity of tokenB held by the contract

invariant: public(uint256) #The Constant-Function invariant (tokenAQty*tokenBQty = invariant throughout the life of the contract)
tokenA: ERC20 #The ERC20 contract for tokenA
tokenB: ERC20 #The ERC20 contract for tokenB
owner: public(address) #The liquidity provider (the address that has the right to withdraw funds and close the contract)

@external
def get_token_address(token: uint256) -> address:
	if token == 0:
		return self.tokenA.address
	if token == 1:
		return self.tokenB.address
	return ZERO_ADDRESS	

# Sets the on chain market maker with its owner, and initial token quantities
@external
def provideLiquidity(tokenA_addr: address, tokenB_addr: address, tokenA_quantity: uint256, tokenB_quantity: uint256):
	assert self.invariant == 0 #This ensures that liquidity can only be provided once
	
	self.owner = msg.sender





	self.tokenA_address = ERC20(tokenA_addr)
	self.tokenA_address.transferFrom(msg.sender, self, tokenA_quantity)
    
	self.totalTokenQtyA = tokenA_quantity
    

	self.tokenB_address = ERC20(tokenB_addr)
	self.tokenB_address.transferFrom(msg.sender, self, tokenB_quantity)
    
	self.totalTokenQtyB = tokenB_quantity
    

	assert self.invariant > 0

# Trades one token for the other
@external
def tradeTokens(sell_token: address, sell_quantity: uint256):
	assert sell_token == self.tokenA.address or sell_token == self.tokenB.address
	if sell_token == self.tokenA_address:
		sell_token.transferFrom(msg.sender, self, sell_quantity)
		new_total_tokens: uint256 = self.totalTokenQtyA + sell_quantity
		new_total_eth: uint256 = self.invariantA / new_total_tokens
		eth_to_send: uint256 = self.totalEthQtyA - new_total_eth
		send(msg.sender, eth_to_send)
		self.totalEthQtyA = new_total_eth
		self.totalTokenQtyA = new_total_tokens
	elif sell_token == self.tokenB.address:
		sell_token.transferFrom(msg.sender, self, sell_quantity)
		new_total_tokens: uint256 = self.totalTokenQtyB + sell_quantity
		new_total_eth: uint256 = self.invariantB / new_total_tokens
		eth_to_send: uint256 = self.totalEthQtyB - new_total_eth
		send(msg.sender, eth_to_send)
		self.totalEthQtyB = new_total_eth
		self.totalTokenQtyB = new_total_tokens


	#Your code here

# Owner can withdraw their funds and destroy the market maker
@external
def ownerWithdraw():
	assert self.owner == msg.sender
	#Your code here
	self.token_address.transfer(self.owner, self.totalTokenQtyA)
	self.token_address.transfer(self.owner, self.totalTokenQtyB)
	selfdestruct(self.owner)