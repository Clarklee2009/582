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

	self.tokenA = ERC20(tokenA_addr)
	self.tokenA.transferFrom(msg.sender, self.tokenA.address, tokenA_quantity) 
	self.tokenAQty = tokenA_quantity

	self.tokenB = ERC20(tokenB_addr)
	self.tokenB.transferFrom(msg.sender, self.tokenB.address, tokenB_quantity)
	self.tokenBQty = tokenB_quantity

	self.invariant = self.tokenAQty * self.tokenBQty

	assert self.invariant > 0

# Trades one token for the other
@external
def tradeTokens(sell_token: address, sell_quantity: uint256):
	assert sell_token == self.tokenA.address or sell_token == self.tokenB.address
	if sell_token == self.tokenA.address:
		self.tokenA.transferFrom(msg.sender, self.tokenA.address, sell_quantity)

		new_total_tokens: uint256 = self.tokenAQty + sell_quantity
		new_total: uint256 = self.invariant / new_total_tokens
		send_token: uint256 = self.tokenAQty - new_total
		send(msg.sender, send_token)
		self.tokenBQty = new_total
		self.tokenAQty = new_total_tokens


	elif sell_token == self.tokenB.address:
		self.tokenB.transferFrom(msg.sender, self.tokenB.address, sell_quantity)
		new_total_tokens: uint256 = self.tokenBQty + sell_quantity
		new_total: uint256 = self.invariant / new_total_tokens
		send_token: uint256 = self.tokenBQty - new_total
		send(msg.sender, send_token)
		self.tokenAQty = new_total
		self.tokenBQty = new_total_tokens


	#Your code here

# Owner can withdraw their funds and destroy the market maker
@external
def ownerWithdraw():
	assert self.owner == msg.sender
	#Your code here
	self.tokenA.transfer(self.owner, self.tokenAQty)
	self.tokenB.transfer(self.owner, self.tokenBQty)
	selfdestruct(self.owner)