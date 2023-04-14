# databricks-dolly-15k_ja_by_fuguMT

https://github.com/databrickslabs/dolly/tree/master/data
↑
こちらで公開されているデータセットを、英日翻訳エンジンfuguMTを使ってローカルで翻訳したものです。
翻訳の精度は、fuguMTのデフォルト設定で翻訳したものです。

fuguMT -> https://huggingface.co/staka/fugumt-en-ja
fuguMT作者のstakaさんのブログ -> https://staka.jp/wordpress/

出来上がってみたら、すでにもっといい翻訳をされたがクニえもん.inc🤗さん（@kun1em0n）によって公開されていたので、そちらを使うことをおすすめします。
https://huggingface.co/datasets/kunishou/databricks-dolly-15k-ja
https://twitter.com/kun1em0n/status/1646441038415028224?s=20

プログラミング初心者である私（matsuvr）がローカルで翻訳エンジンを回していたら30時間近くかかりました。
すでに意味が無いデータセットではありますが、翻訳プログラムの練習のために作ったものではあるので、翻訳のソースと一緒に公開しておきます。
