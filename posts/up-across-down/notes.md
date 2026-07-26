The purpose of this folder is to develop a blog post. 
The blog post will be called Up, Across, Down: 
Subtitle: On developing Upgrade, my new retro game; Comparing Claude Fable 5 with Claude Opus 5; and reflecting on pushback on presenting an AI codeveloped game as 'mine'. 

Sections: 

Up: The Upgrade Game

- Inspiration was the ZX Spectrum game Feud, in which two wizards (two brothers) battle to defeat each other over an multi-screen arena. 

- My own history with home computers: ZX Spectrum 48K; ZX Spectrum 128K; Amiga 500; then Amiga 1200 (before PCs). 

- Spectrum had a very distinct graphical style caused by its limitations with colour. It allowed pixels to be specified as 'on' or 'off' at a comparatively high resolution; but the colours associated with 'on' or 'off' to be specified only for (I think) 8 by 8 tiles of cells within the resolution. This was because the Spectrum wasn't really designed with games in mind, but with more serious applications. Consider for instance a simple word processor: a letter is a block of pixels that could fit inside one of the colour block tiles. So being able to change the complete foreground and background colours at once would be helpful for marking out letters for attention, editing, highlighting etc. No higher resolution for specifying colours - like making the edges of a letter a different colour to the rest of it - would be of much additional benefit.

- The game mechanics are based around my own journey with home computers from the early 1980s to mid 1990s. As well as the way that Feud was based on rivalry and foraging. The player navigates a multi-screen arena, looking for shards that they can pick up. When they have three shards, they can upgrade the tech stack; with this the aesthetics of the game change too. 

- List T levels. Specify start is T1, my own first computer, ZX Spectrum, but there's also a T0 - true monochrome purgatory - with T3 and T4, C64 and Atari ST, not being part of my own history but obvious intermediate stages on the way to the Amiga. (Though placing Atari before Amiga might reflect my own subjective biases)

- More materials showing the assets at each T level. 

- More on how level editors and then map generators were added: CA style rules as specified and implemented
     - Multi-stage iteration of maps: checking for where wand station is too close to edge; ensuring bases are sufficiently far from each other; checking all of the arena becomes accessible through 'clearing' mechanics etc.


- Additional game mechanics: Easy and Hard Mode; Icewands and Firewands (different trade-offs); the gameplay and cross-game loop

- Additional arena mechanics: standard initial map, with slight modification from procedurally generated first instance. Then chaos mode. Opportunity to create and supply new maps (either from nothing or procedurally generated then modified) via editor. 

Second section: Across: 

- this focuses on use of Opus 5 (along with GPT and Gemini models) to look for causes of performance issues within games, usually kicking in within T3. 
- GPT (through github copilot) identified issues likely to cause slowdown which accumulate over a game session. Opus 5 did much more thorough investigation of these potential issues and others by running many experiments in the codebase (though afterwards apologised for deleting state data and bespoke map data!). It confirmed the GPT-identified issues were substantive, but that the order of priorities in terms of importance on latency was different to GPT's assumptions. 
- Fable then read multiple code review reports, and largely implemented the changes as recommended by the agentic review panel. 

- Within recent LLM performance benchmarks, Opus 5, despite being nominally a tier below Fable 5 (Mythos + Guardrails) and half the cost-per-token, achieves similar performance on many technical and applied-knowledge related tasks. 

- I don't have a big reason to doubt this (except for the ways metrics could be cherry-picked). But from initial impressions think they may often achieve similar outcomes through different means. Crudely, Opus 5 appears to be more of a 'swot', whereas Fable 5 more of a Savant. 

- Swot behaviour: 
    - Even more extensive and comprehensive RAG searches
    - Even more extensive and comprehensive review of codebases
    - Even more extensive and exhaustive testing and iteration. 

- Savant behaviour: 
    - More reliance on 'reasoning from first principles'
    - More creative and often intelligent inference about the latent subgoals and implicit assumptions and expectations behind the prompt. 

- Both have very high tenacity (though this is probably something being tuned based on capacity/demand)

So, although Opus 5 and Fable 5 are intended as being at different tiers, for now they can perhaps be thought of as similarly capable models which often achieve similar outcomes through different means. Because of its guardrails, which hairtrigger when anything relating to biology or cybersecurity happens to be searched for or reasoned about, Fable probably *shouldn't* aim to be more Swottish, as then it would be more likely to hit one of these hairtriggers by chance. As token cost tariffs are double for Fable than Opus, it should probably not go too far in this direction in any case. 

