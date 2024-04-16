### TLDR
The Farcaster Support Agent is trained on the Farcaster docs and answers users' questions about the protocol in-frame.

# Overview
The Farcaster Support Agent is an open-source agent aimed at helping answer new Farcaster users' questions in a timely and accessible way. The agent was used by hundreds of accounts to ask thousands of questions over the first 3 days. All code is open-source and available for other developers to fork, contribute, etc. under the MIT license. Future work will include improving responses based on collected data and continuing to find accessible form factors to provide the agent as a service to new casters.

# Stats & Performance
2,500+ questions were asked in the first 3 days
Hundreds of accounts interacted with the agent and expressed its usefulness
Agent is available both in a frame and via XMTP wallet-based messaging at farcaster-support.agentid.eth


The agent provided some exceptional answers to common yet complicated questions such as:
Q: What's the difference between Warpcast and Farcaster?
A: Warpcast is an app that allows users to access the Farcaster decentralized social network. Farcaster is the underlying social network itself.

Q: What's a warp?
A: A warp is a way to perform onchain actions within the Warpcast app. It is specific to Warpcast and is not onchain.

Q: How is Farcaster onchain if it doesn't cost me any ETH to post?
A: Farcaster's onchian systems are used for critical actions such as creating an account, paying rent for data storage, or adding account keys for connected apps. Posting on Farcaster does not incur a direct cost in ETH because it utilizes offchain systems, where actions are performed without requiring onchain transactions.

# Stack & Build Process
The agent's context includes both raw documentation and anticipated questions based on that documentation to improve retrieval. I pre-processed the Farcaster documentation along with the protocol specification, then had GPT-3.5 predict questions that could be asked for each section. These questions make it easy to retrieve the relevant documentation sections using users' questions, as opposed to trying to map the long-form documentation to the user's questions directly.

The agent itself is a Python FastAPI that accepts a user's question, generates the question's embedding, then does a similarity search over both the pre-generated question and documentation embeddings. The agent retrieves the closes 8 sections (one section is roughly 1-2 paragraphs) from the documentation and uses it to answer the user's question. The agent is instructed to reply with "I'm not sure." in the event the provided documentation does not directly supply an answer.

The frame was built as a Next.js app that uses a custom-built frames library specializing in asynchronous state. This is important given the LLM's slow response time.

The agent was deployed with Operator's XMTP service to allow for messaging the agent from any XMTP client and referencing it from an ENS.


# Future Work and Challenges
Response time UX: Getting an LLM to respond in under the 5 second frames timeout requirement is quite difficult, especially when the response first requires generating embeddings and performing a latent-space search over the existing documentation, as the agent does. The current build does this quite well (responds in time in about 80% of cases), but I'd like to improve the frame UX for cases where it does not respond in time. (XMTP has no timeout limit so it's not an issue for that form factor.)

Threaded conversations: The current agent does not store a user's message history and therefore can't be asked followup questions. I'd like to add this ability in future iterations.

Improved responses: While the bot does surprisingly well to avoid hallucinating answers, there are common questions that the docs are missing. Notably, I've seen several questions about Base given its strong usage in the Farcaster ecosystem. I'd like to incorporate answers to questions like these into the agent's context so it can provide answers to a wider array of questions.


If you have any questions or suggestions, feel free to DC me @gregfromstl on Farcaster.
