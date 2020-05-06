
This mechanism solves the “rich get richer” problem by assigning the reward to multiple miners that pool their stake. It also solves the “lazy miner” problem by making sure a block is generated before a verifier for the block is assigned.




Let verifiers (miners) create blocks in each time instance (say every 20 seconds) according to a probability p, instead of by mining.

- Each verifier creates a block every 20 seconds, if there are transactions according to some probability

Verifiers with a block interact through consensus to decide which one of them is allowed to add their block to the chain.

- Verifier with lowest nodeid is leader and is the one to add the block to the chain

The winner contacts other verifiers, who sign the block, if the containing transactions do not contain double spending transactions (spender has money to spend) and if the block creator does not exceed p in creating the block. 

- Leader sends block to verifiers (all verfiers?), (who only can sign with prob p?)
- ???

Once a block has signatures from enough verifiers, such that their stake exceeds the total of the transactions, the block can be added to the blockchain. 

- ? 

Finally, a reward for the verifier that created the block and those who signed it is recorded in the block.
- 


1 - a verifier generates a block with probability p
    - Should only the leader generate the block?
    - What is p, is it based on stake?

3 - verifiers reach consensus on accepted blocks
    - Don't send reply or send negative reply if you don't validate block

3 - block signed with sufficient proof of stake
    - Leader collects enough signatures with enough stake that it can be commited

1 - signed block contains no double spending events
    - Everybody checks it

2 - signed block does not exceed p for client
    - What does this mean????

2 - verifiers get reward for creating a block
    - Leader gets a reward for creating

2 - verifiers get reward for signing a block
    - Encoded in block, tallied at node