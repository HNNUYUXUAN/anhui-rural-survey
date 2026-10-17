# 第三方运行资源

| 资源 | 版本 | 来源 | 用途与许可 |
|---|---|---|---|
| KaTeX | 0.19.0 | [官方项目](https://github.com/KaTeX/KaTeX) · [npm 包](https://www.npmjs.com/package/katex/v/0.19.0) | 网页公式渲染，MIT；正文见 [KaTeX 许可](../LICENSES/KaTeX.txt) |

`web/vendor/katex/` 保存该版本的压缩脚本、样式和公式字体。构建时原样复制到站点，浏览器从本站加载。

研究图表在本地使用系统提供的宋体与 Times New Roman 生成；发布结果保存为 PNG 或 SVG 字形轮廓。正文通过 CSS 优先请求访问者系统中的对应字体，并提供衬线字体回退。

研究参考文献及其题录见[参考文献目录](../references/README.md)，原创材料许可见 [LICENSE](../LICENSE)。
