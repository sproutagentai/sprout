<<<<<<< HEAD
# prime
Prime: a solana python library for creating new agents. Agents write python code to call tools or orchestrate other agents.
=======
<!---
Copyright 2024 The HuggingFace Team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

<h3 align="center">
  <p> Prime - First Solana Python Library To Build Great Agents!</p>
</h3>

`prime` is a library that enables you to run powerful agents in a few lines of code. It offers:

✨ **Simplicity**: the logic for agents fits in ~thousand lines of code (see agents.py. We kept abstractions to their minimal shape above raw code!

🧑‍💻 **First-class support for Code Agents**, i.e. agents that write their actions in code (as opposed to "agents being used to write code"). To make it secure, we support executing in sandboxed environments via [E2B](https://e2b.dev/).
 - On top of this `CodeAgent` class, we still support the standard `ToolCallingAgent`

🤗 **Hub integrations**: you can share and load tools to/from the Hub, and more is to come!

🌐 **Support for any LLM**: it supports models hosted on the Hub loaded in their `transformers` version or through our inference API, but also supports models from OpenAI, Anthropic and many others via our [LiteLLM](https://www.litellm.ai/) integration.

## Quick demo

First install the package.
```bash
pip install prime-agents-py
```
Then define your agent, give it the tools it needs and run it!
```py
from prime import CodeAgent, DuckDuckGoSearchTool, HfApiModel

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())

agent.run("Tell me Solana and Bitcoin price in March 2025")
```


## Code agents?

In our `CodeAgent`,  the LLM engine writes its actions in code. This approach is demonstrated to work better than the current industry practice of letting the LLM output a dictionary of the tools it wants to calls: [uses 30% fewer steps](https://huggingface.co/papers/2402.01030) (thus 30% fewer LLM calls)
and [reaches higher performance on difficult benchmarks](https://huggingface.co/papers/2411.01747).

Especially, since code execution can be a security concern (arbitrary code execution!), we provide options at runtime:
  - a secure python interpreter to run code more safely in your environment
  - a sandboxed environment using [E2B](https://e2b.dev/).

## How smol is it really?

We strived to keep abstractions to a strict minimum: the main code in `agents.py` is only ~1,000 lines of code.
Still, we implement several types of agents: `CodeAgent` writes its actions as Python code snippets, and the more classic `ToolCallingAgent` leverages built-in tool calling methods.

By the way, why use a framework at all? Well, because a big part of this stuff is non-trivial. For instance, the code agent has to keep a consistent format for code throughout its system prompt, its parser, the execution. So our framework handles this complexity for you. But of course we still encourage you to hack into the source code and use only the bits that you need, to the exclusion of everything else!

## How strong are open models for agentic workflows?

We've created `CodeAgent` instances with some leading models, and compared them on [this benchmark](https://huggingface.co/datasets/m-ric/agents_medium_benchmark_2) that gathers questions from a few different benchmarks to propose a varied blend of challenges.


This comparison shows that open source models can now take on the best closed models!

## Citing prime

If you use `prime` in your publication, please cite it by using the following BibTeX entry.

```bibtex
@Misc{prime,
  title =        {`prime`: The easiest way to build efficient solana agentic systems.},
  author =       {primengine inc.},
  howpublished = {\url{https://github.com/primengine/prime}},
  year =         {2025}
}
```
