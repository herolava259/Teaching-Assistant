# Logtash guide

## I. Overview
### 1. Introduction
- [Intro](https://www.tutorialspoint.com/logstash/logstash_introduction.htm)

## VII. Common Pulgins
| Type     | Plugin          | Description                                      |
|----------|-----------------|--------------------------------------------------|
| `input`  | `file`          | Read logs from a file                            |
|          | `tcp`, `udp`    | Receive logs over the network                    |
|          | `beats`         | Receive logs from Filebeat                       |
| `filter` | `grok`          | Parse logs using regex                           |
|          | `mutate`        | Rename, remove, or convert field types           |
|          | `date`          | Convert date strings to a standard date format   |
|          | `json`          | Parse JSON strings into fields                   |
| `output` | `elasticsearch` | Send logs to Elasticsearch                       |
|          | `file`          | Write logs to a file                             |
|          | `stdout`        | Print logs to the console                        |


## Sources and practices

- [Complete-guide-tutorialspoint](https://www.tutorialspoint.com/logstash/index.htm)
- [Grok-Pattern](https://github.com/elastic/logstash/blob/v1.4.2/patterns/grok-patterns)
- [example-mutate-filter-usage](https://viblo.asia/p/logstash-cho-bo-loc-dua-tren-du-lieu-log-request-va-response-GyZJZyBQ4jm)
- [aggregated-documentation](https://www.perplexity.ai/search/cach-su-dung-aggregate-filter-F4Z.R60tQpSbHZuImVNrzg?2=d)
- [setup-conifg-logstash-config](https://www.elastic.co/docs/reference/logstash/logstash-settings-file)
- [grok-debugger](https://grokdebugger.com/)
- [codec-multiline](https://github.com/logstash-plugins/logstash-codec-multiline/blob/main/docs/index.asciidoc)
- [setup-elk-for-log](https://viblo.asia/p/trien-khai-bo-log-tap-trung-centralized-logging-voi-docker-va-kubernettes-cho-server-su-dung-elk-stack-maGK7OdMKj2)
- [regex-simp-doc](https://quantrimang.com/hoc/regex-trong-python-165471)
- [grok-example](https://coralogix.com/blog/logstash-grok-tutorial-with-examples/)
- [filter-aggregate-docs](https://www.elastic.co/docs/reference/logstash/plugins/plugins-filters-aggregate)