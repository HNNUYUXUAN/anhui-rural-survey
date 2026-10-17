document.querySelectorAll('.math').forEach((node) => {
  katex.render(node.textContent, node, {
    displayMode: node.classList.contains('block'),
    throwOnError: false, strict: 'ignore', trust: false,
  });
});
const compactNavigation = window.matchMedia('(max-width: 800px)').matches;
if (compactNavigation) {
  document.querySelectorAll('.toc details').forEach((toc) => { toc.open = false; });
  document.querySelectorAll('.toc a').forEach((link) => {
    link.addEventListener('click', () => { link.closest('details').open = false; });
  });
}
document.querySelectorAll('[data-code]').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.code-cell').forEach((cell) => {
      cell.open = button.dataset.code === 'show';
    });
    document.getElementById('code-status').textContent =
      button.dataset.code === 'show' ? '代码已全部展开' : '代码已全部收起';
  });
});
document.querySelectorAll('[data-print]').forEach((button) => {
  button.addEventListener('click', () => window.print());
});
