# Zhtools
Some simple tool methods like cache, timetools and so on.


## Modules
- cache: A simple cache decorator.
- data_structs: Some data structs implements and tools.
- security: some simple security methods.
- api_service: Simple way to define an api client.
- async_tools: about python async/await.
- calculation: Math calculation methods.
- cli: Command-line tools.
- concurrents: Some tools for concurrent base on multi process/thread/coroutine.
- config: Global config by this tool.
- context_manager: Common context manager.
- decorators: Common decorators.
- exceptions: Common exceptions by this tool.
- random: Random methods.
- signals: simple signal dispatcher.
- timetools: Some date/time/timezone tools.
- typing: Common type hints.


## Update logs
- **1.1.0** 2024-07-04:
  - feat: `multi_by_date` decorator
  - feat: Upgrade to python 3.12
  - fix: Support more type hint
- **1.0.2** 2024-01-12:
  - Fix AES encrypt/decrypt type hint.
- **1.0.0** 2023-06-17:
  - Refactored code to used more type hint. Now only support python 3.11+.
  - Because of the ChatGPT, remove the `code_generator` module.
  - Remove `data_structs.lazy` module, recommend to use `lazy-object-proxy` instead.
  - Remove `exporters` module.
  - Remove `io_tools` module.
  - Remove `redis_helper` module.
  - Remove `log` module.
  - Move `enum` to `data_structs.enum`.
  - Move `third_parties.pydantic` to `data_structs.pydantic`.
  - Move `type_hint` to `typing`.
  - Change `requests` and `aiohttp` requirement to `httpx`.
- **0.3.0** 2022-07-21:
  - Refactored cache.
  - Add signal dispatcher.
- **0.2.3** 2022-04-08: 
  - Fix & add cli command.
  - Add log module.
- **0.2.2** 2022-01-08:
  - Add AES encrypt/decrypt method. 
- **0.2.1** 2021-12-30:
  - Move `convertors` to `data_structs.convertors`
  - add some data_structs and methods.
- **0.1.1** 2021-12-8:
  - Optimize timetools. Now can set global timezone.
- **0.0.11** 2021-10-21:
  - Add js-like *Promise*.
- **0.0.10** 2021-06-25:
  - Add go-like defer.
- **0.0.9** 2021-06-04:
  - Fix setup bug.
- **0.0.8** 2021-06-04:
  - Add concurrents tools.
  - Add orm code generators command-line client.
- **0.0.7** 2021-05-21:
  - Add singleton decorator.
  - Add orm code generators.
- **0.0.6** 2021-04-25:
  - Add enum module.
- **0.0.5** 2021-04-19: 
  - Added api service.
  - Optimized the performance of XlsxReader.
  - Added progress bar to XlsxExporter (supported by [tqdm](https://github.com/tqdm/tqdm)).