Two more implications:

- Fable and Opus should, for now, be considered complementary siblings to each other. 
- Because of its high tendency to swottishness, though Opus has half the cost per token, we shouldn't assume it's going to be half the cost per completed project. Opus 5 may, conceivibly, burn through twice as many tokens as Fable in search and evaluation, leading to the model that on the face of it looks 'twice as cheap' turning out to have about the same cost per project completion. 

Anyway, the agentic review carousel, for identifying and fixing performance issues, seemed to work well, and Opus 5 was a critical part of this multi-agent mix. (Even if it did delete and modify some uncommitted files in my codebase in the process.)

Third section: Down: Pushback against AI-coproduced game creation. 

- Local Game Developers Forum. Post link on Show & Tell Channel. 
- Some engagement initially. Mentioned number of iterations and tuning. Someone points out written 'by' Claude. Responded: didn't try to hide this: name credited is Jon Fableton.; public repo: 'Claude' listed throughout as collaborator. 
- Initial positive response shifts. Request for moderators to force explicit declaration of AI-coproduced content so respondent can ignore and disengage with it. (Strong support for that sentiment). 

- Broader reflections on this: 

- False binary: Never fully AI or fully human. Always some mixture. 

- Very broad range of levels of AI engagement with human content, human engagement with AI content. Still learning right balance. Cognitive centaurs. 

- Workflow with AI *will* come to outcompete workflow without AI across pretty much every dimension, and *will* come to become the dominant means of doing games development, or any other kind of analytical technical systems work, within 1-5 years. 
    - When this happens the falseness of the binary will be recognised
    - During the transition phase there will be groups and cliches that will increasingly define themselves by their opposition to AI; and to the extent some consumers will also have anti-AI sentiments they may get short-term bumps in engagement and support. But these are ripples in the opposite direction to the main tide. 

- At its best AI will be a multiplier, not replacement, for human knowledge, curiousity, and creativity. Already it allows hunches, eddies, asides, etc to be developed into full-blown prototypes so much faster and more cheaply than ever before, making it much easier to evaluate whether the hunches are likely to pay off. 
- Creative and curious people *won't* run out of creativity and curiosity. The collapse in implementation cost means new demand will emerge: Jevon's Effects. 
- This is the corrective to the intuitive framing of the role of AI, and why it's often instinctively seen as a 'threat'. This is the Lump of Labour fallacy, in which it is assumed there is only a finite demand for 'stuff' - prototypes, games, analytic outputs, websites, databases, papers, etc - and so technologies that reduce the cost of producing this stuff reduce the total sum of labour that can be supported by an industry, and so 'put people out of work'. 
    - Some of the less insightful proponents of AI in business, such as mid/senior managers and executives, may also subscribe to the Lump of Labour Fallacy, and be attracted to implementing AI for exactly the reason many other people are repelled to implementing AI: that they think they can and should simply reduce headcount. 
    - The irony in this position: large organisations tend to be *less* adaptable to the pace of change required to get the best from AI. There will be standards, procedures, conventions and 'ways of working' that are long established and which will ultimately be impediments to the wholesale reconfiguration of work, tasks and roles in ways that allow organisations to use AI to multiply the creativity and productivity of employees as much as they can. Instead smaller, nimbler, AI-native organisations, without the cold hand of history/path dependency, will be able to structure themselves from scratch around agentic ways of working, and very soon to be able to outcompete the old behemoths. The beautiful sting in the tail: if a large and slowly adapting organisation *does* use AI to justify making talented staff redundant en mass, those former staff are now in a better position than ever before to form AI-native startups and destroy their alma maters! But only if the laid-off staff realise AI is the solution, not the problem, and embrace AI as human effort multipliers, rather than reject and oppose it. 


- AI is ultimately 'just' yet another example of the decades-long tendencies in applied information sciences to progress along two axes: 1) for information retrieval, producing, and processing speeds to increase; 2) for the level of abstraction and generalisation at which humans instruct machines to go 'up', i.e. to become more about the level of the intent and outcome, and less about processes and mechanisms. 
    - Examples of this include pretty much any programming language at a 'higher' level than machine code/assembly language, which uses human-like nouns and verbs. This includes the BASIC shipped with every ZX Spectrum. 
    - AI differs, however, in two ways: firstly the breadth and pace at which things are changing; secondly in potentially reducing the premium for specialisation as opposed to generalism. 


