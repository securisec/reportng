# -*- coding: utf-8 -*-
import reportng

reportng.DownloadAssets.download_assets('', theme='pulse')


r = reportng.ReportWriter(report_name='somename', brand='somebrand',
                          asciinema=True, code_highlight=True, progress_bar=True)
report = r.report_header()
content = """
    # fasfdds
    # fdsfsfsd
    # fdsfasdfsd
    # fdsfsdf
    # Malmö
    # 아름다운
    # 你好""" * 100
report += r.report_section(title='title', content=content, pre_tag=True,
                           tag_color='danger', title_color=False)
report += r.report_section(title='title', content=content, pre_tag=True,
                           tag_color='danger', title_color=False, overflow='')
report += r.report_image_carousel('a', 'b', a='a', b='b')
report += r.report_asciinema('https://asciinema.org/a/123683', title='title')
report += r.report_code_section(title='title', code="""
    $(document).ready(function() {
    $('pre code').each(function(i, block) {
        hljs.highlightBlock(block);
    });
    });)""")
report += r.report_captions('test')
report += r.report_cards(
    ('primary', 'a', 'a'), ('danger', 'a', 'a'),
    section=True, title='title', border_only=True
)
report += r.report_footer(message='message', github='a',
                          linkedin='a', email='a', twitter='a')
r.report_save(report, 'test.html')

