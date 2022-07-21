# Zhtools
Some simple tool methods like cache, exporter and so on.


## Modules
- cache: A simple cache decorator.
- code_generator: 
  - json2model: Generate pydantic model from json string.
  - orms: Generate model code from create table sql.
- exporters: Export data to a file like .xlsx and etc.
- io_tools: Some io tool methods.
  - readers: Simple method to read data from a file like .xlsx and etc.
- data_structs: Some data structs implements and tools.
- random: Uuid, random string and so on.
- redis_helper: Some tools base on redis.
- timetools: Some date/time/timezone tools.
- type_hint: Common type hints.
- api_service: Simple way to define an api client.
- enum: More practical enum.
- concurrents: Some tools for concurrent base on multi process/thread/coroutine.
- ctx: Some context tools.
- async_tools: about python async/await.
- security: some simple security methods.
- log: simple logging config tools.
- signals: simple signal dispatcher.
- \_\_init\_\_: Unclassified tools.


## Update logs
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
