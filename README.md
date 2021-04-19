# Zhtools
Some simple tool methods like cache, exporter and so on.


## Modules
- cache: A simple cache decorator.
- code_generator: 
  - json2model: Generate pydantic model from json string.
- exporters: Export data to a file like .xlsx and etc.
- io_tools: Some io tool methods.
  - readers: Simple method to read data from a file like .xlsx and etc.
- convertors: Some unit convertors or string handlers.
- random: Uuid, random string and so on.
- redis_helper: Some tools base on redis.
- timetools: Some date/time/timezone tools.
- type_hint: Common type hints.
- api_service: Simple way to define an api client.
- \_\_init\_\_: Unclassified tools.


## Update logs
- **0.0.5** 2021-04-19: 
  - Added api service.
  - Optimized the performance of XlsxReader.
  - Added progress bar to XlsxExporter (supported by [tqdm](https://github.com/tqdm/tqdm)).
