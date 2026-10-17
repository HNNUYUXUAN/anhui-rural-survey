"""Regression checks for reading links, anchors and figure captions."""
import unittest

from bs4 import BeautifulSoup

from build_site import enhance, render_markdown


class ReadingPageTests(unittest.TestCase):
    def test_source_download_preserves_markdown_file(self):
        body, _ = enhance(render_markdown('[Markdown 源文件](report.md)'),
                          'report/README.md', 'report/guide.html')
        link = BeautifulSoup(body, 'html.parser').a
        self.assertEqual(link['href'], 'report.md')
        self.assertEqual(link['download'], 'report.md')

    def test_explicit_section_anchor_is_the_heading(self):
        body, toc = enhance(render_markdown('<a id="methods"></a>\n\n## 三、方法'),
                            'report/report.md', 'report/index.html')
        soup = BeautifulSoup(body, 'html.parser')
        self.assertEqual(len(soup.select('#methods')), 1)
        self.assertEqual(soup.select_one('#methods').name, 'h2')
        self.assertIn('href="#methods"', toc)
        self.assertTrue(toc.startswith('<ul>'))

    def test_bibliography_url_excludes_sentence_punctuation(self):
        source = '来源 https://example.org/paper?id=1. `https://example.org/code`'
        body, _ = enhance(render_markdown(source), 'references/bibliography.md',
                          'references/bibliography.html')
        soup = BeautifulSoup(body, 'html.parser')
        self.assertEqual([a['href'] for a in soup.select('a')], ['https://example.org/paper?id=1'])
        self.assertEqual(soup.get_text().strip(), source.replace('`', ''))

    def test_notebook_caption_follows_the_image(self):
        source = ('<section class="notebook-cell"><figure><img src="../assets/f.svg"></figure></section>'
                  '<p><strong>图1　土地状态</strong></p>')
        body, _ = enhance(source, 'notebook/index.md', 'notebook/index.html')
        figure = BeautifulSoup(body, 'html.parser').figure
        self.assertEqual(figure['id'], 'figure-1')
        self.assertEqual(figure.find_all(recursive=False)[-1].name, 'figcaption')


if __name__ == '__main__':
    unittest.main()
